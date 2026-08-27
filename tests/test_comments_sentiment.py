"""
Unit and integration tests for reader feedback comment section,
RSS comment perspective extraction, and semantic sentiment analysis.
"""

import pytest
import news
from news import (
    app,
    get_db,
    SemanticSentimentAnalyzer,
    aggregate_comments_sentiment,
    get_comments_for_article,
    generate_rss_perspectives,
    fetch_and_store_rss_comments,
    get_cluster_sentiment,
    cluster_articles,
)


class TestSemanticSentimentAnalyzer:
    """Test the NLP/Semantic Sentiment Analyzer engine."""

    def test_strong_positive_text(self):
        text = "This is an extraordinary breakthrough! Incredible progress and magnificent results."
        res = SemanticSentimentAnalyzer.analyze(text)
        assert res["positivity_pct"] > 75
        assert res["negativity_pct"] < 25
        assert res["positivity_pct"] + res["negativity_pct"] == 100
        assert res["sentiment"] == "positive"
        assert "Positive" in res["label"]

    def test_strong_negative_text(self):
        text = "Terrible disaster and devastating crisis. Total catastrophe with catastrophic failure."
        res = SemanticSentimentAnalyzer.analyze(text)
        assert res["negativity_pct"] > 70
        assert res["positivity_pct"] < 30
        assert res["positivity_pct"] + res["negativity_pct"] == 100
        assert res["sentiment"] == "negative"
        assert "Critical" in res["label"]

    def test_negation_handling(self):
        positive_text = "The product is good and reliable."
        negated_text = "The product is not good and never reliable."

        pos_res = SemanticSentimentAnalyzer.analyze(positive_text)
        neg_res = SemanticSentimentAnalyzer.analyze(negated_text)

        assert pos_res["positivity_pct"] > neg_res["positivity_pct"]
        assert neg_res["negativity_pct"] > pos_res["negativity_pct"]

    def test_contrastive_clause_handling(self):
        text = "The launch was smooth, but the severe backend collapse caused complete disruption and massive outages."
        res = SemanticSentimentAnalyzer.analyze(text)
        assert res["negativity_pct"] > 50

    def test_neutral_balanced_text(self):
        text = "The committee held a regular standard meeting on Tuesday to review regular schedule reports."
        res = SemanticSentimentAnalyzer.analyze(text)
        assert 35 <= res["positivity_pct"] <= 65
        assert res["positivity_pct"] + res["negativity_pct"] == 100

    def test_score_boundaries(self):
        empty_res = SemanticSentimentAnalyzer.analyze("")
        assert empty_res["positivity_pct"] == 50
        assert empty_res["negativity_pct"] == 50
        assert empty_res["positivity_pct"] + empty_res["negativity_pct"] == 100


class TestAggregationAndRSS:
    """Test aggregation and RSS perspective generation."""

    def test_aggregate_comments_sentiment_empty_fallback(self):
        title = "Incredible Economic Recovery Surpasses Expectations"
        res = aggregate_comments_sentiment([], fallback_text=title)
        assert res["has_comments"] is False
        assert res["positivity_pct"] > 60
        assert res["positivity_pct"] + res["negativity_pct"] == 100

    def test_aggregate_comments_sentiment_with_comments(self):
        comments = [
            {"sentiment": "positive", "positivity_score": 0.9, "negativity_score": 0.1, "rating": 5},
            {"sentiment": "positive", "positivity_score": 0.85, "negativity_score": 0.15, "rating": 4},
            {"sentiment": "negative", "positivity_score": 0.2, "negativity_score": 0.8, "rating": 1},
        ]
        res = aggregate_comments_sentiment(comments)
        assert res["has_comments"] is True
        assert res["total_comments"] == 3
        assert res["positive_count"] == 2
        assert res["negative_count"] == 1
        assert res["positivity_pct"] > res["negativity_pct"]
        assert res["positivity_pct"] + res["negativity_pct"] == 100

    def test_generate_rss_perspectives(self):
        articles = [
            {
                "title": "Quantum Computing Reaches Historic Milestones",
                "summary": "Engineers achieved unprecedented coherence time and fault tolerance.",
                "source": "TechCrunch",
                "url": "https://techcrunch.com/quantum",
            },
            {
                "title": "Concerns Raised Over High Hardware Costs in Quantum Computing",
                "summary": "Critics warn infrastructure costs remain exorbitant and scalability is uncertain.",
                "source": "The Verge",
                "url": "https://theverge.com/quantum-costs",
            }
        ]
        perspectives = generate_rss_perspectives("Quantum Computing Breakthrough", articles)
        assert len(perspectives) >= 2
        assert any(p["sentiment"] in ("positive", "negative", "neutral") for p in perspectives)
        assert all("rss" in p["source"].lower() for p in perspectives)


class TestCommentsAPI:
    """Test the Flask REST endpoints for feedback comments."""

    def test_post_comment_and_retrieve(self, test_db_path):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["user_id"] = 1

            # Seed user
            with get_db() as db:
                user = db.execute("SELECT id FROM users WHERE id = 1").fetchone()
                if not user:
                    db.execute("INSERT INTO users (id, username, email) VALUES (1, 'alice', 'alice@example.com')")

            article_title = "Global Summit on Clean Energy Innovation"
            post_res = client.post(
                "/api/comments",
                json={
                    "title": article_title,
                    "content": "Outstanding initiatives announced! This will greatly accelerate sustainability and clean power.",
                    "url": "https://example.com/energy-summit",
                },
            )
            assert post_res.status_code == 200
            post_data = post_res.get_json()
            assert post_data["success"] is True
            assert post_data["comment"]["author_name"] == "alice"
            assert post_data["comment"]["sentiment"] == "positive"
            assert post_data["comment"]["positivity_pct"] > 70

            # GET comments
            get_res = client.get(f"/api/comments?title={article_title}")
            assert get_res.status_code == 200
            get_data = get_res.get_json()
            assert get_data["total_comments"] >= 1
            assert get_data["sentiment"]["positivity_pct"] > 60

            # Post a negative comment
            client.post(
                "/api/comments",
                json={
                    "title": article_title,
                    "content": "Terrible outcome with severe deficiencies and disappointing lack of real commitments.",
                },
            )

            # Re-fetch comments
            updated_get = client.get(f"/api/comments?title={article_title}")
            updated_data = updated_get.get_json()
            assert updated_data["total_comments"] >= 2
            assert updated_data["sentiment"]["positive_count"] >= 1
            assert updated_data["sentiment"]["negative_count"] >= 1

    def test_delete_comment(self, test_db_path):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["user_id"] = 1

            with get_db() as db:
                user = db.execute("SELECT id FROM users WHERE id = 1").fetchone()
                if not user:
                    db.execute("INSERT INTO users (id, username, email) VALUES (1, 'alice', 'alice@example.com')")

            article_title = "Tech Policy Update"
            res = client.post(
                "/api/comments",
                json={
                    "title": article_title,
                    "content": "A thoughtful and balanced approach to regulating digital platforms.",
                },
            )
            comment_id = res.get_json()["comment"]["id"]

            # Delete comment
            del_res = client.delete(f"/api/comments/{comment_id}")
            assert del_res.status_code == 200
            assert del_res.get_json()["success"] is True

            # Verify deletion
            with get_db() as db:
                deleted = db.execute("SELECT id FROM article_comments WHERE id = ?", (comment_id,)).fetchone()
                assert deleted is None

    def test_validation_errors(self, test_db_path):
        with app.test_client() as client:
            with get_db() as db:
                user = db.execute("SELECT id FROM users WHERE id = 1").fetchone()
                if not user:
                    db.execute("INSERT INTO users (id, username, email) VALUES (1, 'alice', 'alice@example.com')")

            with client.session_transaction() as sess:
                sess["user_id"] = 1

            # Missing title
            res1 = client.post("/api/comments", json={"content": "Great article"})
            assert res1.status_code == 400

            # Missing content
            res2 = client.post("/api/comments", json={"title": "Some Story", "content": ""})
            assert res2.status_code == 400

            # GET without title
            res3 = client.get("/api/comments")
            assert res3.status_code == 400


class TestClusterSentimentIntegration:
    """Test that cluster_articles embeds semantic sentiment."""

    def test_cluster_sentiment_presence(self):
        articles = [
            {
                "title": "Revolutionary AI Breakthrough Boosts Medical Diagnoses",
                "summary": "Innovative diagnostic tool dramatically improves patient survival rates.",
                "url": "https://example.com/ai-med",
                "image": None,
                "published": "2026-08-20T10:00:00Z",
                "source": "HealthTech",
                "domain": "healthtech.com",
            }
        ]
        clusters = cluster_articles(articles, query="healthcare")
        assert len(clusters) > 0
        first_cluster = list(clusters.values())[0]
        assert "sentiment" in first_cluster
        sentiment = first_cluster["sentiment"]
        assert "positivity_pct" in sentiment
        assert "negativity_pct" in sentiment
        assert sentiment["positivity_pct"] + sentiment["negativity_pct"] == 100
        assert sentiment["positivity_pct"] > 60
