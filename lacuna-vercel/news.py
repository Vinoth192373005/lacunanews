from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
import feedparser
import re
import html
import math
import hashlib
import json
import os
import secrets
import sqlite3
import pandas as pd
import urllib.parse
import networkx as nx
import numpy as np
import concurrent.futures
import requests
from contextlib import contextmanager
from functools import wraps
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import normalize
from werkzeug.security import check_password_hash, generate_password_hash

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:
    psycopg = None
    dict_row = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-change-me")

is_serverless = bool(
    os.environ.get("VERCEL")
    or os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
    or os.environ.get("DATABASE_PATH")
)
default_db_path = "/tmp/lacuna.sqlite3" if is_serverless else os.path.join(app.instance_path, "lacuna.sqlite3")
app.config["DATABASE"] = os.environ.get("DATABASE_PATH", default_db_path)
def resolve_database_url():
    for var in (
        "DATABASE_URL",
        "POSTGRES_URL",
        "STORAGE_URL",
        "STORAGE_DATABASE_URL",
        "STORAGE_POSTGRES_URL",
        "POSTGRES_PRISMA_URL",
        "NEON_DATABASE_URL",
    ):
        val = os.environ.get(var, "").strip()
        if val:
            return val
    return ""


app.config["DATABASE_URL"] = resolve_database_url()

USE_POSTGRES = bool(app.config["DATABASE_URL"])
UNIQUE_ERRORS = (sqlite3.IntegrityError,)
if psycopg is not None:
    UNIQUE_ERRORS = UNIQUE_ERRORS + (psycopg.errors.UniqueViolation,)


@contextmanager
def get_db():
    if USE_POSTGRES:
        if psycopg is None:
            raise RuntimeError("DATABASE_URL is set, but psycopg is not installed.")
        db_url = app.config["DATABASE_URL"]
        if db_url.startswith("postgres://"):
            db_url = "postgresql://" + db_url[len("postgres://"):]
        conn = psycopg.connect(db_url, row_factory=dict_row)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    else:
        db_path = app.config["DATABASE"]
        db_dir = os.path.dirname(os.path.abspath(db_path))
        if db_dir:
            try:
                os.makedirs(db_dir, exist_ok=True)
            except OSError:
                pass
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


def sql_param():
    return "%s" if USE_POSTGRES else "?"


def init_db():
    with get_db() as db:
        if USE_POSTGRES:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT UNIQUE,
                    google_id TEXT UNIQUE,
                    avatar_url TEXT,
                    preferred_region TEXT DEFAULT 'US',
                    password_hash TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            # Safe column migrations for existing postgres tables
            for col in ["email", "google_id", "avatar_url", "preferred_region"]:
                try:
                    db.execute(f"ALTER TABLE users ADD COLUMN IF NOT EXISTS {col} TEXT")
                except Exception:
                    pass
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS article_history (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
                    title TEXT NOT NULL,
                    article_text TEXT NOT NULL,
                    image_url TEXT,
                    source_count INTEGER NOT NULL DEFAULT 0,
                    sources_json TEXT NOT NULL DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS user_interests (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
                    interest TEXT NOT NULL,
                    source_type TEXT NOT NULL DEFAULT 'manual',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT uq_user_interest UNIQUE (user_id, interest)
                )
                """
            )
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS bookmarks (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
                    title TEXT NOT NULL,
                    article_text TEXT NOT NULL DEFAULT '',
                    image_url TEXT,
                    source_count INTEGER NOT NULL DEFAULT 0,
                    sources_json TEXT NOT NULL DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT uq_user_bookmark UNIQUE (user_id, title)
                )
                """
            )
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS article_comments (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users (id) ON DELETE SET NULL,
                    article_title TEXT NOT NULL,
                    article_url TEXT,
                    author_name TEXT NOT NULL,
                    avatar_url TEXT,
                    content TEXT NOT NULL,
                    sentiment TEXT NOT NULL DEFAULT 'neutral',
                    positivity_score REAL NOT NULL DEFAULT 0.5,
                    negativity_score REAL NOT NULL DEFAULT 0.5,
                    source TEXT NOT NULL DEFAULT 'user',
                    rating INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            try:
                db.execute("CREATE INDEX IF NOT EXISTS idx_comments_title ON article_comments (article_title)")
                db.execute("CREATE INDEX IF NOT EXISTS idx_comments_created ON article_comments (created_at)")
            except Exception:
                pass
        else:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT UNIQUE,
                    google_id TEXT UNIQUE,
                    avatar_url TEXT,
                    preferred_region TEXT DEFAULT 'US',
                    password_hash TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            # Safe column migrations for existing sqlite tables
            for col in ["email", "google_id", "avatar_url", "preferred_region"]:
                try:
                    db.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT")
                except Exception:
                    pass
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS article_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    article_text TEXT NOT NULL,
                    image_url TEXT,
                    source_count INTEGER NOT NULL DEFAULT 0,
                    sources_json TEXT NOT NULL DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
                """
            )
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS user_interests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    interest TEXT NOT NULL,
                    source_type TEXT NOT NULL DEFAULT 'manual',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                    UNIQUE (user_id, interest)
                )
                """
            )
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS bookmarks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    article_text TEXT NOT NULL DEFAULT '',
                    image_url TEXT,
                    source_count INTEGER NOT NULL DEFAULT 0,
                    sources_json TEXT NOT NULL DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                    UNIQUE (user_id, title)
                )
                """
            )
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS article_comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    article_title TEXT NOT NULL,
                    article_url TEXT,
                    author_name TEXT NOT NULL,
                    avatar_url TEXT,
                    content TEXT NOT NULL,
                    sentiment TEXT NOT NULL DEFAULT 'neutral',
                    positivity_score REAL NOT NULL DEFAULT 0.5,
                    negativity_score REAL NOT NULL DEFAULT 0.5,
                    source TEXT NOT NULL DEFAULT 'user',
                    rating INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
                )
                """
            )
            try:
                db.execute("CREATE INDEX IF NOT EXISTS idx_comments_title ON article_comments (article_title)")
                db.execute("CREATE INDEX IF NOT EXISTS idx_comments_created ON article_comments (created_at)")
            except Exception:
                pass

        # Purge legacy fabricated/synthetic reporter comments
        try:
            db.execute("""
                DELETE FROM article_comments
                WHERE author_name LIKE '% Reporter'
                   OR source LIKE 'RSS:%'
                   OR source IN ('RSS Feed', 'RSS Community', 'RSS Wire')
            """)
        except Exception:
            pass


_db_initialized = False


def ensure_db():
    global _db_initialized
    if not _db_initialized:
        try:
            init_db()
            _db_initialized = True
        except Exception as e:
            app.logger.warning("ensure_db deferral: %s", e)


@app.before_request
def before_request_hook():
    ensure_db()


try:
    init_db()
    _db_initialized = True
except Exception as e:
    app.logger.warning("Initial init_db failed, will retry on request: %s", e)


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    with get_db() as db:
        return db.execute(
            f"SELECT id, username, email, google_id, avatar_url, preferred_region, created_at FROM users WHERE id = {sql_param()}",
            (user_id,),
        ).fetchone()


def get_user_region(user=None):
    if user is None:
        user = current_user()
    if user:
        try:
            val = user["preferred_region"]
            if val:
                return str(val).upper()
        except (KeyError, IndexError, TypeError):
            pass
    return (session.get("region") or DEFAULT_REGION).upper()


def history_row_to_dict(row):
    sources_raw = row["sources_json"] if row["sources_json"] else "[]"
    try:
        sources = json.loads(sources_raw)
    except (TypeError, ValueError):
        sources = []

    created_at = row["created_at"]
    if hasattr(created_at, "isoformat"):
        created_at = created_at.isoformat()

    img = row["image_url"]
    return {
        "id": row["id"],
        "title": row["title"],
        "article": row["article_text"],
        "article_text": row["article_text"],
        "image": img,
        "image_url": img,
        "cluster_image": img,
        "source_count": row["source_count"],
        "sources": sources,
        "created_at": created_at,
    }


def bookmark_row_to_dict(row):
    sources_raw = row["sources_json"] if row["sources_json"] else "[]"
    try:
        sources = json.loads(sources_raw)
    except (TypeError, ValueError):
        sources = []

    created_at = row["created_at"]
    if hasattr(created_at, "isoformat"):
        created_at = created_at.isoformat()

    img = row["image_url"]
    return {
        "id": row["id"],
        "title": row["title"],
        "article": row["article_text"],
        "article_text": row["article_text"],
        "image": img,
        "image_url": img,
        "cluster_image": img,
        "source_count": row["source_count"],
        "sources": sources,
        "created_at": created_at,
    }


def comment_row_to_dict(row):
    if not row:
        return None
    created_at = row["created_at"]
    if hasattr(created_at, "isoformat"):
        created_at = created_at.isoformat()
    elif created_at is not None:
        created_at = str(created_at)

    pos_score = float(row["positivity_score"] if row["positivity_score"] is not None else 0.5)
    neg_score = float(row["negativity_score"] if row["negativity_score"] is not None else 0.5)
    pos_pct = int(round(pos_score * 100))
    neg_pct = 100 - pos_pct

    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "article_title": row["article_title"],
        "article_url": row["article_url"] or "",
        "author_name": row["author_name"] or "Community Reader",
        "avatar_url": row["avatar_url"] or "",
        "content": row["content"],
        "sentiment": row["sentiment"],
        "positivity_score": pos_score,
        "negativity_score": neg_score,
        "positivity_pct": pos_pct,
        "negativity_pct": neg_pct,
        "source": row["source"] or "user",
        "rating": row["rating"] or 0,
        "created_at": created_at,
    }


class SemanticSentimentAnalyzer:
    """
    Advanced semantic sentiment analysis engine combining domain-tuned sentiment
    valence lexicons, morphological stemming variants, contextual modifier resolution
    (negation, intensifiers, diminishers, contrastive conjunctions), emoji semantics,
    and TF-IDF prototype anchoring.
    """
    POSITIVE_WORDS = {
        'breakthrough': 3.2, 'groundbreaking': 3.4, 'innovative': 2.8, 'revolutionary': 3.0,
        'milestone': 2.6, 'triumph': 3.0, 'uplifting': 2.8, 'inspiring': 2.9, 'superb': 3.0,
        'excellent': 2.8, 'great': 2.2, 'good': 1.6, 'positive': 2.0, 'promising': 2.4,
        'remarkable': 2.7, 'impressive': 2.5, 'outstanding': 3.1, 'admirable': 2.6,
        'effective': 2.0, 'efficient': 2.1, 'boost': 2.2, 'surge': 2.0, 'recovery': 2.4,
        'recover': 2.4, 'recovering': 2.4, 'progress': 2.3, 'growth': 2.2, 'grow': 2.0,
        'success': 2.8, 'successful': 2.7, 'succeed': 2.5, 'beneficial': 2.5, 'benefit': 2.2,
        'thrive': 2.6, 'thriving': 2.6, 'love': 2.7, 'like': 1.5, 'hope': 2.0, 'optimism': 2.6,
        'optimistic': 2.5, 'gain': 1.8, 'gains': 2.0, 'support': 2.0, 'supported': 2.0,
        'agree': 1.8, 'agreement': 2.2, 'agrees': 1.8, 'agreed': 1.8, 'applaud': 2.8,
        'applauds': 2.8, 'celebrate': 2.9, 'celebrates': 2.9, 'celebration': 2.8,
        'masterpiece': 3.5, 'solid': 1.8, 'strong': 2.0, 'brilliant': 3.0, 'wonderful': 2.8,
        'fantastic': 2.9, 'fabulous': 2.8, 'victory': 3.0, 'victories': 3.0, 'victorious': 3.0,
        'prosper': 2.7, 'prosperity': 2.8, 'sustainable': 2.2, 'praise': 2.4, 'praised': 2.4,
        'praises': 2.4, 'honor': 2.3, 'honored': 2.3, 'award': 2.2, 'awarded': 2.2,
        'advancement': 2.5, 'advance': 2.3, 'advances': 2.3, 'visionary': 2.8, 'commend': 2.5,
        'commendable': 2.6, 'cheer': 2.2, 'cheers': 2.2, 'stellar': 3.0, 'phenomenal': 3.2,
        'exquisite': 2.8, 'genius': 3.0, 'fascinating': 2.4, 'delightful': 2.6, 'thrilling': 2.7,
        'champion': 2.6, 'champions': 2.6, 'miracle': 3.2, 'robust': 2.2, 'resilient': 2.4,
        'resilience': 2.4, 'harmony': 2.2, 'peaceful': 2.4, 'peace': 2.4, 'ceasefire': 2.6,
        'truce': 2.4, 'treaty': 2.4, 'accord': 2.2, 'deal': 1.8, 'settle': 1.8, 'settlement': 2.0,
        'reconcile': 2.2, 'reconciliation': 2.4, 'relief': 2.4, 'rescue': 2.6, 'rescued': 2.6,
        'rescues': 2.6, 'save': 2.4, 'saved': 2.4, 'saves': 2.4, 'survive': 2.2, 'survived': 2.2,
        'survivor': 2.2, 'survivors': 2.2, 'aid': 2.0, 'funding': 1.8, 'cure': 3.0, 'cured': 3.0,
        'cures': 3.0, 'heal': 2.4, 'healing': 2.4, 'healed': 2.4, 'rebound': 2.2, 'rebounds': 2.2,
        'rally': 2.2, 'rallies': 2.2, 'soar': 2.4, 'soars': 2.4, 'soaring': 2.4, 'win': 2.6,
        'wins': 2.6, 'won': 2.6, 'safe': 2.0, 'safest': 2.4, 'safety': 2.2, 'secure': 2.0,
        'security': 2.0, 'clean': 1.8, 'renewable': 2.0, 'clear': 1.6, 'clarity': 2.0,
        'justice': 2.4, 'empower': 2.4, 'empowerment': 2.5, 'wisdom': 2.5, 'dazzling': 2.7,
        'valuable': 2.2, 'advantage': 2.0, 'favorable': 2.2, 'favor': 1.8, 'upgrade': 1.8,
        'upgrades': 1.8, 'upgraded': 1.8, 'flourish': 2.5, 'flourishing': 2.5, 'pioneering': 2.8,
        'pioneer': 2.5, 'credible': 2.0, 'trustworthy': 2.5, 'generous': 2.2, 'pleased': 2.0,
        'enjoyable': 2.2, 'perfect': 3.0, 'worthwhile': 2.3, 'lucrative': 2.2, 'brilliance': 2.8,
        'promptly': 1.5, 'avert': 1.6, 'averts': 1.6, 'averted': 1.6, 'cooperation': 2.2,
        'cooperate': 2.0, 'collaboration': 2.0, 'collaborate': 2.0, 'partnership': 2.0,
    }

    NEGATIVE_WORDS = {
        'disaster': -3.5, 'catastrophic': -3.6, 'catastrophe': -3.6, 'crisis': -2.8, 'crises': -2.8,
        'failure': -3.0, 'failed': -2.8, 'fail': -2.6, 'fails': -2.6, 'terrible': -3.0,
        'horrible': -3.0, 'awful': -2.9, 'bad': -1.8, 'worst': -3.3, 'corrupt': -3.2,
        'corruption': -3.3, 'collapse': -3.2, 'collapses': -3.2, 'collapsed': -3.2,
        'plunge': -2.6, 'plunges': -2.6, 'plunged': -2.6, 'crash': -3.0, 'crashes': -3.0,
        'crashed': -3.0, 'devastating': -3.4, 'devastate': -3.2, 'devastates': -3.2,
        'devastated': -3.4, 'devastation': -3.4, 'scandal': -3.1, 'scandals': -3.1,
        'harmful': -2.7, 'harm': -2.5, 'harms': -2.5, 'harmed': -2.5, 'toxic': -3.0,
        'unethical': -3.0, 'atrocious': -3.2, 'miserable': -2.8, 'worsen': -2.5, 'worsening': -2.6,
        'worsens': -2.5, 'worsened': -2.5, 'worse': -2.6, 'danger': -2.7, 'dangers': -2.7,
        'dangerous': -2.8, 'threat': -2.7, 'threats': -2.7, 'threaten': -2.7, 'threatens': -2.7,
        'threatened': -2.7, 'threatening': -2.7, 'outrage': -3.0, 'outraged': -3.0,
        'disappointing': -2.5, 'disappointment': -2.6, 'disappointed': -2.5, 'flawed': -2.2,
        'flaw': -2.0, 'flaws': -2.0, 'fraud': -3.5, 'fraudulent': -3.5, 'tragic': -3.2,
        'tragedy': -3.2, 'tragedies': -3.2, 'decline': -2.0, 'declines': -2.0, 'declined': -2.0,
        'loss': -2.2, 'losses': -2.4, 'lose': -2.0, 'loses': -2.0, 'lost': -2.0, 'losing': -2.0,
        'suffer': -2.7, 'suffering': -2.8, 'suffers': -2.7, 'suffered': -2.7, 'horrific': -3.4,
        'chaos': -2.9, 'chaotic': -2.8, 'hate': -2.9, 'hates': -2.9, 'hated': -2.9,
        'condemn': -2.8, 'condemns': -2.8, 'condemned': -2.8, 'condemning': -2.8, 'oppose': -2.0,
        'opposes': -2.0, 'opposed': -2.0, 'opposing': -2.0, 'alarming': -2.7, 'alarm': -2.2,
        'alarms': -2.2, 'alarmed': -2.2, 'bleak': -2.6, 'doomed': -3.2, 'useless': -2.5,
        'reckless': -2.8, 'ruin': -3.0, 'ruined': -3.0, 'ruins': -3.0, 'destruction': -3.2,
        'destroy': -3.2, 'destroys': -3.2, 'destroyed': -3.2, 'destructive': -3.0,
        'slaughter': -3.8, 'controversy': -2.2, 'controversial': -2.0, 'guilt': -2.2,
        'guilty': -2.4, 'crime': -2.8, 'crimes': -2.8, 'criminal': -2.8, 'criminals': -2.8,
        'exploit': -2.6, 'exploits': -2.6, 'exploited': -2.6, 'exploitation': -2.8,
        'poverty': -2.6, 'famine': -3.4, 'inflation': -2.0, 'recession': -2.8, 'depression': -2.8,
        'deficit': -2.0, 'deficits': -2.0, 'breach': -2.5, 'breaches': -2.5, 'breached': -2.5,
        'vulnerability': -2.2, 'vulnerabilities': -2.2, 'vulnerable': -2.0, 'fake': -2.5,
        'deceit': -3.0, 'lie': -2.8, 'lies': -2.8, 'lying': -2.8, 'cruel': -3.2, 'cruelty': -3.2,
        'violence': -3.2, 'violent': -3.0, 'assault': -3.2, 'assaults': -3.2, 'assaulted': -3.2,
        'murder': -3.8, 'murders': -3.8, 'murdered': -3.8, 'manslaughter': -3.6, 'kill': -3.5,
        'kills': -3.5, 'killed': -3.5, 'killing': -3.5, 'killings': -3.5, 'dead': -3.0,
        'death': -3.0, 'deaths': -3.2, 'fatal': -3.4, 'fatality': -3.4, 'fatalities': -3.5,
        'brutal': -3.2, 'brutality': -3.2, 'oppress': -3.0, 'oppression': -3.0,
        'discrimination': -3.0, 'disgust': -3.0, 'disgusting': -3.2, 'shameful': -2.8,
        'shame': -2.5, 'disgraceful': -3.0, 'disgrace': -2.8, 'downfall': -2.8, 'backlash': -2.6,
        'rebuke': -2.4, 'rebukes': -2.4, 'rebuked': -2.4, 'setback': -2.4, 'setbacks': -2.4,
        'stumble': -2.0, 'stumbles': -2.0, 'stumbled': -2.0, 'cynical': -2.0, 'pessimistic': -2.2,
        'waste': -2.2, 'worthless': -3.0, 'obsolete': -2.0, 'disarray': -2.5, 'distress': -2.6,
        'panic': -2.8, 'panicked': -2.8, 'attack': -3.2, 'attacks': -3.2, 'attacked': -3.2,
        'attacking': -3.2, 'attacker': -3.2, 'attackers': -3.2, 'strike': -2.8, 'strikes': -2.8,
        'struck': -2.8, 'striking': -2.8, 'warn': -2.0, 'warns': -2.0, 'warned': -2.0,
        'warning': -2.2, 'warnings': -2.2, 'criticize': -2.4, 'criticizes': -2.4,
        'criticized': -2.4, 'criticizing': -2.4, 'criticism': -2.2, 'critique': -1.8,
        'misconduct': -3.0, 'furious': -3.0, 'fury': -3.0, 'anger': -2.8, 'angry': -2.8,
        'toll': -2.2, 'tolls': -2.2, 'sanction': -2.4, 'sanctions': -2.6, 'sanctioned': -2.6,
        'freeze': -2.0, 'frozen': -2.0, 'freezes': -2.0, 'ban': -2.2, 'banned': -2.4,
        'bans': -2.2, 'banning': -2.4, 'downturn': -2.6, 'downturns': -2.6, 'layoff': -2.8,
        'layoffs': -3.0, 'laid off': -3.0, 'slump': -2.4, 'slumps': -2.4, 'slumped': -2.4,
        'tumble': -2.2, 'tumbles': -2.2, 'tumbled': -2.2, 'drop': -1.8, 'drops': -1.8,
        'dropped': -1.8, 'dropping': -1.8, 'wildfire': -3.0, 'wildfires': -3.0, 'flood': -3.0,
        'floods': -3.0, 'flooding': -3.0, 'flooded': -3.0, 'storm': -2.4, 'storms': -2.4,
        'hurricane': -3.2, 'cyclone': -3.2, 'tornado': -3.2, 'earthquake': -3.4, 'missing': -2.6,
        'extradite': -1.8, 'extradition': -2.0, 'inquiry': -1.5, 'investigate': -1.8,
        'investigation': -2.0, 'probe': -2.0, 'probes': -2.0, 'probed': -2.0, 'misstep': -2.2,
        'missteps': -2.2, 'reckoning': -2.5, 'dip': -1.4, 'dips': -1.4, 'dipped': -1.4,
        'clash': -2.6, 'clashes': -2.6, 'clashed': -2.6, 'clashing': -2.6, 'war': -3.5,
        'wars': -3.5, 'conflict': -2.8, 'conflicts': -2.8, 'hostage': -3.6, 'hostages': -3.6,
        'bomb': -3.6, 'bombs': -3.6, 'bombing': -3.6, 'blast': -3.4, 'blasts': -3.4,
        'missile': -3.2, 'missiles': -3.2, 'casualty': -3.2, 'casualties': -3.5,
        'injured': -2.6, 'injuries': -2.6, 'wound': -2.6, 'wounds': -2.6, 'wounded': -2.6,
    }

    INTENSIFIERS = {
        'extremely': 1.6, 'hugely': 1.5, 'tremendously': 1.6, 'immensely': 1.6, 'deeply': 1.4,
        'remarkably': 1.4, 'utterly': 1.7, 'absolutely': 1.6, 'totally': 1.5, 'highly': 1.4,
        'significantly': 1.4, 'so': 1.3, 'truly': 1.4, 'very': 1.35, 'really': 1.3,
        'exceptionally': 1.6, 'insanely': 1.5, 'wildly': 1.4, 'strongly': 1.4, 'completely': 1.4,
        'massively': 1.6, 'severely': 1.6, 'heavily': 1.4,
    }

    DIMINISHERS = {
        'somewhat': 0.6, 'slightly': 0.5, 'barely': 0.5, 'mildly': 0.6, 'a bit': 0.6,
        'marginally': 0.5, 'scarcely': 0.5, 'partially': 0.7, 'kind of': 0.6, 'sort of': 0.6,
    }

    NEGATORS = {
        'not', 'no', 'never', 'none', 'neither', 'nor', 'barely', 'scarcely', 'hardly',
        'doesnt', 'dont', 'didnt', 'isnt', 'arent', 'wasnt', 'werent', 'cannot', 'cant',
        'wont', 'without', 'lacks', 'failed to'
    }

    EMOJIS = {
        '👍': 2.5, '❤️': 3.0, '🔥': 2.2, '🚀': 2.5, '👏': 2.2, '✨': 1.8, '💯': 2.5,
        '😊': 2.0, '🎉': 2.6, '💪': 2.0, '💡': 1.5, '🌟': 2.2, '🏆': 2.8, '🙌': 2.2,
        '👎': -2.5, '😡': -3.0, '💩': -3.0, '💔': -2.5, '😢': -2.2, '🤮': -3.5,
        '🤡': -2.2, '📉': -2.0, '⚠️': -1.8, '❌': -2.0, '🤦': -2.2, '⛔': -2.0,
    }

    _vectorizer = None
    _proto_matrix = None

    @classmethod
    def _stem_variants(cls, w: str) -> list:
        stems = [w]
        if w.endswith('ies') and len(w) > 4:
            stems.append(w[:-3] + 'y')
        if w.endswith('es') and len(w) > 3:
            stems.append(w[:-2])
        if w.endswith('s') and len(w) > 2 and not w.endswith('ss'):
            stems.append(w[:-1])
        if w.endswith('ed') and len(w) > 3:
            stems.append(w[:-2])
            stems.append(w[:-1])
        if w.endswith('ing') and len(w) > 4:
            stems.append(w[:-3])
            stems.append(w[:-3] + 'e')
        if w.endswith('ly') and len(w) > 3:
            stems.append(w[:-2])
        return stems

    @classmethod
    def _init_vectorizer(cls):
        if cls._vectorizer is None:
            try:
                pos_proto = (
                    "groundbreaking breakthrough innovative innovation milestone revolutionary triumph "
                    "uplifting inspiring superb excellent great positive promising remarkable impressive "
                    "outstanding recovery recover progress growth grow success successful beneficial benefit "
                    "victory victorious sustainable visionary heroic brilliant fantastic achievement advancement "
                    "thriving thrive admirable solution support applaud commend cheer peace peaceful ceasefire "
                    "truce treaty accord agreement agree settlement reconcile reconciliation relief rescue save "
                    "cure cured heal healing rebound rally soar win wins won safe safety clean renewable deal "
                    "cooperation collaborate partnership record profits surge expansion boom aid prosperity"
                )
                neg_proto = (
                    "disaster catastrophic catastrophe crisis crises failure failed fail terrible horrible awful "
                    "corrupt corruption collapse plunge crash devastating devastate scandal harmful toxic "
                    "unethical atrocious miserable worsening danger dangerous threat threaten outrage "
                    "disappointing flawed fraud tragic tragedy decline loss losses lose suffering horrific chaos "
                    "alarming doomed useless reckless controversy controversial setback stumble recession inflation "
                    "murder manslaughter kill killed killing death deaths fatal fatalities assault brutal violence "
                    "violent attack attacks warning warn warned strike strikes criticize criticizes misconduct furious "
                    "toll sanctions banned ban layoff layoffs downturn slump wildfire flood earthquake missing clash "
                    "war conflict hostage bomb blast missile casualty injured emergency wreckage panic dispute"
                )
                cls._vectorizer = TfidfVectorizer(stop_words='english')
                cls._vectorizer.fit([pos_proto, neg_proto])
                cls._proto_matrix = cls._vectorizer.transform([pos_proto, neg_proto])
            except Exception:
                cls._vectorizer = False

    @classmethod
    def analyze(cls, text: str, **kwargs) -> dict:
        """
        Pure semantic NLP analysis of text sentiment using fine-tuned valence lexicons,
        morphological stemming lookups, negation detection, intensifiers/diminishers,
        contrastive clause weighting, punctuation/emoji signals, and TF-IDF semantic
        prototype vector cosine similarity.
        """
        if not text:
            return {
                'compound': 0.0,
                'positivity_score': 0.5,
                'negativity_score': 0.5,
                'positivity_pct': 50,
                'negativity_pct': 50,
                'sentiment': 'neutral',
                'label': 'Mixed / Balanced',
            }

        # Contrastive clauses: clauses after 'but', 'however', etc. carry more weight
        clauses = re.split(r'\b(?:but|however|although|nevertheless|nonetheless|yet|whereas)\b', text, flags=re.IGNORECASE)
        clause_scores = []

        for idx, clause in enumerate(clauses):
            weight = 0.5 if (idx == 0 and len(clauses) > 1) else (1.4 if idx > 0 else 1.0)
            score = 0.0

            # Emojis
            for em, val in cls.EMOJIS.items():
                if em in clause:
                    score += val * clause.count(em)

            # Tokenize words
            clean_clause = re.sub(r'[^a-zA-Z0-9\s\']', ' ', clause.lower())
            words = [w.replace("'", '') for w in clean_clause.split() if w]

            negate_window = 0
            intensity_mod = 1.0

            for i, w in enumerate(words):
                if w in cls.NEGATORS or (i > 0 and f"{words[i-1]} {w}" in cls.NEGATORS):
                    negate_window = 3
                    continue
                if w in cls.INTENSIFIERS:
                    intensity_mod = cls.INTENSIFIERS[w]
                    continue
                if w in cls.DIMINISHERS:
                    intensity_mod = cls.DIMINISHERS[w]
                    continue

                w_score = 0.0
                matched = False
                for cand in cls._stem_variants(w):
                    if cand in cls.POSITIVE_WORDS:
                        w_score = cls.POSITIVE_WORDS[cand]
                        matched = True
                        break
                    elif cand in cls.NEGATIVE_WORDS:
                        w_score = cls.NEGATIVE_WORDS[cand]
                        matched = True
                        break

                if matched:
                    w_score *= intensity_mod
                    if negate_window > 0:
                        w_score = -w_score * 0.75
                    score += w_score
                    intensity_mod = 1.0

                if negate_window > 0:
                    negate_window -= 1

            # Exclamation boost
            if '!' in clause:
                ex_count = min(3, clause.count('!'))
                if score > 0:
                    score += ex_count * 0.4
                elif score < 0:
                    score -= ex_count * 0.4

            clause_scores.append(score * weight)

        raw_score = sum(clause_scores)

        # Semantic TF-IDF Vector Anchoring
        try:
            cls._init_vectorizer()
            if cls._vectorizer:
                tx = cls._vectorizer.transform([text])
                sims = cosine_similarity(tx, cls._proto_matrix)[0]
                pos_sim, neg_sim = float(sims[0]), float(sims[1])
                vector_delta = (pos_sim - neg_sim) * 4.5
                raw_score += vector_delta
        except Exception:
            pass

        # Compound score normalization into [-1.0, 1.0] (purely derived from semantic NLP analysis)
        denom = math.sqrt(raw_score * raw_score + 10.0)
        compound = raw_score / denom if denom > 0 else 0.0
        compound = max(-1.0, min(1.0, compound))

        positivity_score = (compound + 1.0) / 2.0
        positivity_score = max(0.02, min(0.98, positivity_score))
        negativity_score = 1.0 - positivity_score

        positivity_pct = int(round(positivity_score * 100))
        negativity_pct = 100 - positivity_pct

        if positivity_pct >= 58:
            sentiment = 'positive'
        elif positivity_pct <= 42:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        if positivity_pct >= 75:
            label = 'Strongly Positive'
        elif positivity_pct >= 60:
            label = 'Mostly Positive'
        elif positivity_pct >= 45:
            label = 'Mixed / Balanced'
        elif positivity_pct >= 30:
            label = 'Mostly Critical'
        else:
            label = 'Strongly Critical'

        return {
            'compound': round(compound, 3),
            'positivity_score': round(positivity_score, 3),
            'negativity_score': round(negativity_score, 3),
            'positivity_pct': positivity_pct,
            'negativity_pct': negativity_pct,
            'sentiment': sentiment,
            'label': label,
        }


def aggregate_comments_sentiment(comments: list, fallback_text: str = "") -> dict:
    """
    Aggregates comment sentiments into overall positivity and negativity percentages,
    sentiment label, and metrics.
    """
    if not comments:
        if fallback_text:
            analysis = SemanticSentimentAnalyzer.analyze(fallback_text)
            return {
                'positivity_pct': analysis['positivity_pct'],
                'negativity_pct': analysis['negativity_pct'],
                'total_comments': 0,
                'sentiment': analysis['sentiment'],
                'label': analysis['label'],
                'has_comments': False,
            }
        return {
            'positivity_pct': 50,
            'negativity_pct': 50,
            'total_comments': 0,
            'sentiment': 'neutral',
            'label': 'No Comments Yet',
            'has_comments': False,
        }

    pos_scores = [c.get('positivity_score', 0.5) for c in comments]
    avg_pos = sum(pos_scores) / max(1, len(pos_scores))
    positivity_pct = int(round(avg_pos * 100))
    positivity_pct = max(2, min(98, positivity_pct))
    negativity_pct = 100 - positivity_pct

    if positivity_pct >= 58:
        sentiment = 'positive'
    elif positivity_pct <= 42:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    if positivity_pct >= 75:
        label = 'Strongly Positive'
    elif positivity_pct >= 60:
        label = 'Mostly Positive'
    elif positivity_pct >= 45:
        label = 'Mixed / Balanced'
    elif positivity_pct >= 30:
        label = 'Mostly Critical'
    else:
        label = 'Strongly Critical'

    pos_count = sum(1 for c in comments if c.get('sentiment') == 'positive')
    neg_count = sum(1 for c in comments if c.get('sentiment') == 'negative')
    neu_count = len(comments) - pos_count - neg_count

    return {
        'positivity_pct': positivity_pct,
        'negativity_pct': negativity_pct,
        'total_comments': len(comments),
        'positive_count': pos_count,
        'negative_count': neg_count,
        'neutral_count': neu_count,
        'sentiment': sentiment,
        'label': label,
        'has_comments': True,
    }


def get_comments_for_article(article_title: str) -> list:
    """Fetch all comments for an article title from database."""
    article_title = (article_title or '').strip()
    if not article_title:
        return []
    with get_db() as db:
        p = sql_param()
        rows = db.execute(
            f"""
            SELECT id, user_id, article_title, article_url, author_name, avatar_url,
                   content, sentiment, positivity_score, negativity_score, source, rating, created_at
            FROM article_comments
            WHERE LOWER(article_title) = LOWER({p})
            ORDER BY created_at ASC, id ASC
            """,
            (article_title[:240],)
        ).fetchall()
        return [comment_row_to_dict(r) for r in rows]


COMMENT_BOILERPLATE_RE = re.compile(
    r'\b('
    r'leave a (reply|comment)|post a comment|sign in to (comment|reply)|'
    r'log in to (comment|reply)|must be logged in|all rights reserved|'
    r'cookie policy|privacy policy|terms of service|subscribe for|'
    r'read more|load more comments|view all \d+ comments|add your comment|'
    r'related articles?|trending stories|recommended for you|copyright'
    r')\b',
    re.IGNORECASE
)


def extract_comments_from_article_html(html_text: str, source_name: str = "", article_url: str = "") -> list:
    """
    Extracts genuine reader/people feedback from an article's web page if it has a comment section
    (e.g., Schema.org UserComments, WordPress, Coral, OpenWeb, Spot.IM, or standard HTML comment blocks).
    """
    if not html_text or len(html_text) < 100:
        return []

    comments = []
    seen = set()
    src = (source_name or '').strip()

    # 1. JSON-LD structured comments (@type: Comment / UserComments)
    try:
        json_ld_matches = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html_text, re.DOTALL | re.IGNORECASE)
        for block in json_ld_matches:
            try:
                data = json.loads(block.strip())
                items = data if isinstance(data, list) else [data]
                for item in items:
                    if isinstance(item, dict):
                        c_list = item.get('comment') or item.get('commentList') or []
                        if isinstance(c_list, dict):
                            c_list = [c_list]
                        if item.get('@type') in ('Comment', 'UserComments'):
                            c_list.append(item)

                        for c in c_list:
                            if isinstance(c, dict):
                                text = clean_html(c.get('text') or c.get('description') or c.get('articleBody') or '').strip()
                                author = c.get('author')
                                author_name = ""
                                if isinstance(author, dict):
                                    author_name = author.get('name') or author.get('alternateName') or ''
                                elif isinstance(author, str):
                                    author_name = author
                                author_name = clean_html(author_name or (f"Reader via {src}" if src else "Community Reader")).strip()

                                if text and len(text) >= 15 and len(text) <= 1200:
                                    norm_key = text[:80].lower()
                                    if norm_key not in seen and not COMMENT_BOILERPLATE_RE.search(text):
                                        seen.add(norm_key)
                                        analysis = SemanticSentimentAnalyzer.analyze(text)
                                        comments.append({
                                            'author_name': author_name[:60] or (f"Reader via {src}" if src else "Community Reader"),
                                            'content': text[:800],
                                            'sentiment': analysis['sentiment'],
                                            'positivity_score': analysis['positivity_score'],
                                            'negativity_score': analysis['negativity_score'],
                                            'source': f"via {src}" if src else "Article Comment",
                                            'article_url': article_url or '',
                                        })
            except Exception:
                pass
    except Exception:
        pass

    # 2. HTML comment blocks (WordPress, Coral, Spot.IM, OpenWeb, Custom CMS)
    if len(comments) < 5:
        comment_block_re = re.compile(
            r'<(?:article|li|div|section)\b[^>]*class=["\'][^"\']*\b(?:comment|comment-body|comment-item|user-comment|reader-comment|comments__item|comment__wrap|wp-block-comment)\b[^"\']*["\'][^>]*>(.*?)</(?:article|li|div|section)>',
            re.DOTALL | re.IGNORECASE
        )
        for match in comment_block_re.finditer(html_text):
            block_html = match.group(1)
            text_match = re.search(
                r'<(?:div|p|span|blockquote)\b[^>]*class=["\'][^"\']*\b(?:comment-content|comment-body|comment-text|comment-message|user-comment-body|comment__text|content)\b[^"\']*["\'][^>]*>(.*?)</(?:div|p|span|blockquote)>',
                block_html,
                re.DOTALL | re.IGNORECASE
            )
            raw_text = text_match.group(1) if text_match else block_html
            text = clean_html(raw_text).strip()

            author_match = re.search(
                r'<(?:span|a|div|strong|cite|h[4-6])\b[^>]*class=["\'][^"\']*\b(?:comment-author|comment__author|user-name|author-name|commenter-name|fn)\b[^"\']*["\'][^>]*>(.*?)</(?:span|a|div|strong|cite|h[4-6])>',
                block_html,
                re.DOTALL | re.IGNORECASE
            )
            author_name = clean_html(author_match.group(1)).strip() if author_match else (f"Reader via {src}" if src else "Community Reader")

            if text and len(text) >= 15 and len(text) <= 1200:
                if not COMMENT_BOILERPLATE_RE.search(text):
                    if not text.startswith(('Day after', 'Lok Sabha', 'Supreme Court', 'Reporting by')):
                        norm_key = text[:80].lower()
                        if norm_key not in seen:
                            seen.add(norm_key)
                            analysis = SemanticSentimentAnalyzer.analyze(text)
                            comments.append({
                                'author_name': author_name[:60] or (f"Reader via {src}" if src else "Community Reader"),
                                'content': text[:800],
                                'sentiment': analysis['sentiment'],
                                'positivity_score': analysis['positivity_score'],
                                'negativity_score': analysis['negativity_score'],
                                'source': f"via {src}" if src else "Article Comment",
                                'article_url': article_url or '',
                            })
            if len(comments) >= 8:
                break

    return comments[:8]


def fetch_and_store_rss_comments(article_title: str, articles: list = None) -> list:
    """
    Fetches real reader comments from the comment sections of fetched articles or their RSS comment feeds.
    Returns only genuine reader comments (no fabricated reporter articles).
    """
    article_title = (article_title or '').strip()
    if not article_title:
        return []

    existing = get_comments_for_article(article_title)
    if existing:
        return existing

    new_comments = []
    articles = articles or []

    # 1. Direct comment RSS (wfw:commentRss or <comments> feed)
    for a in articles:
        comment_rss = a.get('wfw_commentrss') or a.get('comments_url') or ''
        if comment_rss and comment_rss.startswith('http'):
            try:
                cfeed = feedparser.parse(comment_rss)
                if cfeed and getattr(cfeed, 'entries', None):
                    for ce in cfeed.entries[:5]:
                        c_text = clean_html(
                            ce.get('summary')
                            or ce.get('description')
                            or (ce.get('content', [{}])[0].get('value') if ce.get('content') else '')
                            or ''
                        ).strip()
                        c_author = ce.get('author') or ce.get('dc_creator') or (f"Reader via {a.get('source')}" if a.get('source') else "RSS Reader")
                        if len(c_text) >= 15 and not COMMENT_BOILERPLATE_RE.search(c_text):
                            analysis = SemanticSentimentAnalyzer.analyze(c_text)
                            new_comments.append({
                                'user_id': None,
                                'article_title': article_title[:240],
                                'article_url': a.get('url', ''),
                                'author_name': str(c_author)[:60],
                                'avatar_url': '',
                                'content': c_text[:1000],
                                'sentiment': analysis['sentiment'],
                                'positivity_score': analysis['positivity_score'],
                                'negativity_score': analysis['negativity_score'],
                                'source': f"via {a.get('source') or 'RSS'}",
                                'rating': 0,
                            })
            except Exception as e:
                app.logger.warning("Failed parsing comment RSS %s: %s", comment_rss, e)

    # 2. Extract real comment section feedback from fetched article web pages
    if len(new_comments) < 5 and articles:
        for a in articles[:3]:
            url = a.get('url', '')
            if not url:
                continue
            src = a.get('source', '')
            dest_url = url
            if 'news.google.com' in url:
                try:
                    from googlenewsdecoder import gnewsdecoder
                    res = gnewsdecoder(url)
                    if res.get('status') and res.get('decoded_url'):
                        dest_url = res.get('decoded_url')
                except Exception:
                    pass

            try:
                resp = requests.get(dest_url, headers=HEADERS, timeout=4)
                if resp.status_code == 200:
                    html_content = resp.text
                    extracted = extract_comments_from_article_html(html_content, source_name=src, article_url=dest_url)
                    for ec in extracted:
                        new_comments.append({
                            'user_id': None,
                            'article_title': article_title[:240],
                            'article_url': ec.get('article_url', dest_url),
                            'author_name': ec.get('author_name', f"Reader via {src}"),
                            'avatar_url': '',
                            'content': ec['content'][:1000],
                            'sentiment': ec['sentiment'],
                            'positivity_score': ec['positivity_score'],
                            'negativity_score': ec['negativity_score'],
                            'source': ec.get('source', f"via {src}"),
                            'rating': 0,
                        })
                        if len(new_comments) >= 8:
                            break
            except Exception:
                pass
            if len(new_comments) >= 5:
                break

    # Save any genuine comments found to database
    if new_comments:
        with get_db() as db:
            p = sql_param()
            for c in new_comments:
                db.execute(
                    f"""
                    INSERT INTO article_comments
                        (user_id, article_title, article_url, author_name, avatar_url,
                         content, sentiment, positivity_score, negativity_score, source, rating)
                    VALUES ({p}, {p}, {p}, {p}, {p}, {p}, {p}, {p}, {p}, {p}, {p})
                    """,
                    (
                        c.get('user_id'),
                        c['article_title'],
                        c.get('article_url', ''),
                        c.get('author_name', 'Reader'),
                        c.get('avatar_url', ''),
                        c['content'],
                        c['sentiment'],
                        c['positivity_score'],
                        c['negativity_score'],
                        c.get('source', 'Article Comment'),
                        c.get('rating', 0),
                    )
                )

    return get_comments_for_article(article_title)


def get_cluster_sentiment(cluster_title: str, arts: list = None, consensus_summary: str = "") -> dict:
    """
    Returns aggregate sentiment {positivity_pct, negativity_pct, total_comments, label, sentiment}
    for a cluster on the homefeed.
    """
    cluster_title = (cluster_title or '').strip()
    if not cluster_title:
        return {
            'positivity_pct': 50,
            'negativity_pct': 50,
            'total_comments': 0,
            'sentiment': 'neutral',
            'label': 'Mixed / Balanced',
            'has_comments': False,
        }

    try:
        comments = get_comments_for_article(cluster_title)
        fallback_text = f"{cluster_title}. {consensus_summary}"
        return aggregate_comments_sentiment(comments, fallback_text=fallback_text)
    except Exception as e:
        app.logger.warning("Error computing cluster sentiment for %s: %s", cluster_title, e)
        fallback_text = f"{cluster_title}. {consensus_summary}"
        analysis = SemanticSentimentAnalyzer.analyze(fallback_text)
        return {
            'positivity_pct': analysis['positivity_pct'],
            'negativity_pct': analysis['negativity_pct'],
            'total_comments': 0,
            'sentiment': analysis['sentiment'],
            'label': analysis['label'],
            'has_comments': False,
        }


def normalize_interest_term(term: str) -> str:
    """Normalize interest term: clean whitespace, strip punctuation noise, clean capitalization."""
    if not term:
        return ""
    t = str(term).strip()
    t = re.sub(r'https?://\S+', '', t)
    t = re.sub(r'[\r\n\t_]+', ' ', t)
    t = re.sub(r'^[^\w#/@]+|[^\w#/@]+$', '', t.strip())
    if not t:
        return ""
    if re.match(r'^r/[A-Za-z0-9_]+$', t, re.I):
        parts = t.split('/')
        return f"r/{parts[1]}"
    if len(t) <= 4 and t.isupper():
        return t
    if t.islower():
        words = [w.capitalize() if len(w) > 2 else w.upper() for w in t.split()]
        t = " ".join(words)
    return t[:60].strip()


def save_user_interest(user_id: int, interest: str, source_type: str = "manual"):
    if not user_id:
        return None
    clean = normalize_interest_term(interest)
    if not clean or len(clean) < 2 or clean.lower() in ("__home__", "home", "all", "news", "undefined", "null", "none"):
        return None
    try:
        with get_db() as db:
            if USE_POSTGRES:
                db.execute(
                    """
                    INSERT INTO user_interests (user_id, interest, source_type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (user_id, interest) DO UPDATE SET created_at = CURRENT_TIMESTAMP
                    """,
                    (user_id, clean, source_type),
                )
            else:
                db.execute(
                    """
                    INSERT INTO user_interests (user_id, interest, source_type)
                    VALUES (?, ?, ?)
                    ON CONFLICT(user_id, interest) DO UPDATE SET created_at = CURRENT_TIMESTAMP
                    """,
                    (user_id, clean, source_type),
                )
        return clean
    except Exception as e:
        app.logger.warning("Failed to save user interest: %s", e)
        return None


def get_user_interests(user_id: int):
    if not user_id:
        return []
    with get_db() as db:
        rows = db.execute(
            f"""
            SELECT id, interest, source_type, created_at
            FROM user_interests
            WHERE user_id = {sql_param()}
            ORDER BY created_at DESC, id DESC
            LIMIT 100
            """,
            (user_id,),
        ).fetchall()
        result = []
        for r in rows:
            created_at = r["created_at"]
            if hasattr(created_at, "isoformat"):
                created_at = created_at.isoformat()
            elif created_at is not None:
                created_at = str(created_at)
            result.append({
                "id": r["id"],
                "interest": r["interest"],
                "source_type": r["source_type"],
                "created_at": created_at,
            })
        return result


def delete_user_interest(user_id: int, interest_id: int = None, interest_name: str = None):
    if not user_id:
        return False
    with get_db() as db:
        if interest_id is not None:
            db.execute(
                f"DELETE FROM user_interests WHERE user_id = {sql_param()} AND id = {sql_param()}",
                (user_id, interest_id),
            )
        elif interest_name:
            db.execute(
                f"DELETE FROM user_interests WHERE user_id = {sql_param()} AND LOWER(interest) = LOWER({sql_param()})",
                (user_id, str(interest_name).strip()),
            )
    return True


def clear_user_interests(user_id: int):
    if not user_id:
        return False
    with get_db() as db:
        db.execute(
            f"DELETE FROM user_interests WHERE user_id = {sql_param()}",
            (user_id,),
        )
    return True


CATEGORY_TAXONOMY = {
    "Technology": [
        "tech", "technology", "artificial intelligence", "ai", "machine learning", "software", "hardware",
        "apple", "google", "microsoft", "meta", "nvidia", "openai", "semiconductor", "semiconductors",
        "chip", "chips", "cybersecurity", "cyber", "hack", "hacker", "crypto", "bitcoin", "blockchain",
        "smartphone", "smartphones", "iphone", "ipad", "android", "gadget", "gadgets", "app", "apps",
        "robot", "robots", "robotics", "quantum", "computing", "cloud", "algorithm", "startup", "startups",
        "internet", "browser", "windows", "linux", "metaverse", "chatgpt", "deepseek", "anthropic",
        "data", "database", "neural", "gpu", "server"
    ],
    "Business": [
        "business", "economy", "economic", "economics", "market", "markets", "stock", "stocks", "wall street",
        "nasdaq", "dow jones", "s&p", "finance", "financial", "banking", "bank", "banks", "federal reserve",
        "fed", "inflation", "recession", "gdp", "earnings", "revenue", "profit", "quarterly", "investor",
        "investors", "investment", "investments", "shares", "trade", "tariff", "tariffs", "ceo", "merger",
        "acquisition", "deal", "commerce", "retail", "real estate", "housing", "mortgage", "fund",
        "venture capital", "corporate", "corporation", "sales", "export", "import"
    ],
    "Sports": [
        "sport", "sports", "football", "soccer", "nfl", "nba", "mlb", "nhl", "premier league", "champions league",
        "la liga", "serie a", "bundesliga", "fifa", "uefa", "basketball", "baseball", "tennis", "cricket",
        "golf", "olympics", "olympic", "f1", "formula 1", "racing", "grand prix", "ufc", "mma", "boxing",
        "rugby", "athlete", "athletes", "coach", "tournament", "championship", "playoffs", "stadium",
        "match", "goal", "score", "touchdown", "quarterback", "super bowl", "world cup", "wimbledon", "club"
    ],
    "Health": [
        "health", "healthy", "medicine", "medical", "disease", "diseases", "virus", "viral", "vaccine",
        "vaccines", "vaccination", "fda", "cdc", "who", "cancer", "tumor", "diabetes", "heart", "cardiac",
        "mental health", "depression", "anxiety", "therapy", "diet", "nutrition", "fitness", "workout",
        "hospital", "hospitals", "doctor", "doctors", "patient", "patients", "clinical", "trial", "trials",
        "pharma", "pharmaceutical", "drug", "drugs", "treatment", "treatments", "cure", "surgery",
        "pandemic", "epidemic", "wellness", "physician", "healthcare", "brain", "syndrome"
    ],
    "Science": [
        "science", "scientific", "scientist", "scientists", "space", "nasa", "esa", "spacex", "astronomy",
        "astronomer", "telescope", "james webb", "hubble", "mars", "moon", "lunar", "orbit", "planet",
        "planets", "solar system", "galaxy", "universe", "cosmos", "physics", "physicist", "quantum",
        "biology", "biologist", "genetics", "dna", "crispr", "evolution", "fossil", "dinosaur", "climate change",
        "global warming", "environment", "ecology", "ocean", "geology", "earthquake", "volcano", "asteroid"
    ],
    "Culture": [
        "culture", "entertainment", "movie", "movies", "film", "films", "cinema", "actor", "actors",
        "actress", "hollywood", "celebrity", "celebrities", "music", "musical", "album", "song", "songs",
        "singer", "artist", "artists", "concert", "tour", "grammy", "grammys", "oscar", "oscars", "emmy",
        "emmys", "tv", "television", "series", "season", "trailer", "streaming", "netflix", "disney",
        "hbo", "spotify", "game", "games", "gaming", "playstation", "xbox", "nintendo", "steam", "book",
        "books", "author", "novel", "art", "museum", "exhibition", "fashion", "runway", "broadway", "theater"
    ],
    "Politics": [
        "politics", "political", "politician", "politicians", "election", "elections", "vote", "voters",
        "voting", "ballot", "democrat", "democrats", "republican", "republicans", "gop", "biden", "trump",
        "white house", "congress", "senate", "senator", "senators", "house of representatives", "parliament",
        "prime minister", "president", "presidential", "governor", "mayor", "legislation", "bill", "law",
        "supreme court", "justice", "judge", "attorney general", "doj", "sanction", "sanctions", "diplomacy",
        "diplomat", "treaty", "ambassador", "foreign policy", "geopolitics", "war", "military", "defense",
        "pentagon", "nato", "united nations", "un"
    ]
}


def classify_article_category(title: str, article_text: str = "", sources: list = None) -> str:
    """Determine the topic category of an article instead of using its raw title."""
    combined = ((title or "") + " ") * 4 + ((article_text or "")[:1500] + " ")
    if sources:
        combined += " ".join((s.get("title") or "") for s in sources[:6])
    combined_lower = combined.lower()

    scores = {}
    for cat, keywords in CATEGORY_TAXONOMY.items():
        score = 0
        for kw in keywords:
            if " " in kw:
                if kw in combined_lower:
                    score += 3
            else:
                matches = len(re.findall(r'\b' + re.escape(kw) + r'\b', combined_lower))
                score += matches
        if score > 0:
            scores[cat] = score

    if scores:
        best_cat = max(scores, key=scores.get)
        if scores[best_cat] >= 1:
            return best_cat

    for key in ("technology", "business", "sports", "health", "culture", "science", "politics", "world"):
        if key in combined_lower:
            return key.title()

    return "General News"


def save_interests_from_roundup(user_id: int, title: str, sources: list = None, article_text: str = ""):
    """Automatically record the category of an article when a user reads a roundup."""
    if not user_id:
        return
    category = classify_article_category(title, article_text=article_text, sources=sources)
    if category and category != "General News":
        save_user_interest(user_id, category, source_type="read")


def save_article_history(title, article_text, image_url, sources):
    user = current_user()
    if user is None or not article_text:
        return

    # Automatically extract image from sources if not provided directly
    if not image_url and sources:
        for s in sources:
            img = s.get("image") or s.get("image_url") or s.get("cluster_image")
            if img and is_valid_img(img):
                image_url = img
                break

    # Automatically save user interests from the read roundup
    try:
        save_interests_from_roundup(user["id"], title, sources=sources, article_text=article_text)
    except Exception as e:
        app.logger.warning("save_interests_from_roundup failed: %s", e)

    cleaned_sources = [
        {
            "title": (src.get("title") or "").strip(),
            "url": (src.get("url") or "").strip(),
        }
        for src in sources
        if src.get("url")
    ][:12]

    with get_db() as db:
        if USE_POSTGRES:
            db.execute(
                """
                INSERT INTO article_history
                    (user_id, title, article_text, image_url, source_count, sources_json)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    user["id"],
                    title[:240],
                    article_text,
                    image_url,
                    len(cleaned_sources),
                    json.dumps(cleaned_sources),
                ),
            )
            db.execute(
                """
                DELETE FROM article_history
                WHERE user_id = %s
                  AND id NOT IN (
                    SELECT id FROM article_history
                    WHERE user_id = %s
                    ORDER BY created_at DESC, id DESC
                    LIMIT 10
                  )
                """,
                (user["id"], user["id"]),
            )
        else:
            db.execute(
                """
                INSERT INTO article_history
                    (user_id, title, article_text, image_url, source_count, sources_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user["id"],
                    title[:240],
                    article_text,
                    image_url,
                    len(cleaned_sources),
                    json.dumps(cleaned_sources),
                ),
            )
            db.execute(
                """
                DELETE FROM article_history
                WHERE user_id = ?
                  AND id NOT IN (
                    SELECT id FROM article_history
                    WHERE user_id = ?
                    ORDER BY created_at DESC, id DESC
                    LIMIT 10
                  )
                """,
                (user["id"], user["id"]),
            )


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if current_user() is not None:
            return view(*args, **kwargs)
        if request.path.startswith("/api/"):
            return jsonify({"error": "Authentication required"}), 401
        return redirect(url_for("login", next=request.path))

    return wrapped_view

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

import threading

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

_domain_image_cache = {}
_fallback_image_cache = {}
_wiki_image_cache = {}

HOME_QUERY = "__home__"

_embedder_lock = threading.Lock()
_embedder = None
def get_embedder():
    global _embedder
    if _embedder is None:
        with _embedder_lock:
            if _embedder is None:
                try:
                    from sentence_transformers import SentenceTransformer
                    print("  Loading MiniLM model...")
                    _embedder = SentenceTransformer('all-MiniLM-L6-v2')
                    print("  MiniLM ready.")
                except (ImportError, OSError, RuntimeError, ValueError, Exception) as e:
                    print(f"  MiniLM unavailable ({e}), will fall back to TF-IDF.")
                    _embedder = False
    return _embedder if _embedder else None


def embed(texts):
    model = get_embedder()
    if model is None:
        return None
    try:
        with _embedder_lock:
            vecs = model.encode(texts, batch_size=64, show_progress_bar=False,
                                convert_to_numpy=True)
            return normalize(vecs)
    except (RuntimeError, ValueError, Exception) as e:
        print(f"  embed() error: {e}")
        return None


def clean_html(raw_html):
    text = re.sub(r'<.*?>', '', raw_html)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def json_safe(value):
    if value is None:
        return None
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, np.generic):
        return json_safe(value.item())
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return value


BOILERPLATE_RE = re.compile(
    r'\b('
    r'go to the .* home page|switch site|toggle (social menu|dark mode|search|search form)|'
    r'search for:|submit|forums|store|podcasts|privacy|about|'
    r'expand close comments|close comments|check out .* on youtube|'
    r'author |guides news author|related articles?|read more|'
    r'ad-container|adsbygoogle|newsletter|sign up|subscribe|'
    r'all rights reserved|cookie|terms of use'
    r')\b',
    re.IGNORECASE
)

ARTICLE_CONTAINER_RE = re.compile(
    r'<(?P<tag>article|main|section|div)\b(?P<attrs>[^>]*)>(?P<body>.*?)</(?P=tag)>',
    re.DOTALL | re.IGNORECASE
)


def is_boilerplate_text(text):
    if not text:
        return True
    if BOILERPLATE_RE.search(text):
        return True

    words = re.findall(r'[A-Za-z0-9]+', text)
    if len(words) < 8:
        return True

    lower = text.lower()
    nav_hits = sum(1 for token in (
        'iphone', 'ipad', 'macbook', 'apple watch', 'forums', 'store',
        'podcast', 'toggle', 'search', 'privacy', 'comments'
    ) if token in lower)
    if nav_hits >= 4:
        return True

    if len(text) > 450 and text.count('.') <= 1:
        return True

    return False


def strip_page_chrome(raw):
    raw = re.sub(r'<(script|style|noscript|svg|iframe|form|button|nav|header|footer|aside)[^>]*>.*?</\1>',
                 ' ', raw, flags=re.DOTALL | re.IGNORECASE)
    raw = re.sub(r'<[^>]+class=["\'][^"\']*(?:menu|nav|footer|header|sidebar|comment|ad-|advert|newsletter|related|share|social)[^"\']*["\'][^>]*>.*?</[^>]+>',
                 ' ', raw, flags=re.DOTALL | re.IGNORECASE)
    return raw


def likely_article_html(raw):
    candidates = []
    for match in ARTICLE_CONTAINER_RE.finditer(raw):
        attrs = match.group('attrs') or ''
        body = match.group('body') or ''
        marker = f"{match.group('tag')} {attrs}".lower()
        score = len(re.findall(r'<p\b', body, re.IGNORECASE)) * 100 + len(clean_html(body))
        if re.search(r'article|story|entry-content|post-content|article-content|main-content|content', marker):
            score += 2000
        if re.search(r'nav|menu|footer|header|sidebar|comment|related|advert|ad-', marker):
            score -= 3000
        if score > 0:
            candidates.append((score, body))

    if not candidates:
        return raw
    return max(candidates, key=lambda item: item[0])[1]


def extract_clean_paragraphs(raw):
    raw = strip_page_chrome(raw)
    article_html = likely_article_html(raw)
    article_html = strip_page_chrome(article_html)
    paras = re.findall(r'<p\b[^>]*>(.*?)</p>', article_html, re.DOTALL | re.IGNORECASE)

    cleaned = []
    seen = set()
    for para in paras:
        if re.search(r'<(figcaption|caption|time|address)\b', para, re.IGNORECASE):
            continue
        text = clean_html(para)
        text = re.sub(r'\s+', ' ', text).strip()
        if is_boilerplate_text(text):
            continue
        key = re.sub(r'[^a-z0-9]', '', text.lower())[:90]
        if key and key not in seen:
            cleaned.append(text)
            seen.add(key)

    return cleaned


def is_useful_sentence(sentence):
    if not sentence or is_boilerplate_text(sentence):
        return False
    if len(sentence) < 35 or len(sentence) > 520:
        return False
    if re.search(r'\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}', sentence):
        return False
    if re.search(r'\b(updated:|published:|photo by|getty images|reuters/|ap photo|all rights reserved|read more|advertisement|click here)\b', sentence, re.IGNORECASE):
        return False
    if len(re.findall(r'[A-Z][A-Za-z0-9+@.-]{1,}', sentence)) > 18:
        return False
    return True


def decode_bing_url(url):
    if 'bing.com' in url and 'url=' in url:
        m = re.search(r'[&?]url=([^&]+)', url)
        if m:
            return urllib.parse.unquote(m.group(1))
    return url


def extract_publisher(title):
    if not title or not isinstance(title, str):
        return None
    parts = title.rsplit(' - ', 1)
    if len(parts) == 2:
        return parts[1].strip()
    return None


def publisher_to_domain_name(publisher):
    if not publisher:
        return ''
    p = publisher.lower().strip()
    p = re.sub(r'\b(news|the|online|digital|media|times|post|daily|weekly|report|wire)\b', '', p).strip()
    p = re.sub(r'[^a-z0-9]', '', p)
    if p:
        return f"{p}.com"
    return ''


def hostname_from_url(url):
    try:
        host = urllib.parse.urlparse(url).hostname or ''
        return host.replace('www.', '')
    except Exception:
        return ''


def extract_feed_source(e):
    title = (e.get('title') or '').strip()
    source_name = ''
    source_url = ''

    if hasattr(e, 'source'):
        s_obj = e.source
        if isinstance(s_obj, dict):
            source_name = s_obj.get('title') or s_obj.get('value') or ''
            source_url = s_obj.get('href') or s_obj.get('url') or ''
        else:
            source_name = getattr(s_obj, 'title', None) or getattr(s_obj, 'value', None) or ''
            source_url = getattr(s_obj, 'href', None) or getattr(s_obj, 'url', None) or ''

    if not source_name and title:
        source_name = extract_publisher(title) or ''

    source_name = (source_name or '').strip()
    source_url = (source_url or '').strip()

    if source_name.lower() in ('google news', 'news.google.com') and source_url:
        source_name = hostname_from_url(source_url) or source_name

    domain = hostname_from_url(source_url) if source_url else ''
    if not domain and source_name:
        domain = publisher_to_domain_name(source_name)

    return source_name or domain or 'News', source_url, domain


def get_publisher_image(publisher, entry):
    source_url = None
    if hasattr(entry, 'source') and hasattr(entry.source, 'href'):
        source_url = entry.source.href
    if hasattr(entry, 'source') and isinstance(entry.source, dict):
        source_url = entry.source.get('href') or entry.source.get('url')

    if source_url and source_url not in _domain_image_cache:
        img = scrape_og_image(source_url)
        _domain_image_cache[source_url] = img
        return img
    elif source_url:
        return _domain_image_cache[source_url]

    return None


def scrape_og_image(url):
    if not url or not url.startswith('http'):
        return None

    import random
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    ]
    hdrs = {
        **HEADERS,
        "User-Agent": random.choice(agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        resp = requests.get(url, headers=hdrs, timeout=8,
                            allow_redirects=True, stream=True)
        chunk = b""
        for piece in resp.iter_content(8192):
            chunk += piece
            if len(chunk) >= 50000:
                break
        resp.close()

        if resp.status_code not in (200, 203):
            return None

        if 'google.com' in resp.url:
            return None

        text = chunk.decode("utf-8", errors="ignore")

        for pat in [
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\'>]+)',
            r'<meta[^>]+content=["\']([^"\'>]+)["\'][^>]+property=["\']og:image',
            r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\'>]+)',
            r'<meta[^>]+content=["\']([^"\'>]+)["\'][^>]+name=["\']twitter:image',
            r'<meta[^>]+property=["\']og:image:url["\'][^>]+content=["\']([^"\'>]+)',
        ]:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                img = m.group(1).strip()
                if img.startswith('http') and not img.endswith(('.svg', '.gif')):
                    return img

        jld = re.search(
            r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            text, re.DOTALL | re.IGNORECASE)
        if jld:
            m = re.search(r'"image"\s*:\s*["\']?(https://[^"\'\s,}{\\]]+)', jld.group(1))
            if m:
                img = m.group(1).strip()
                if img.startswith('http') and not img.endswith(('.svg', '.gif')):
                    return img

        for img_tag in re.finditer(r'<img[^>]+src=["\']([^"\'>]+)["\']', text, re.IGNORECASE):
            src = img_tag.group(1).strip()
            if (src.startswith('http')
                    and any(ext in src.lower() for ext in ('.jpg', '.jpeg', '.png', '.webp'))
                    and not any(x in src.lower() for x in ('logo', 'icon', 'avatar', '1x1', 'pixel', 'spacer'))):
                return src

    except requests.RequestException:
        return None
    return None


# ── Local fallback images ─────────────────────────────────────────────────────
FALLBACK_STOPWORDS = {
    "a", "an", "the", "in", "on", "at", "to", "of", "and", "or", "but",
    "for", "with", "by", "from", "as", "is", "are", "was", "were", "be",
    "been", "being", "it", "its", "this", "that", "these", "those", "after",
    "before", "over", "under", "into", "amid", "about", "against", "than",
    "says", "say", "said", "new", "latest", "breaking", "live", "updates",
    "update", "news", "how", "why", "what", "when", "where", "who", "will",
    "may", "could", "would", "should", "can", "more", "most", "top", "big",
    "first", "last", "now", "today", "tomorrow", "yesterday",
}


def stable_index(text, size):
    digest = hashlib.sha256((text or "").encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % size


def fallback_keywords_from_title(title, max_terms=4):
    if not title:
        return ["news"]

    candidates = re.findall(r"[A-Za-z][A-Za-z0-9-]{2,}", title)
    proper_nouns = [
        word.lower()
        for word in candidates
        if word[:1].isupper() and word.lower() not in FALLBACK_STOPWORDS
    ]
    descriptive = [
        word.lower()
        for word in candidates
        if word.lower() not in FALLBACK_STOPWORDS
    ]

    keywords = []
    for word in proper_nouns + descriptive:
        word = word.strip("-").lower()
        if word and word not in keywords:
            keywords.append(word)
        if len(keywords) >= max_terms:
            break

    return keywords if keywords else ["news"]


def fallback_keywords_for_image(title, query=""):
    title_terms = fallback_keywords_from_title(title, max_terms=5)
    query_terms = []
    if query and query != HOME_QUERY:
        query_terms = fallback_keywords_from_title(query, max_terms=3)

    keywords = []
    for word in query_terms + title_terms:
        word = word.strip().lower()
        if word and word != "news" and word not in keywords:
            keywords.append(word)
        if len(keywords) >= 5:
            break

    return keywords if keywords else ["news"]


FALLBACK_TOPIC_KEYWORDS = {
    "games": {
        "capcom", "resident", "evil", "requiem", "monster", "hunter", "game",
        "games", "gaming", "console", "playstation", "xbox", "nintendo",
        "steam", "esports",
    },
    "technology": {
        "technology", "tech", "software", "ai", "artificial", "intelligence",
        "chip", "chips", "cyber", "security", "data", "app", "google",
        "apple", "microsoft", "openai", "tesla", "spacex",
    },
    "business": {
        "business", "economy", "market", "markets", "stock", "stocks",
        "finance", "bank", "banks", "trade", "inflation", "tariff",
        "company", "earnings", "sales", "quarterly", "industry",
    },
    "sports": {
        "sport", "sports", "football", "soccer", "basketball", "baseball",
        "cricket", "tennis", "golf", "match", "league", "nba", "nfl",
        "mlb", "ipl", "fifa", "olympic", "olympics",
    },
    "health": {
        "health", "medical", "medicine", "hospital", "doctor", "doctors",
        "vaccine", "covid", "disease", "drug", "fda", "wellness",
        "mental", "cancer", "virus",
    },
    "science": {
        "science", "research", "space", "nasa", "climate", "weather",
        "study", "scientists", "physics", "biology", "planet", "moon",
        "mars", "earthquake",
    },
    "culture": {
        "culture", "arts", "film", "movie", "movies", "music", "album",
        "book", "books", "theater", "festival", "celebrity", "hollywood",
        "streaming", "netflix",
    },
}

FALLBACK_PALETTES = {
    "games":     ("#171717", "#86efac", "#f97316", "#f8fafc"),
    "technology":("#071013", "#22d3ee", "#facc15", "#f8fafc"),
    "business":  ("#111827", "#a7f3d0", "#f59e0b", "#f9fafb"),
    "sports":    ("#102a43", "#fef08a", "#ef4444", "#f8fafc"),
    "health":    ("#f7f3ea", "#f97316", "#111827", "#1f2937"),
    "science":   ("#0f172a", "#93c5fd", "#fb7185", "#f8fafc"),
    "culture":   ("#231f20", "#f9a8d4", "#fde68a", "#fff7ed"),
    "general":   ("#f4f1e8", "#111827", "#8fa2ff", "#111827"),
}


def fallback_topic_from_keywords(keywords):
    words = set(keywords)
    for topic, topic_words in FALLBACK_TOPIC_KEYWORDS.items():
        if words & topic_words:
            return topic
    return "general"


TOPIC_FALLBACK_SEARCH_TERMS = {
    "technology": "Artificial intelligence technology",
    "business": "Stock market and global economy",
    "space": "Outer space and astronomy",
    "politics": "Politics and government",
    "sports": "Sports competition stadium",
    "science": "Earth science and nature",
    "health": "Medical healthcare medicine",
}


def extract_wiki_search_candidates(title, query=""):
    candidates = []
    clean_title = re.sub(r'\s+', ' ', title or '').strip()
    clean_title = re.sub(r'\s*-\s*[^-]{2,40}$', '', clean_title).strip()
    clean_title_no_punct = re.sub(r'[\'"`:;?!]', '', clean_title)

    # 1. Multi-word proper names/entities (e.g. "Charles Leclerc", "European Central Bank", "Real Madrid")
    entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', clean_title_no_punct)
    for e in entities:
        if len(e) > 3 and e.lower() not in ("the new", "breaking news", "live updates", "first time"):
            candidates.append(e)

    # 2. Prominent single capitalized words / acronyms (e.g. "Nvidia", "NASA", "Boeing", "Ferrari")
    prominent = re.findall(r'\b[A-Z][A-Za-z0-9]{2,}\b', clean_title_no_punct)
    stop_words = {"The", "And", "For", "With", "After", "Before", "Over", "Under", "Says", "Report", "Reports", "Update", "Updates", "Watch", "Live", "What", "When", "Where", "Why", "How", "Releases", "Surpasses", "Wins"}
    for p in prominent:
        if p not in stop_words and p not in candidates:
            candidates.append(p)

    # 3. Clean full headline or query
    if query and query != "__home__":
        candidates.insert(0, query.strip())
    if clean_title:
        candidates.append(clean_title[:80])

    # 4. Inferred topic fallback
    title_lower = (title or "").lower()
    for topic, keywords in FALLBACK_TOPIC_KEYWORDS.items():
        if any(k in title_lower for k in keywords):
            if topic in TOPIC_FALLBACK_SEARCH_TERMS:
                candidates.append(TOPIC_FALLBACK_SEARCH_TERMS[topic])
            break

    return candidates


def fetch_wikipedia_image(title, query=""):
    cache_key = f"{query}|{title}".strip().lower()
    if cache_key in _wiki_image_cache:
        return _wiki_image_cache[cache_key]

    candidates = extract_wiki_search_candidates(title, query=query)
    wiki_headers = {
        "User-Agent": "LacunaNewsApp/1.0 (https://lacuna.app; info@lacuna.app)"
    }
    for term in candidates[:4]:
        try:
            url = (
                f"https://en.wikipedia.org/w/api.php"
                f"?action=query&generator=search&gsrsearch={urllib.parse.quote(term)}"
                f"&gsrlimit=2&prop=pageimages&pithumbsize=800&pilicense=any&format=json"
            )
            resp = requests.get(url, headers=wiki_headers, timeout=3.5)
            if resp.status_code == 200:
                pages = resp.json().get("query", {}).get("pages", {})
                for _, page in sorted(pages.items(), key=lambda x: x[1].get("index", 99)):
                    thumb = page.get("thumbnail", {}).get("source")
                    if thumb and thumb.startswith("https://"):
                        _wiki_image_cache[cache_key] = thumb
                        return thumb
        except Exception:
            continue

    _wiki_image_cache[cache_key] = None
    return None


_og_image_cache = {}

def extract_article_og_image(url):
    if not url or not isinstance(url, str):
        return None
    url = url.strip()
    if url in _og_image_cache:
        return _og_image_cache[url]

    dest_url = url
    if 'news.google.com' in url:
        try:
            from googlenewsdecoder import gnewsdecoder
            res = gnewsdecoder(url)
            if res.get('status') and res.get('decoded_url'):
                dest_url = res.get('decoded_url')
        except Exception:
            pass

    try:
        import random
        agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        ]
        hdrs = {
            "User-Agent": random.choice(agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        resp = requests.get(dest_url, headers=hdrs, timeout=5, stream=True, allow_redirects=True)
        chunk = b""
        for piece in resp.iter_content(8192):
            chunk += piece
            if len(chunk) >= 65536:
                break
        resp.close()
        html_head = chunk.decode('utf-8', errors='ignore')

        m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html_head, re.IGNORECASE)
        if not m:
            m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html_head, re.IGNORECASE)
        if not m:
            m = re.search(r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']', html_head, re.IGNORECASE)
        if not m:
            m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']twitter:image["\']', html_head, re.IGNORECASE)

        if m:
            raw_img = html.unescape(m.group(1).strip())
            img_clean = clean_image_url(raw_img)
            if img_clean:
                _og_image_cache[url] = img_clean
                return img_clean
    except Exception:
        pass

    _og_image_cache[url] = None
    return None


def fallback_image(title, query="", offset=0):
    if not title:
        return None

    cache_key = f"{query}|{title}|{offset}".lower()
    if cache_key in _fallback_image_cache:
        return _fallback_image_cache[cache_key]

    if offset == 0:
        wiki_img = fetch_wikipedia_image(title, query=query)
        if wiki_img:
            _fallback_image_cache[cache_key] = wiki_img
            return wiki_img

    keywords = fallback_keywords_for_image(title, query=query)
    topic = fallback_topic_from_keywords(keywords)
    bg, primary, secondary, text_color = FALLBACK_PALETTES[topic]
    seed = stable_index(f"{query}|{title}|{offset}", 100000)
    label = " ".join(keywords[:3]).upper()
    safe_title = html.escape(title[:72])
    safe_label = html.escape(label)
    x1 = 110 + (seed % 220)
    x2 = 620 + (seed % 260)
    y1 = 130 + (seed % 160)
    y2 = 430 + (seed % 110)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800">
<rect width="1200" height="800" fill="{bg}"/>
<rect x="56" y="56" width="1088" height="688" fill="none" stroke="{primary}" stroke-width="3" opacity=".65"/>
<circle cx="{x1}" cy="{y1}" r="210" fill="{primary}" opacity=".22"/>
<circle cx="{x2}" cy="{y2}" r="260" fill="{secondary}" opacity=".20"/>
<path d="M80 610 C260 520 380 720 560 610 S870 510 1120 620" fill="none" stroke="{primary}" stroke-width="16" opacity=".55"/>
<text x="86" y="124" fill="{text_color}" font-family="Glacial Indifference, Helvetica Neue, Helvetica, Arial, sans-serif" font-size="28" font-weight="700" letter-spacing="4">{safe_label}</text>
<text x="86" y="664" fill="{text_color}" font-family="Glacial Indifference, Helvetica Neue, Helvetica, Arial, sans-serif" font-size="50" font-weight="700">{safe_title}</text>
</svg>"""
    img_url = "data:image/svg+xml;charset=utf-8," + urllib.parse.quote(svg)
    _fallback_image_cache[cache_key] = img_url
    return img_url


def clean_article_title(title):
    if not title:
        return ""
    t = str(title).strip()
    while True:
        cleaned = re.sub(r'\s*[-|–—:]\s*[^-|–—:]{2,50}$', '', t).strip()
        if cleaned == t or len(cleaned) <= 10:
            break
        t = cleaned
    return t


JUNK_PATTERNS = re.compile(
    r'\b('
    r'comic|comics|manga|anime|pokemon|batman|spider-?man|marvel|dc comics|dcu|mcu|superman|x-men|avengers|star wars|star trek|fantastic voyage|lanterns'
    r'|#\d+\s*(selling|ranked|bestsell)'
    r'|best seller|top \d+ (comics|issues|graphic)'
    r'|straw bag|fashion week|spring style|outfit ideas|wardrobe'
    r'|game recap|final score|box score|match preview|lineups? and prediction|injury report'
    r'|vote for|athlete of the week|player of the week|bracketology'
    r'|rumor[s]? and information|jewel thief'
    r'|trailer promises|trailer|teaser|leak|spoilers?|fan theory|box office|easter egg|post-credit'
    r'|streaming now|where to watch|how to watch|on netflix|on hbo|on disney\+|on prime|now streaming'
    r'|deal|deals|discount|coupon|promo|price drop|% off|\$\d+|best buy|amazon deal'
    r'|review|reviews|hands-on|unboxing|first look|buying guide|best \w+ (under|for|to buy)'
    r'|betting|odds|spread|parlay|mock draft|power ranking|fantasy|lineup'
    r'|horoscope|zodiac|outfit|dating|relationship|wedding|spotted with|celebrity romance'
    r'|beta\s+\d|firmware update|patch notes|how to install|how to fix|ios\s+\d|watchos\s+\d'
    r')\b',
    re.IGNORECASE
)

HOME_JUNK_PATTERNS = re.compile(
    r'\b('
    r'review|hands[- ]on|unboxing|first look|tested|impressions'
    r'|public beta|developer beta|\bbeta\s+\d|seed[s]? first|firmware update'
    r'|ios\s+\d+(?:\.\d+)?|ipados\s+\d+(?:\.\d+)?|macos\s+\d+(?:\.\d+)?|watchos\s+\d+(?:\.\d+)?|tvos\s+\d+(?:\.\d+)?'
    r'|vs\.?\s+\w|compared|comparison|benchmark'
    r'|best buy|deal[s]?|discount|coupon|promo|sale|offer|price drop'
    r'|% off|\$\d+|£\d+|€\d+'
    r'|best \w+ (phone|laptop|tablet|headphone|camera|tv|monitor|router|charger|earbuds)'
    r'|top \d+ (phone|laptop|tablet|gadget|product|tool|app|plugin|extension)'
    r'|buying guide|should you buy|worth (buying|it)'
    r'|spec[s]?|specifications|teardown|repairability'
    r'|release date|pre-?order|launch date|now available|ships|shipping'
    r'|(iphone|pixel|galaxy|oneplus|xiaomi|oppo|vivo|tecno|itel|realme|nothing phone)\s+\d'
    r'|(macbook|thinkpad|surface|chromebook|ideapad|zenbook|vivobook|expertbook)\s+\w'
    r'|ceiling light|smart (bulb|plug|switch|display|speaker|home hub)'
    r'|crossbow|airsoft|pellet|fishing rod|golf club|yoga mat'
    r'|reveals he almost directed|just explained why|keeps the dcu|wants to believe|is hiding in plain sight'
    r'|rebooted|director reveals|cast member|season \d+|episode \d+|series finale'
    r')\b',
    re.IGNORECASE
)

HOME_PRIORITY_PATTERNS = re.compile(
    r'\b('
    r'election|vote|voters|congress|senate|house|parliament|president|prime minister|'
    r'white house|supreme court|judge|court|lawsuit|trial|charges|indict|verdict|'
    r'government|policy|bill|law|regulator|sanction|tariff|ceasefire|war|military|'
    r'attack|strike|missile|hostage|peace talks|summit|nato|united nations|'
    r'economy|inflation|interest rate|fed|federal reserve|jobs report|unemployment|'
    r'market[s]?|stocks?|earnings|recession|gdp|oil prices?|'
    r'outbreak|vaccine|hospital|fda|cdc|who|disease|health|'
    r'climate|wildfire|hurricane|flood|earthquake|storm|heat wave|'
    r'ai|artificial intelligence|cybersecurity|data breach|antitrust|merger|'
    r'investigation|corruption|protest|strike|immigration|border|'
    r'death toll|killed|injured|evacuat|emergency'
    r')\b',
    re.IGNORECASE
)

HOME_LOW_VALUE_PATTERNS = re.compile(
    r'\b('
    r'rumor|leak|teaser|trailer|spoiler|episode|box office|streaming now|'
    r'game recap|power ranking|mock draft|lineups?|prediction|odds|'
    r'how to|what to expect|everything we know|things to know|'
    r'best \w+|top \d+|ranking|ranked|'
    r'beta|firmware|release candidate|update now|'
    r'deal|sale|discount|coupon|price drop|'
    r'review|hands[- ]on|unboxing|benchmark|'
    r'lanterns|dcu|mcu|superman|marvel|batman|superhero'
    r')\b',
    re.IGNORECASE
)


def parse_news_date(d):
    from datetime import datetime, timezone

    if not d:
        return None
    for fmt in ('%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S%z',
                '%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S GMT'):
        try:
            dt = datetime.strptime(str(d).strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def home_article_score(article):
    title = article.get('title') or ''
    summary = article.get('summary') or ''
    text = f"{title} {summary}"
    score = 1.0

    if article.get('_api_seed'):
        score += 0.9
    if article.get('image'):
        score += 0.75
    if summary and len(summary) > 40:
        score += 0.25
    if HOME_PRIORITY_PATTERNS.search(text):
        score += 1.8
    if HOME_LOW_VALUE_PATTERNS.search(text):
        score -= 1.7
    if JUNK_PATTERNS.search(title) or HOME_JUNK_PATTERNS.search(title):
        score -= 2.5

    dt = parse_news_date(article.get('published', ''))
    if dt is not None:
        from datetime import datetime, timezone

        age_hours = max(0.0, (datetime.now(timezone.utc) - dt).total_seconds() / 3600)
        score += max(0.0, 1.1 - (age_hours / 72.0))

    return score

# ── Region configs ────────────────────────────────────────────────────────────
REGIONS = {
    "US": {"hl": "en-US", "gl": "US", "ceid": "US:en", "label": "United States"},
    "GB": {"hl": "en-GB", "gl": "GB", "ceid": "GB:en", "label": "United Kingdom"},
    "IN": {"hl": "en-IN", "gl": "IN", "ceid": "IN:en", "label": "India"},
    "AU": {"hl": "en-AU", "gl": "AU", "ceid": "AU:en", "label": "Australia"},
    "CA": {"hl": "en-CA", "gl": "CA", "ceid": "CA:en", "label": "Canada"},
    "SG": {"hl": "en-SG", "gl": "SG", "ceid": "SG:en", "label": "Singapore"},
    "ZA": {"hl": "en-ZA", "gl": "ZA", "ceid": "ZA:en", "label": "South Africa"},
    "NG": {"hl": "en-NG", "gl": "NG", "ceid": "NG:en", "label": "Nigeria"},
    "DE": {"hl": "de",    "gl": "DE", "ceid": "DE:de", "label": "Germany"},
    "FR": {"hl": "fr",    "gl": "FR", "ceid": "FR:fr", "label": "France"},
}

DEFAULT_REGION = "US"


def clean_image_url(url):
    if not url or not isinstance(url, str):
        return None
    url = url.strip()
    if url.startswith("http://"):
        return "https://" + url[7:]
    if url.startswith("https://") or url.startswith("data:image/"):
        return url
    return None


def region_rss_url(path, region_code):
    r = REGIONS.get(region_code, REGIONS[DEFAULT_REGION])
    return f"https://news.google.com/rss/{path}?hl={r['hl']}&gl={r['gl']}&ceid={r['ceid']}"


def fetch_home_articles(region_code=DEFAULT_REGION):
    from datetime import datetime, timezone, timedelta

    RECENCY_DAYS = 3
    cutoff = datetime.now(timezone.utc) - timedelta(days=RECENCY_DAYS)
    seen = set()
    articles = []

    def norm(t):
        return re.sub(r'[^a-z0-9]', '', t.lower())[:60]

    def is_recent(published_str):
        dt = parse_news_date(published_str)
        if dt is None:
            return True
        return dt >= cutoff

    def add(art):
        title = clean_article_title(art.get('title') or '')
        if len(title) <= 12:
            return False
        if JUNK_PATTERNS.search(title) or HOME_JUNK_PATTERNS.search(title):
            return False
        art['title'] = title
        key = norm(title)
        if not key or key in seen:
            return False
        score = home_article_score(art)
        if score <= 0.4:
            return False
        art['_home_score'] = score
        seen.add(key)
        articles.append(art)
        return True

    # Primary high-signal RSS topics for Home feed
    PRIMARY_HOME_PATHS = [
        "headlines",
        "headlines/section/world",
        "headlines/section/business",
        "headlines/section/technology",
        "headlines/section/science",
        "headlines/section/health",
    ]
    TOPIC_FEEDS = [region_rss_url(p, region_code) for p in PRIMARY_HOME_PATHS]

    def fetch_rss(url):
        feed = feedparser.parse(url)
        out = []
        for e in feed.entries[:25]:
            title = clean_article_title(e.get('title') or '')
            if len(title) <= 12 or JUNK_PATTERNS.search(title) or HOME_JUNK_PATTERNS.search(title):
                continue
            pub = e.get('published', '')
            if not is_recent(pub):
                continue
            s_name, s_url, s_domain = extract_feed_source(e)
            out.append({
                'title':     title,
                'summary':   clean_html(e.get('summary', '')),
                'url':       e.get('link', ''),
                'image':     None,
                'published': pub,
                'source':    s_name,
                'source_url': s_url,
                'domain':    s_domain,
                'wfw_commentrss': e.get('wfw_commentrss', ''),
                'comments_url': e.get('comments', ''),
                '_source_kind': 'rss_topic',
            })
        return out

    # Fetch initial topic feeds
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        rss_batches = list(ex.map(fetch_rss, TOPIC_FEEDS))

    rss_added = 0
    for batch in rss_batches:
        for entry in batch:
            if add(entry):
                rss_added += 1
    print(f"  Google News RSS topic feeds: {rss_added} articles")

    def keywords_strict(title):
        stop = {'a','an','the','in','on','at','to','of','and','or','but',
                'for','with','is','was','are','says','say','after','over',
                'as','by','its','it','that','this','has','have','from',
                'be','been','not','no','new','will','can','could','would',
                'more','most','top','best','big','one','two','three',
                'years','year','today','now','just','also','how','why',
                'what','who','when','where','than','amid','into','up',
                'out','off','about','all','here','there','news','latest',
                'live','updates','briefing'}
        caps = re.findall(r'\b[A-Z][a-z]{2,}\b', title)
        caps_filtered = [w for w in caps if w.lower() not in stop]
        if len(caps_filtered) >= 2:
            return ' '.join(caps_filtered[:5])
        words = re.findall(r'[A-Za-z]{3,}', title)
        return ' '.join([w for w in words if w.lower() not in stop][:4])

    def fetch_related_rss(art):
        kw = keywords_strict(art['title'])
        if not kw or len(kw) < 4:
            return []
        enc_kw = urllib.parse.quote(kw)
        r_cfg = REGIONS.get(region_code, REGIONS[DEFAULT_REGION])
        url = (f"https://news.google.com/rss/search?q={enc_kw}"
               f"&hl={r_cfg['hl']}&gl={r_cfg['gl']}&ceid={r_cfg['ceid']}")
        feed = feedparser.parse(url)
        out = []
        for e in feed.entries[:8]:
            title = clean_article_title(e.get('title') or '')
            if len(title) <= 12 or JUNK_PATTERNS.search(title) or HOME_JUNK_PATTERNS.search(title):
                continue
            pub = e.get('published', '')
            if not is_recent(pub):
                continue
            s_name, s_url, s_domain = extract_feed_source(e)
            out.append({
                'title':     title,
                'summary':   clean_html(e.get('summary', '')),
                'url':       e.get('link', ''),
                'image':     None,
                'published': pub,
                '_seed':     norm(art['title']),
                'source':    s_name,
                'source_url': s_url,
                'domain':    s_domain,
                'wfw_commentrss': e.get('wfw_commentrss', ''),
                'comments_url': e.get('comments', ''),
                '_source_kind': 'rss_support',
            })
        return out

    # Cross-reference the top priority headlines in parallel
    top_seeds = sorted(articles, key=lambda a: -a.get('_home_score', 0.0))[:20]
    if top_seeds:
        print(f"  Cross-referencing {len(top_seeds)} top seed home stories...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            xref_batches = list(ex.map(fetch_related_rss, top_seeds))
        xref_added = 0
        for batch in xref_batches:
            for entry in batch:
                if add(entry):
                    xref_added += 1
        print(f"  Cross-reference: {xref_added} additional multi-source articles")

    # Enrich top seed articles with real publisher OG images
    seeds_to_enrich = [a for a in articles if not a.get('image')][:28]
    if seeds_to_enrich:
        print(f"  Extracting real publisher images for {len(seeds_to_enrich)} top stories...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
            extracted_images = list(ex.map(lambda a: extract_article_og_image(a.get('url')), seeds_to_enrich))
        for a, img in zip(seeds_to_enrich, extracted_images):
            if img:
                a['image'] = img
                a['_api_seed'] = True

    print(f"\n=== HOME ({region_code}): {len(articles)} articles, "
          f"{sum(1 for a in articles if a.get('image'))} with images ===\n")
    return articles


TOPIC_CATEGORY_MAP = {
    "business": ("BUSINESS", ["business news", "stock markets economy", "finance corporate"]),
    "technology": ("TECHNOLOGY", ["technology news", "artificial intelligence tech", "gadgets software"]),
    "sports": ("SPORTS", ["sports headlines", "football soccer", "basketball championship"]),
    "sport": ("SPORTS", ["sports headlines", "football soccer", "basketball championship"]),
    "culture": ("ENTERTAINMENT", ["entertainment culture", "film music", "celebrity arts books"]),
    "entertainment": ("ENTERTAINMENT", ["entertainment culture", "film music", "celebrity arts books"]),
    "health": ("HEALTH", ["health medicine", "wellness medical", "healthcare science"]),
    "science": ("SCIENCE", ["science research", "space astronomy", "nature climate"]),
    "world": ("WORLD", ["world news", "international diplomacy", "global affairs"]),
}


def fetch_search_articles(query, region_code=DEFAULT_REGION):
    from datetime import datetime, timezone, timedelta

    if query == HOME_QUERY:
        return fetch_home_articles(region_code=region_code)

    r_cfg = REGIONS.get(region_code, REGIONS[DEFAULT_REGION])
    encoded = urllib.parse.quote(query)
    seen = set()
    articles = []

    RECENCY_DAYS = 30
    cutoff = datetime.now(timezone.utc) - timedelta(days=RECENCY_DAYS)

    def norm(t):
        return re.sub(r'[^a-z0-9]', '', t.lower())[:60]

    def parse_date(d):
        if not d:
            return None
        for fmt in ('%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S%z',
                    '%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S GMT'):
            try:
                dt = datetime.strptime(d.strip(), fmt)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except ValueError:
                continue
        return None

    def is_recent(published_str):
        dt = parse_date(published_str)
        if dt is None:
            return True
        return dt >= cutoff

    def is_relevant(title, ref_query):
        if JUNK_PATTERNS.search(title):
            return False
        stop = {'a','an','the','in','on','at','to','of','and','or','but',
                'for','with','is','was','are','today','trending','popular',
                'most','news','latest'}
        q_words = [w.lower() for w in re.findall(r'[A-Za-z]{3,}', ref_query)
                   if w.lower() not in stop]
        if not q_words:
            return True
        title_lower = title.lower()
        return any(w in title_lower for w in q_words)

    q_norm = query.lower().strip()
    topic_match = None
    for key, val in TOPIC_CATEGORY_MAP.items():
        if q_norm == key or q_norm.startswith(key + " ") or q_norm.startswith("topic:" + key):
            topic_match = val
            break

    if topic_match:
        topic_code, subqueries = topic_match
        print(f"  Fetching Topic Feed: {topic_code} for region {region_code}...")
        topic_urls = [
            f"https://news.google.com/rss/headlines/section/topic/{topic_code}?hl={r_cfg['hl']}&gl={r_cfg['gl']}&ceid={r_cfg['ceid']}"
        ]
        for sq in subqueries:
            enc = urllib.parse.quote(sq)
            topic_urls.append(f"https://news.google.com/rss/search?q={enc}&hl={r_cfg['hl']}&gl={r_cfg['gl']}&ceid={r_cfg['ceid']}")

        def fetch_topic_feed(url):
            feed = feedparser.parse(url)
            out = []
            for e in feed.entries:
                title = clean_article_title(e.get('title') or '')
                if len(title) <= 12 or JUNK_PATTERNS.search(title):
                    continue
                pub = e.get('published', '')
                if not is_recent(pub):
                    continue
                s_name, s_url, s_domain = extract_feed_source(e)
                out.append({
                    'title': title,
                    'summary': clean_html(e.get('summary', '')),
                    'url': e.get('link', ''),
                    'image': None,
                    'published': pub,
                    'source': s_name,
                    'source_url': s_url,
                    'domain': s_domain,
                    'wfw_commentrss': e.get('wfw_commentrss', ''),
                    'comments_url': e.get('comments', ''),
                    '_source_kind': 'rss_topic'
                })
            return out

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            for batch in ex.map(fetch_topic_feed, topic_urls):
                for entry in batch:
                    key = norm(entry['title'])
                    if key and key not in seen:
                        seen.add(key)
                        articles.append(entry)

        # Cross-reference top seeds for multi-source consensus depth
        top_seeds = articles[:15]
        if top_seeds:
            def fetch_related_category_rss(art):
                words = re.findall(r'[A-Za-z]{4,}', art['title'])
                kw = ' '.join(words[:4])
                if not kw or len(kw) < 4:
                    return []
                enc_kw = urllib.parse.quote(kw)
                url = f"https://news.google.com/rss/search?q={enc_kw}&hl={r_cfg['hl']}&gl={r_cfg['gl']}&ceid={r_cfg['ceid']}"
                feed = feedparser.parse(url)
                out = []
                for e in feed.entries[:6]:
                    title = clean_article_title(e.get('title') or '')
                    if len(title) <= 12 or JUNK_PATTERNS.search(title):
                        continue
                    pub = e.get('published', '')
                    if not is_recent(pub):
                        continue
                    s_name, s_url, s_domain = extract_feed_source(e)
                    out.append({
                        'title': title,
                        'summary': clean_html(e.get('summary', '')),
                        'url': e.get('link', ''),
                        'image': None,
                        'published': pub,
                        '_seed': norm(art['title']),
                        'source': s_name,
                        'source_url': s_url,
                        'domain': s_domain,
                        'wfw_commentrss': e.get('wfw_commentrss', ''),
                        'comments_url': e.get('comments', ''),
                        '_source_kind': 'rss_support',
                    })
                return out

            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
                xref_batches = list(ex.map(fetch_related_category_rss, top_seeds))
            for batch in xref_batches:
                for entry in batch:
                    key = norm(entry['title'])
                    if key and key not in seen:
                        seen.add(key)
                        articles.append(entry)

    else:
        gnews_urls = [
            f"https://news.google.com/rss/search?q={encoded}&hl={r_cfg['hl']}&gl={r_cfg['gl']}&ceid={r_cfg['ceid']}",
            f"https://news.google.com/rss/search?q={encoded}+news&hl={r_cfg['hl']}&gl={r_cfg['gl']}&ceid={r_cfg['ceid']}",
            f"https://news.google.com/rss/search?q={encoded}+latest&hl={r_cfg['hl']}&gl={r_cfg['gl']}&ceid={r_cfg['ceid']}",
        ]
        def fetch_gnews(url):
            feed = feedparser.parse(url)
            out = []
            for e in feed.entries:
                title = re.sub(r' - [^-]{2,40}$', '', (e.get('title') or '')).strip()
                if len(title) <= 10 or not is_relevant(title, query):
                    continue
                pub = e.get('published', '')
                if not is_recent(pub):
                    continue
                s_name, s_url, s_domain = extract_feed_source(e)
                out.append({'title': title,
                            'summary': clean_html(e.get('summary', '')),
                            'url': e.get('link', ''), 'image': None,
                            'published': pub,
                            'source': s_name,
                            'source_url': s_url,
                            'domain': s_domain,
                            'wfw_commentrss': e.get('wfw_commentrss', ''),
                            'comments_url': e.get('comments', ''),
                            '_source_kind': 'rss_topic'})
            return out
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
            for batch in ex.map(fetch_gnews, gnews_urls):
                for entry in batch:
                    key = norm(entry['title'])
                    if key and key not in seen:
                        seen.add(key)
                        articles.append(entry)

        # Cross-reference custom search seeds for depth
        top_seeds = articles[:12]
        if top_seeds:
            def fetch_related_search_rss(art):
                words = re.findall(r'[A-Za-z]{4,}', art['title'])
                kw = ' '.join(words[:4])
                if not kw or len(kw) < 4:
                    return []
                enc_kw = urllib.parse.quote(kw)
                url = f"https://news.google.com/rss/search?q={enc_kw}&hl={r_cfg['hl']}&gl={r_cfg['gl']}&ceid={r_cfg['ceid']}"
                feed = feedparser.parse(url)
                out = []
                for e in feed.entries[:5]:
                    title = clean_article_title(e.get('title') or '')
                    if len(title) <= 10 or JUNK_PATTERNS.search(title):
                        continue
                    pub = e.get('published', '')
                    if not is_recent(pub):
                        continue
                    s_name, s_url, s_domain = extract_feed_source(e)
                    out.append({
                        'title': title,
                        'summary': clean_html(e.get('summary', '')),
                        'url': e.get('link', ''),
                        'image': None,
                        'published': pub,
                        '_seed': norm(art['title']),
                        'source': s_name,
                        'source_url': s_url,
                        'domain': s_domain,
                        'wfw_commentrss': e.get('wfw_commentrss', ''),
                        'comments_url': e.get('comments', ''),
                        '_source_kind': 'rss_support',
                    })
                return out

            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
                xref_batches = list(ex.map(fetch_related_search_rss, top_seeds))
            for batch in xref_batches:
                for entry in batch:
                    key = norm(entry['title'])
                    if key and key not in seen:
                        seen.add(key)
                        articles.append(entry)

    # Enrich search results with real publisher OG images
    search_to_enrich = [a for a in articles if not a.get('image')][:28]
    if search_to_enrich:
        print(f"  Extracting real publisher images for {len(search_to_enrich)} search stories...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
            extracted_images = list(ex.map(lambda a: extract_article_og_image(a.get('url')), search_to_enrich))
        for a, img in zip(search_to_enrich, extracted_images):
            if img:
                a['image'] = img
                a['_api_seed'] = True

    print(f"\n=== Total: {len(articles)} articles, "
          f"{sum(1 for a in articles if a.get('image'))} with images ===\n")
    return articles


def get_consensus_summary(articles):
    combined = " ".join(a.get('summary', '') for a in articles)
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', combined)
                 if len(s.strip()) > 30]
    if not sentences:
        return ""
    if len(sentences) == 1:
        return sentences[0][:250]

    vecs = embed(sentences)
    if vecs is not None:
        centroid = vecs.mean(axis=0, keepdims=True)
        scores = (vecs @ centroid.T).flatten()
        best = sentences[int(scores.argmax())]
        return (best[:247] + "...") if len(best) > 250 else best

    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(sentences)
        sim = cosine_similarity(X)
        G = nx.from_numpy_array(sim)
        pr = nx.pagerank(G)
        best = sentences[max(pr, key=pr.get)]
        return (best[:247] + "...") if len(best) > 250 else best
    except (ValueError, nx.NetworkXException):
        return sentences[0][:250]


def get_cluster_title(articles):
    if len(articles) == 1:
        return articles[0]['title']
    titles = [a['title'] for a in articles]

    vecs = embed(titles)
    if vecs is not None:
        centroid = vecs.mean(axis=0, keepdims=True)
        scores = (vecs @ centroid.T).flatten()
        return titles[int(scores.argmax())]

    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(titles)
        scores = cosine_similarity(X).sum(axis=1)
        return titles[int(scores.argmax())]
    except ValueError:
        return titles[0]


def cluster_articles(articles, query=''):
    if not articles:
        return {}

    df = pd.DataFrame(articles)

    def col_or_default(name, default):
        if name in df:
            return df[name]
        return pd.Series([default] * len(df), index=df.index)

    image_col = col_or_default('image', None)
    df['title']     = col_or_default('title', '').fillna('')
    df['summary']   = col_or_default('summary', '').fillna('')
    df['url']       = col_or_default('url', '').fillna('')
    df['image']     = image_col.where(pd.notna(image_col), None)
    df['published'] = col_or_default('published', '').fillna('')
    df['_seed']     = col_or_default('_seed', '').fillna('')
    df['_home_score'] = col_or_default('_home_score', 0.0).fillna(0.0)
    df['source']    = col_or_default('source', '').fillna('')
    df['_source_kind'] = col_or_default('_source_kind', '').fillna('')
    df['_api_seed'] = col_or_default('_api_seed', False).fillna(False)
    n = len(df)

    texts = [(row['title'] + ' ') * 3 + row['summary']
             for _, row in df.iterrows()]

    labels = None
    vecs   = embed(texts)

    if vecs is not None:
        dist_matrix = 1.0 - np.clip(vecs @ vecs.T, -1, 1)
        np.fill_diagonal(dist_matrix, 0.0)

        eps = 0.28
        db = DBSCAN(eps=eps, min_samples=1, metric='precomputed')
        labels = db.fit_predict(dist_matrix)
        print(f"  DBSCAN (MiniLM, eps={eps}): {len(set(labels))} clusters from {n} articles")

        SEED_SIM_GATE = 0.55
        label_arr  = list(labels)
        seed_rep   = {}
        seed_anchor = {}

        for i, row in df.iterrows():
            s = row.get('_seed', '')
            if not s:
                continue
            if s not in seed_anchor:
                seed_anchor[s] = i
                seed_rep[s]    = label_arr[i]
            else:
                j = seed_anchor[s]
                if 1.0 - dist_matrix[i, j] >= SEED_SIM_GATE:
                    old_lbl, new_lbl = label_arr[i], seed_rep[s]
                    if old_lbl != new_lbl:
                        label_arr = [new_lbl if l == old_lbl else l for l in label_arr]
        labels = label_arr

    if labels is None:
        print("  Falling back to TF-IDF union-find clustering.")
        try:
            vectorizer = TfidfVectorizer(stop_words='english',
                                         max_features=5000, min_df=1)
            X   = vectorizer.fit_transform(texts)
            sim = cosine_similarity(X)
        except ValueError as e:
            print(f"  TF-IDF error: {e}")
            sim = None

        parent = list(range(n))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        def union(a, b):
            a, b = find(a), find(b)
            if a != b: parent[b] = a

        THRESHOLD = 0.55
        seed_idx_tf = {}
        for i, row in df.iterrows():
            s = row.get('_seed', '')
            if s:
                if s not in seed_idx_tf:
                    seed_idx_tf[s] = i
                elif sim is not None and sim[i, seed_idx_tf[s]] >= 0.55:
                    union(i, seed_idx_tf[s])

        if sim is not None:
            for i in range(n):
                for j in range(i + 1, n):
                    if sim[i, j] >= THRESHOLD:
                        union(i, j)

        labels = [find(i) for i in range(n)]

    def is_valid_img(img):
        return bool(img and isinstance(img, str) and img.strip() and not img.lower().startswith('nan'))

    temp = {}
    for i, (_, row) in enumerate(df.iterrows()):
        cid = labels[i]
        raw_img = row.get('image')
        valid_img = raw_img if is_valid_img(raw_img) else None
        temp.setdefault(cid, []).append({
            'title':     row['title'],
            'summary':   row['summary'],
            'url':       row['url'],
            'image':     valid_img,
            'published': row.get('published', ''),
            '_home_score': float(row.get('_home_score') or 0.0),
            'source':    row.get('source', ''),
            '_source_kind': row.get('_source_kind', ''),
            '_api_seed': bool(row.get('_api_seed')),
        })

    for cid in temp:
        temp[cid].sort(key=lambda a: (
            0 if a.get('_api_seed') and is_valid_img(a.get('image')) else 1,
            0 if is_valid_img(a.get('image')) else 1,
            -a.get('_home_score', 0.0),
        ))

    query_scores = {}
    effective_query = '' if query == HOME_QUERY else query
    if effective_query:
        cluster_ids   = sorted(temp.keys())
        cluster_texts = [' '.join(a['title'] for a in temp[cid])
                         for cid in cluster_ids]

        q_vecs = embed([effective_query] + cluster_texts)
        if q_vecs is not None:
            q_sim = (q_vecs[0:1] @ q_vecs[1:].T).flatten()
            for cid, score in zip(cluster_ids, q_sim):
                query_scores[cid] = float(score)
        else:
            try:
                qv  = TfidfVectorizer(stop_words='english',
                                      max_features=5000, min_df=1)
                qX  = qv.fit_transform([effective_query] + cluster_texts)
                sims = cosine_similarity(qX[0:1], qX[1:])[0]
                for cid, score in zip(cluster_ids, sims):
                    query_scores[cid] = float(score)
            except ValueError:
                query_scores = {}

    def combined_score(cid):
        rel        = query_scores.get(cid, 0.0)
        size_boost = math.log(len(temp[cid]) + 1)
        api_image_bonus = 0.35 if any(a.get('_api_seed') and is_valid_img(a.get('image')) for a in temp[cid]) else 0.0
        rss_support_bonus = min(0.25, sum(1 for a in temp[cid] if a.get('_source_kind') == 'rss_support') * 0.04)
        base = (rel * size_boost) if query_scores else size_boost
        return base + api_image_bonus + rss_support_bonus

    user_interest_terms = set()
    try:
        u = current_user()
        if u:
            for r in get_user_interests(u["id"]):
                t_low = r["interest"].strip().lower()
                if t_low:
                    user_interest_terms.add(t_low)
    except Exception:
        pass

    def home_cluster_score(cid):
        arts = temp[cid]
        source_names = {
            (a.get('source') or publisher_to_domain(hostname_from_url(a.get('url', '')))).lower()
            for a in arts
            if a.get('source') or a.get('url')
        }
        best_article = max((a.get('_home_score', 0.0) for a in arts), default=0.0)
        avg_article = sum(a.get('_home_score', 0.0) for a in arts) / max(1, len(arts))
        coverage = math.log(len(arts) + 1) * 2.2 + math.log(len(source_names) + 1) * 1.6
        has_image = any(is_valid_img(a.get('image')) for a in arts)
        image_bonus = 1.0 if has_image else 0.0
        support_bonus = min(1.8, sum(1 for a in arts if a.get('_source_kind') == 'rss_support') * 0.25)
        single_source_penalty = -3.5 if len(arts) == 1 else 0.0

        interest_bonus = 0.0
        if user_interest_terms:
            combined_text = " ".join([
                (a.get('title') or '') + " " + (a.get('source') or '') + " " + (a.get('summary') or '')
                for a in arts
            ]).lower()
            for term in user_interest_terms:
                if term in combined_text:
                    interest_bonus += 3.5

        return best_article * 0.70 + avg_article * 0.80 + coverage + image_bonus + support_bonus + single_source_penalty + interest_bonus

    def ranking_score(cid):
        if query == HOME_QUERY:
            return home_cluster_score(cid)
        return combined_score(cid)

    clusters_needing_image = []

    payload_pre = {}
    MAX_HOME_CLUSTERS = 28
    for cid in sorted(temp.keys(), key=lambda c: -ranking_score(c)):
        arts = temp[cid]
        cluster_image = next((a['image'] for a in arts if is_valid_img(a.get('image'))), None)
        if query == HOME_QUERY:
            cluster_title = next(
                (a['title'] for a in arts if a.get('_api_seed') and is_valid_img(a.get('image'))),
                get_cluster_title(arts)
            )
        else:
            cluster_title = get_cluster_title(arts)
        cluster_title = clean_article_title(cluster_title)
        if len(cluster_title) <= 12:
            continue

        score = ranking_score(cid)

        # On Home feed, eliminate noise, single-source low-signal stories, and junk
        if query == HOME_QUERY:
            if JUNK_PATTERNS.search(cluster_title) or HOME_JUNK_PATTERNS.search(cluster_title):
                continue
            if len(arts) == 1 and score < 4.0:
                continue
            if len(payload_pre) >= MAX_HOME_CLUSTERS:
                break

        consensus_summary = (
            get_consensus_summary(arts) if len(arts) > 1
            else (arts[0].get('summary') or '')
        )
        sentiment_info = get_cluster_sentiment(cluster_title, arts, consensus_summary)
        payload_pre[str(cid)] = {
            "cluster_title":     cluster_title,
            "consensus_summary": consensus_summary,
            "cluster_image":     cluster_image,
            "query_score":       score,
            "source_count":      len(arts),
            "sentiment":         sentiment_info,
            "articles": [
                {
                    "title": clean_article_title(a["title"]),
                    "url": a["url"],
                    "summary": a.get("summary", ""),
                    "image": a.get("image"),
                    "published": a.get("published", ""),
                    "source": a.get("source", "") or "",
                    "source_url": a.get("source_url", "") or "",
                    "domain": a.get("domain", "") or "",
                    "wfw_commentrss": a.get("wfw_commentrss", ""),
                    "comments_url": a.get("comments_url", ""),
                }
                for a in arts
            ],
        }
        if cluster_image is None:
            clusters_needing_image.append(str(cid))

    if clusters_needing_image:
        print(f"  Creating local fallback images for "
              f"{len(clusters_needing_image)} imageless clusters...")
        titles_to_fetch = {cid: payload_pre[cid]["cluster_title"]
                           for cid in clusters_needing_image}

        def _fetch_one(cid_title):
            cid, title = cid_title
            return cid, fallback_image(title, query=effective_query)

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            results = list(ex.map(_fetch_one, titles_to_fetch.items()))

        fallback_filled = 0
        seen_fallback_images = {
            payload_pre[cid]["cluster_image"]
            for cid in payload_pre
            if payload_pre[cid].get("cluster_image")
        }
        for cid, img_url in results:
            if img_url:
                title = payload_pre[cid]["cluster_title"]
                # Only deduplicate if it's an SVG data URI
                if img_url.startswith("data:image/svg"):
                    for offset in range(12):
                        if img_url not in seen_fallback_images:
                            break
                        img_url = fallback_image(title, query=effective_query, offset=offset + 1)
                payload_pre[cid]["cluster_image"] = img_url
                seen_fallback_images.add(img_url)
                fallback_filled += 1

        print(f"  Fallback images: filled {fallback_filled} / {len(clusters_needing_image)} clusters")

    # Ensure all sub-articles inherit cluster_image so no article is imageless
    for cid, cdata in payload_pre.items():
        c_img = cdata.get("cluster_image")
        if c_img:
            for art in cdata.get("articles", []):
                if not art.get("image"):
                    art["image"] = c_img

    return payload_pre


@app.route('/api/cluster')
@login_required
def api_cluster():
    query = request.args.get('q', '').strip()
    user = current_user()
    user_reg = get_user_region(user)
    region = request.args.get('region', user_reg).strip().upper()
    if region not in REGIONS:
        region = user_reg if user_reg in REGIONS else DEFAULT_REGION
    if not query:
        return jsonify({})

    # Record search query as a user interest
    if user and query and query != HOME_QUERY and query.lower() not in ('business', 'technology', 'sports', 'health', 'culture'):
        save_user_interest(user["id"], query, source_type="search")

    mock_clusters = app.config.get('MOCK_CLUSTERS')
    if mock_clusters is not None:
        return jsonify(mock_clusters)

    clusters = cluster_articles(fetch_search_articles(query, region_code=region), query=query)
    return jsonify(json_safe(clusters))


@app.route('/api/regions')
@login_required
def api_regions():
    return jsonify({code: info['label'] for code, info in REGIONS.items()})


@app.route('/api/region', methods=['POST'])
@login_required
def api_set_region():
    user = current_user()
    data = request.get_json(silent=True) or request.form
    region = (data.get('region') or '').strip().upper()
    if region not in REGIONS:
        return jsonify({"error": f"Invalid region '{region}'"}), 400

    session['region'] = region
    with get_db() as db:
        db.execute(
            f"UPDATE users SET preferred_region = {sql_param()} WHERE id = {sql_param()}",
            (region, user["id"]),
        )
    return jsonify({"success": True, "region": region})


@app.route('/api/account')
@login_required
def api_account():
    user = current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    created_at = user["created_at"]
    if hasattr(created_at, "isoformat"):
        created_at = created_at.isoformat()
    elif created_at is not None:
        created_at = str(created_at)

    with get_db() as db:
        count_row = db.execute(
            f"SELECT COUNT(*) AS total FROM article_history WHERE user_id = {sql_param()}",
            (user["id"],),
        ).fetchone()
        history_count = count_row["total"] if count_row else 0

        bm_row = db.execute(
            f"SELECT COUNT(*) AS total FROM bookmarks WHERE user_id = {sql_param()}",
            (user["id"],),
        ).fetchone()
        bookmarks_count = bm_row["total"] if bm_row else 0

    return jsonify({
        "id": user["id"],
        "username": user["username"],
        "email": user["email"] or "",
        "avatar_url": user["avatar_url"] or "",
        "preferred_region": get_user_region(user),
        "created_at": created_at,
        "history_count": history_count,
        "bookmarks_count": bookmarks_count,
    })


@app.route('/api/history')
@login_required
def api_history():
    user = current_user()
    with get_db() as db:
        rows = db.execute(
            f"""
            SELECT id, title, article_text, image_url, source_count, sources_json, created_at
            FROM article_history
            WHERE user_id = {sql_param()}
            ORDER BY created_at DESC, id DESC
            LIMIT 20
            """,
            (user["id"],),
        ).fetchall()
    return jsonify([history_row_to_dict(row) for row in rows])


@app.route('/api/history/clear', methods=['POST'])
@login_required
def api_history_clear():
    user = current_user()
    with get_db() as db:
        db.execute(
            f"DELETE FROM article_history WHERE user_id = {sql_param()}",
            (user["id"],),
        )
    return jsonify({"success": True})


@app.route('/api/history/<int:history_id>', methods=['DELETE', 'POST'])
@login_required
def api_history_item_delete(history_id):
    user = current_user()
    with get_db() as db:
        db.execute(
            f"DELETE FROM article_history WHERE id = {sql_param()} AND user_id = {sql_param()}",
            (history_id, user["id"]),
        )
    return jsonify({"success": True, "id": history_id})


@app.route('/api/history/remove', methods=['POST'])
@login_required
def api_history_remove():
    user = current_user()
    data = request.get_json(silent=True) or request.form
    history_id = data.get('id')
    if not history_id:
        return jsonify({"error": "History ID required"}), 400
    with get_db() as db:
        db.execute(
            f"DELETE FROM article_history WHERE id = {sql_param()} AND user_id = {sql_param()}",
            (int(history_id), user["id"]),
        )
    return jsonify({"success": True, "id": history_id})


@app.route('/api/bookmarks', methods=['GET'])
@login_required
def api_bookmarks():
    user = current_user()
    with get_db() as db:
        rows = db.execute(
            f"""
            SELECT id, title, article_text, image_url, source_count, sources_json, created_at
            FROM bookmarks
            WHERE user_id = {sql_param()}
            ORDER BY created_at DESC, id DESC
            LIMIT 100
            """,
            (user["id"],),
        ).fetchall()
    return jsonify([bookmark_row_to_dict(row) for row in rows])


@app.route('/api/bookmarks/toggle', methods=['POST'])
@login_required
def api_bookmarks_toggle():
    user = current_user()
    data = request.get_json(silent=True) or request.form
    title = (data.get('title') or '').strip()
    if not title:
        return jsonify({"error": "Title is required"}), 400

    article_text = (data.get('article_text') or data.get('article') or '').strip()
    image_url = (data.get('image_url') or data.get('image') or '').strip()
    sources = data.get('sources') or []
    if isinstance(sources, str):
        try:
            sources = json.loads(sources)
        except Exception:
            sources = []

    if not image_url and sources:
        for s in sources:
            img = s.get("image") or s.get("image_url") or s.get("cluster_image")
            if img and is_valid_img(img):
                image_url = img
                break

    cleaned_sources = [
        {
            "title": (s.get("title") or "").strip(),
            "url": (s.get("url") or "").strip(),
        }
        for s in sources
        if s.get("url")
    ][:12]

    with get_db() as db:
        existing = db.execute(
            f"SELECT id FROM bookmarks WHERE user_id = {sql_param()} AND title = {sql_param()}",
            (user["id"], title[:240]),
        ).fetchone()

        if existing:
            db.execute(
                f"DELETE FROM bookmarks WHERE id = {sql_param()} AND user_id = {sql_param()}",
                (existing["id"], user["id"]),
            )
            return jsonify({"bookmarked": False, "id": existing["id"], "action": "removed"})
        else:
            param = sql_param()
            db.execute(
                f"""
                INSERT INTO bookmarks
                    (user_id, title, article_text, image_url, source_count, sources_json)
                VALUES ({param}, {param}, {param}, {param}, {param}, {param})
                """,
                (
                    user["id"],
                    title[:240],
                    article_text,
                    image_url,
                    len(cleaned_sources),
                    json.dumps(cleaned_sources),
                ),
            )
            created = db.execute(
                f"SELECT * FROM bookmarks WHERE user_id = {sql_param()} AND title = {sql_param()}",
                (user["id"], title[:240]),
            ).fetchone()
            return jsonify({
                "bookmarked": True,
                "bookmark": bookmark_row_to_dict(created) if created else None,
                "action": "added"
            })


@app.route('/api/bookmarks/<int:bookmark_id>', methods=['DELETE', 'POST'])
@login_required
def api_bookmarks_item_delete(bookmark_id):
    user = current_user()
    with get_db() as db:
        db.execute(
            f"DELETE FROM bookmarks WHERE id = {sql_param()} AND user_id = {sql_param()}",
            (bookmark_id, user["id"]),
        )
    return jsonify({"success": True, "id": bookmark_id})


@app.route('/api/bookmarks/remove', methods=['POST'])
@login_required
def api_bookmarks_remove():
    user = current_user()
    data = request.get_json(silent=True) or request.form
    bookmark_id = data.get('id')
    if not bookmark_id:
        return jsonify({"error": "Bookmark ID required"}), 400
    with get_db() as db:
        db.execute(
            f"DELETE FROM bookmarks WHERE id = {sql_param()} AND user_id = {sql_param()}",
            (int(bookmark_id), user["id"]),
        )
    return jsonify({"success": True, "id": bookmark_id})


@app.route('/api/bookmarks/clear', methods=['POST'])
@login_required
def api_bookmarks_clear():
    user = current_user()
    with get_db() as db:
        db.execute(
            f"DELETE FROM bookmarks WHERE user_id = {sql_param()}",
            (user["id"],),
        )
    return jsonify({"success": True})


@app.route('/api/bookmarks/check', methods=['GET'])
@login_required
def api_bookmarks_check():
    user = current_user()
    title = (request.args.get('title') or '').strip()
    if not title:
        return jsonify({"bookmarked": False})
    with get_db() as db:
        existing = db.execute(
            f"SELECT id FROM bookmarks WHERE user_id = {sql_param()} AND title = {sql_param()}",
            (user["id"], title[:240]),
        ).fetchone()
    return jsonify({"bookmarked": bool(existing), "id": existing["id"] if existing else None})


@app.route('/api/comments', methods=['GET', 'POST'])
@login_required
def api_comments():
    user = current_user()
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        title = (data.get('title') or data.get('article_title') or '').strip()
        content = (data.get('content') or data.get('comment') or '').strip()
        article_url = (data.get('article_url') or data.get('url') or '').strip()
        rating = data.get('rating', 0)
        try:
            rating = int(rating)
        except (ValueError, TypeError):
            rating = 0

        if not title:
            return jsonify({'error': 'Article title is required'}), 400
        if not content or len(content) < 2:
            return jsonify({'error': 'Comment content cannot be empty'}), 400

        # Perform semantic sentiment analysis
        analysis = SemanticSentimentAnalyzer.analyze(content, rating=rating)

        author_name = user['username'] if user else (data.get('author_name') or 'Community Reader')
        avatar_url = (user['avatar_url'] if user else '') or ''
        user_id = user['id'] if user else None

        with get_db() as db:
            p = sql_param()
            if USE_POSTGRES:
                cursor = db.execute(
                    f"""
                    INSERT INTO article_comments
                        (user_id, article_title, article_url, author_name, avatar_url,
                         content, sentiment, positivity_score, negativity_score, source, rating)
                    VALUES ({p}, {p}, {p}, {p}, {p}, {p}, {p}, {p}, {p}, {p}, {p})
                    RETURNING id, user_id, article_title, article_url, author_name, avatar_url,
                              content, sentiment, positivity_score, negativity_score, source, rating, created_at
                    """,
                    (
                        user_id,
                        title[:240],
                        article_url,
                        author_name,
                        avatar_url,
                        content[:2000],
                        analysis['sentiment'],
                        analysis['positivity_score'],
                        analysis['negativity_score'],
                        'user',
                        rating,
                    )
                )
                created_row = cursor.fetchone()
            else:
                cursor = db.execute(
                    f"""
                    INSERT INTO article_comments
                        (user_id, article_title, article_url, author_name, avatar_url,
                         content, sentiment, positivity_score, negativity_score, source, rating)
                    VALUES ({p}, {p}, {p}, {p}, {p}, {p}, {p}, {p}, {p}, {p}, {p})
                    """,
                    (
                        user_id,
                        title[:240],
                        article_url,
                        author_name,
                        avatar_url,
                        content[:2000],
                        analysis['sentiment'],
                        analysis['positivity_score'],
                        analysis['negativity_score'],
                        'user',
                        rating,
                    )
                )
                new_id = cursor.lastrowid
                created_row = db.execute(
                    f"SELECT * FROM article_comments WHERE id = {sql_param()}",
                    (new_id,)
                ).fetchone()

        all_comments = get_comments_for_article(title)
        sentiment_summary = aggregate_comments_sentiment(all_comments, fallback_text=title)

        return jsonify({
            'success': True,
            'comment': comment_row_to_dict(created_row),
            'sentiment': sentiment_summary,
            'total_comments': len(all_comments),
        })

    # GET request
    title = (request.args.get('title') or request.args.get('q') or '').strip()
    if not title:
        return jsonify({'error': 'Title query parameter required', 'comments': [], 'sentiment': {}}), 400

    comments = get_comments_for_article(title)
    if not comments:
        # Check if articles were passed in request or attempt RSS comment fetch
        comments = fetch_and_store_rss_comments(title)

    sentiment_summary = aggregate_comments_sentiment(comments, fallback_text=title)
    return jsonify({
        'article_title': title,
        'sentiment': sentiment_summary,
        'comments': comments,
        'total_comments': len(comments),
    })


@app.route('/api/comments/<int:comment_id>', methods=['DELETE', 'POST'])
@login_required
def api_comment_delete(comment_id):
    user = current_user()
    with get_db() as db:
        comment = db.execute(
            f"SELECT * FROM article_comments WHERE id = {sql_param()}",
            (comment_id,)
        ).fetchone()
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404
        # Allow deletion if user created the comment or is authenticated user
        if comment['user_id'] and comment['user_id'] != user['id']:
            return jsonify({'error': 'Forbidden: cannot delete other users comments'}), 403

        db.execute(
            f"DELETE FROM article_comments WHERE id = {sql_param()}",
            (comment_id,)
        )
    return jsonify({'success': True, 'id': comment_id})


@app.route('/api/comments/remove', methods=['POST'])
@login_required
def api_comment_remove():
    user = current_user()
    data = request.get_json(silent=True) or request.form
    comment_id = data.get('id')
    if not comment_id:
        return jsonify({'error': 'Comment ID required'}), 400
    try:
        comment_id = int(comment_id)
    except ValueError:
        return jsonify({'error': 'Invalid comment ID'}), 400

    with get_db() as db:
        comment = db.execute(
            f"SELECT * FROM article_comments WHERE id = {sql_param()}",
            (comment_id,)
        ).fetchone()
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404
        if comment['user_id'] and comment['user_id'] != user['id']:
            return jsonify({'error': 'Forbidden: cannot delete other users comments'}), 403

        db.execute(
            f"DELETE FROM article_comments WHERE id = {sql_param()}",
            (comment_id,)
        )
    return jsonify({'success': True, 'id': comment_id})


def scrape_article_text(url, max_chars=4000):
    if not url or not url.startswith('http'):
        return ''
    dest_url = url
    if 'news.google.com' in url:
        try:
            from googlenewsdecoder import gnewsdecoder
            res = gnewsdecoder(url)
            if res.get('status') and res.get('decoded_url'):
                dest_url = res.get('decoded_url')
        except Exception:
            pass

    try:
        import random
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        ]
        hdrs = {
            **HEADERS,
            "User-Agent": random.choice(agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        resp = requests.get(dest_url, headers=hdrs, timeout=8, allow_redirects=True, stream=True)
        chunk = b""
        for piece in resp.iter_content(16384):
            chunk += piece
            if len(chunk) >= 150000:
                break
        resp.close()
        if resp.status_code not in (200, 203):
            return ''
        raw = chunk.decode('utf-8', errors='ignore')
        paras = extract_clean_paragraphs(raw)
        text = ' '.join(paras)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:max_chars]
    except (requests.RequestException, ValueError):
        return ''


@app.route('/api/synthesize', methods=['POST'])
@login_required
def api_synthesize():
    data = request.get_json(force=True)
    cluster_title = (data.get('title') or 'News Summary').strip()
    cluster_image = (data.get('image') or '').strip() or None
    articles = data.get('articles', [])[:12]

    if not articles and not cluster_title:
        return jsonify({'error': 'No articles provided'}), 400

    mock_synth = app.config.get('MOCK_SYNTHESIZE')
    if mock_synth is not None:
        save_article_history(cluster_title, mock_synth, cluster_image, articles)
        return jsonify({'article': mock_synth})

    urls_to_scrape = [a['url'] for a in articles if a.get('url')][:8]
    scraped = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(scrape_article_text, u): u for u in urls_to_scrape}
        for fut in concurrent.futures.as_completed(futures):
            u = futures[fut]
            scraped[u] = fut.result()

    all_text = ' '.join(
        ' '.join((
            a.get('title') or '',
            a.get('summary') or '',
            scraped.get(a.get('url', ''), ''),
        ))
        for a in articles
    )
    sentences = [
        s.strip()
        for s in re.split(r'(?<=[.!?])\s+', all_text)
        if len(s.strip()) > 35 and is_useful_sentence(s.strip())
    ]
    if not sentences:
        fallback_bits = []
        if cluster_title:
            fallback_bits.append(cluster_title)
        fallback_bits.extend(
            a.get('title', '').strip()
            for a in articles
            if a.get('title') and a.get('title', '').strip() != cluster_title
        )
        fallback_text = '. '.join(fallback_bits[:6]).strip()
        if fallback_text:
            if not fallback_text.endswith(('.', '!', '?')):
                fallback_text += '.'
            save_article_history(cluster_title, fallback_text, cluster_image, articles)
            return jsonify({'article': fallback_text})
        return jsonify({'article': 'No usable article text was available from these sources.'})

    seen_sent = []
    seen_keys = set()
    for s in sentences:
        key = re.sub(r'[^a-z0-9]', '', s.lower())[:80]
        if key not in seen_keys:
            seen_sent.append(s)
            seen_keys.add(key)

    try:
        vect = TfidfVectorizer(stop_words='english')
        X = vect.fit_transform(seen_sent[:90])
        scores = np.asarray(cosine_similarity(X).sum(axis=1)).ravel()
        title_terms = set(re.findall(r'[a-z0-9]+', cluster_title.lower()))
        if title_terms:
            for idx, sentence in enumerate(seen_sent[:90]):
                sentence_terms = set(re.findall(r'[a-z0-9]+', sentence.lower()))
                scores[idx] += len(title_terms & sentence_terms) * 0.35
        ranked = sorted(zip(scores, seen_sent[:90]), reverse=True)
        top = [s for _, s in ranked[:9]]
        order = {s: seen_sent.index(s) for s in top if s in seen_sent}
        top.sort(key=lambda s: order.get(s, 0))
    except ValueError:
        top = seen_sent[:9]

    paragraphs = []
    for idx in range(0, len(top), 3):
        paragraph = ' '.join(top[idx:idx + 3]).strip()
        if paragraph:
            paragraphs.append(paragraph)

    article_text = '\n\n'.join(paragraphs)
    save_article_history(cluster_title, article_text, cluster_image, articles)

    return jsonify({'article': article_text})


@app.route('/favicon.ico')
def favicon():
    return '', 204


@app.route('/')
@login_required
def index():
    user = current_user()
    regions_json = {code: info['label'] for code, info in REGIONS.items()}
    user_reg = get_user_region(user)
    return render_template(
        'index.html',
        regions=regions_json,
        user=user,
        default_region=user_reg,
    )


@app.route('/roundup')
@login_required
def roundup_page():
    user = current_user()
    regions_json = {code: info['label'] for code, info in REGIONS.items()}
    history_id = request.args.get('id', type=int)
    initial_roundup_json = None
    roundup_title = None
    initial_image = None
    if history_id:
        with get_db() as db:
            row = db.execute(
                f"SELECT * FROM article_history WHERE id = {sql_param()} AND user_id = {sql_param()}",
                (history_id, user["id"])
            ).fetchone()
            if row:
                d = history_row_to_dict(row)
                initial_roundup_json = d
                roundup_title = d.get('title')
                initial_image = d.get('image_url')

    user_reg = get_user_region(user)
    return render_template(
        'roundup.html',
        user=user,
        regions=regions_json,
        roundup_title=roundup_title,
        initial_image=initial_image,
        initial_roundup_json=initial_roundup_json,
        default_region=user_reg,
    )


@app.route('/roundup/<int:history_id>')
@login_required
def roundup_by_id(history_id):
    user = current_user()
    regions_json = {code: info['label'] for code, info in REGIONS.items()}
    initial_roundup_json = None
    roundup_title = None
    initial_image = None
    with get_db() as db:
        row = db.execute(
            f"SELECT * FROM article_history WHERE id = {sql_param()} AND user_id = {sql_param()}",
            (history_id, user["id"])
        ).fetchone()
        if row:
            d = history_row_to_dict(row)
            initial_roundup_json = d
            roundup_title = d.get('title')
            initial_image = d.get('image_url')

    user_reg = get_user_region(user)
    return render_template(
        'roundup.html',
        user=user,
        regions=regions_json,
        roundup_title=roundup_title,
        initial_image=initial_image,
        initial_roundup_json=initial_roundup_json,
        default_region=user_reg,
    )


@app.route('/history')
@login_required
def history_page():
    user = current_user()
    regions_json = {code: info['label'] for code, info in REGIONS.items()}
    with get_db() as db:
        rows = db.execute(
            f"""
            SELECT id, title, article_text, image_url, source_count, sources_json, created_at
            FROM article_history
            WHERE user_id = {sql_param()}
            ORDER BY created_at DESC, id DESC
            LIMIT 100
            """,
            (user["id"],),
        ).fetchall()
        history_items = [history_row_to_dict(row) for row in rows]

    user_reg = get_user_region(user)
    return render_template(
        'history.html',
        user=user,
        regions=regions_json,
        history_items=history_items,
        history_count=len(history_items),
        default_region=user_reg,
    )


@app.route('/bookmarks')
@login_required
def bookmarks_page():
    user = current_user()
    regions_json = {code: info['label'] for code, info in REGIONS.items()}
    with get_db() as db:
        rows = db.execute(
            f"""
            SELECT id, title, article_text, image_url, source_count, sources_json, created_at
            FROM bookmarks
            WHERE user_id = {sql_param()}
            ORDER BY created_at DESC, id DESC
            LIMIT 100
            """,
            (user["id"],),
        ).fetchall()
        bookmark_items = [bookmark_row_to_dict(row) for row in rows]

    user_reg = get_user_region(user)
    return render_template(
        'bookmarks.html',
        user=user,
        regions=regions_json,
        bookmark_items=bookmark_items,
        bookmarks_count=len(bookmark_items),
        default_region=user_reg,
    )


@app.route('/settings')
@login_required
def settings():
    user = current_user()
    regions_json = {code: info['label'] for code, info in REGIONS.items()}
    interests = get_user_interests(user["id"])
    user_reg = get_user_region(user)
    return render_template(
        'settings.html',
        user=user,
        regions=regions_json,
        interests=interests,
        default_region=user_reg,
    )


@app.route('/api/interests', methods=['GET', 'POST'])
@login_required
def api_interests():
    user = current_user()
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        interest = (data.get('interest') or '').strip()
        if not interest:
            return jsonify({"error": "Interest cannot be empty"}), 400
        saved = save_user_interest(user["id"], interest, source_type="manual")
        return jsonify({"success": True, "interest": saved, "interests": get_user_interests(user["id"])})
    return jsonify(get_user_interests(user["id"]))


@app.route('/api/interests/<int:interest_id>', methods=['DELETE'])
@login_required
def api_interests_delete(interest_id):
    user = current_user()
    delete_user_interest(user["id"], interest_id=interest_id)
    return jsonify({"success": True, "interests": get_user_interests(user["id"])})


@app.route('/api/interests/remove', methods=['POST'])
@login_required
def api_interests_remove():
    user = current_user()
    data = request.get_json(silent=True) or request.form
    interest_id = data.get('id')
    interest_name = data.get('interest')
    delete_user_interest(user["id"], interest_id=interest_id, interest_name=interest_name)
    return jsonify({"success": True, "interests": get_user_interests(user["id"])})


@app.route('/api/interests/clear', methods=['POST'])
@login_required
def api_interests_clear():
    user = current_user()
    clear_user_interests(user["id"])
    return jsonify({"success": True, "interests": []})


def generate_unique_username(base_name: str) -> str:
    """Generate a unique username from base name (e.g. from Google name or email prefix)."""
    clean = re.sub(r'[^A-Za-z0-9_.-]', '', base_name.strip())
    if len(clean) < 3:
        clean = f"user_{secrets.token_hex(3)}"
    elif len(clean) > 28:
        clean = clean[:28]

    candidate = clean
    suffix = 1
    with get_db() as db:
        while True:
            if USE_POSTGRES:
                existing = db.execute("SELECT id FROM users WHERE username = %s", (candidate,)).fetchone()
            else:
                existing = db.execute("SELECT id FROM users WHERE username = ?", (candidate,)).fetchone()
            if not existing:
                return candidate
            candidate = f"{clean[:24]}_{suffix}"
            suffix += 1


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user() is not None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        with get_db() as db:
            if USE_POSTGRES:
                user = db.execute(
                    "SELECT id, username, email, password_hash FROM users WHERE LOWER(email) = LOWER(%s)",
                    (email,),
                ).fetchone()
            else:
                user = db.execute(
                    "SELECT id, username, email, password_hash FROM users WHERE LOWER(email) = LOWER(?)",
                    (email,),
                ).fetchone()

        if user is None or not user['password_hash'] or not check_password_hash(user['password_hash'], password):
            flash('Invalid email or password.', 'error')
        else:
            session.clear()
            session['user_id'] = user['id']
            next_url = request.args.get('next') or url_for('index')
            return redirect(next_url if next_url.startswith('/') else url_for('index'))

    return render_template('auth.html', mode='login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user() is not None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not email or not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', email):
            flash('Please enter a valid email address.', 'error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
        elif password != confirm_password:
            flash('Passwords do not match.', 'error')
        else:
            # Check for existing email
            with get_db() as db:
                if USE_POSTGRES:
                    existing_email = db.execute("SELECT id FROM users WHERE LOWER(email) = %s", (email,)).fetchone()
                else:
                    existing_email = db.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email,)).fetchone()
            if existing_email:
                flash('That email is already registered.', 'error')
            else:
                username = generate_unique_username(email.split('@')[0])
                try:
                    with get_db() as db:
                        password_hash = generate_password_hash(password)
                        if USE_POSTGRES:
                            cursor = db.execute(
                                """
                                INSERT INTO users (email, username, password_hash)
                                VALUES (%s, %s, %s)
                                RETURNING id
                                """,
                                (email, username, password_hash),
                            )
                            user_id = cursor.fetchone()["id"]
                        else:
                            cursor = db.execute(
                                "INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)",
                                (email, username, password_hash),
                            )
                            user_id = cursor.lastrowid
                        session.clear()
                        session['user_id'] = user_id
                        return redirect(url_for('index'))
                except UNIQUE_ERRORS:
                    flash('That email is already registered.', 'error')

    return render_template('auth.html', mode='register')


@app.route('/login/google')
def login_google():
    if current_user() is not None:
        return redirect(url_for('index'))

    # If in test mode with mock query param, redirect directly to test mock callback
    if app.config.get("TESTING") and request.args.get("mock") == "1":
        return redirect(url_for('google_callback', mock="1", code="mock_code", state="mock_state"))

    client_id = app.config.get("GOOGLE_CLIENT_ID") or os.environ.get("GOOGLE_CLIENT_ID")
    if not client_id:
        if app.config.get("TESTING"):
            return redirect(url_for('google_callback', mock="1", code="mock_code", state="mock_state"))
        flash('Google Sign-In is not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env.', 'error')
        return redirect(url_for('login'))

    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    redirect_uri = url_for('google_callback', _external=True)

    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
        'access_type': 'online',
        'prompt': 'select_account',
    }
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    return redirect(google_auth_url)


@app.route('/login/google/callback')
def google_callback():
    error = request.args.get('error')
    if error:
        flash(f'Google Sign-In was cancelled or failed ({error}).', 'error')
        return redirect(url_for('login'))

    is_mock = request.args.get('mock') == '1' and app.config.get('TESTING')

    if is_mock:
        google_info = {
            'sub': 'google_mock_user_123',
            'email': 'tester@gmail.com',
            'name': 'Google Tester',
            'picture': 'https://picsum.photos/100/100',
        }
    else:
        state = request.args.get('state')
        saved_state = session.pop('oauth_state', None)
        if not state or state != saved_state:
            flash('Invalid OAuth state. Please try logging in again.', 'error')
            return redirect(url_for('login'))

        code = request.args.get('code')
        if not code:
            flash('Missing authorization code from Google.', 'error')
            return redirect(url_for('login'))

        client_id = app.config.get("GOOGLE_CLIENT_ID") or os.environ.get("GOOGLE_CLIENT_ID")
        client_secret = app.config.get("GOOGLE_CLIENT_SECRET") or os.environ.get("GOOGLE_CLIENT_SECRET")
        redirect_uri = url_for('google_callback', _external=True)

        try:
            token_resp = requests.post(
                'https://oauth2.googleapis.com/token',
                data={
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'code': code,
                    'grant_type': 'authorization_code',
                    'redirect_uri': redirect_uri,
                },
                timeout=10,
            )
            token_data = token_resp.json()
            access_token = token_data.get('access_token')
            if not access_token:
                flash('Failed to obtain access token from Google.', 'error')
                return redirect(url_for('login'))

            userinfo_resp = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {access_token}'},
                timeout=10,
            )
            google_info = userinfo_resp.json()
        except requests.RequestException as e:
            flash(f'Network error connecting to Google: {e}', 'error')
            return redirect(url_for('login'))

    google_id = str(google_info.get('sub', '')).strip()
    google_email = (google_info.get('email') or '').strip().lower()
    google_name = (google_info.get('name') or '').strip()
    avatar_url = (google_info.get('picture') or '').strip()

    if not google_id or not google_email:
        flash('Could not retrieve Google profile information.', 'error')
        return redirect(url_for('login'))

    with get_db() as db:
        # 1. Try finding by google_id
        if USE_POSTGRES:
            user = db.execute("SELECT id, username, email FROM users WHERE google_id = %s", (google_id,)).fetchone()
        else:
            user = db.execute("SELECT id, username, email FROM users WHERE google_id = ?", (google_id,)).fetchone()

        if user:
            user_id = user['id']
            if avatar_url:
                if USE_POSTGRES:
                    db.execute("UPDATE users SET avatar_url = %s WHERE id = %s AND (avatar_url IS NULL OR avatar_url = '')", (avatar_url, user_id))
                else:
                    db.execute("UPDATE users SET avatar_url = ? WHERE id = ? AND (avatar_url IS NULL OR avatar_url = '')", (avatar_url, user_id))
        else:
            # 2. Try finding by email to link account
            if USE_POSTGRES:
                user_by_email = db.execute("SELECT id FROM users WHERE LOWER(email) = %s", (google_email,)).fetchone()
            else:
                user_by_email = db.execute("SELECT id FROM users WHERE LOWER(email) = ?", (google_email,)).fetchone()

            if user_by_email:
                user_id = user_by_email['id']
                if USE_POSTGRES:
                    db.execute("UPDATE users SET google_id = %s, avatar_url = COALESCE(avatar_url, %s) WHERE id = %s", (google_id, avatar_url, user_id))
                else:
                    db.execute("UPDATE users SET google_id = ?, avatar_url = COALESCE(avatar_url, ?) WHERE id = ?", (google_id, avatar_url, user_id))
            else:
                # 3. Create new user
                base_name = google_name.replace(' ', '_') if google_name else google_email.split('@')[0]
                username = generate_unique_username(base_name)
                if USE_POSTGRES:
                    cursor = db.execute(
                        """
                        INSERT INTO users (username, email, google_id, avatar_url, password_hash)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (username, google_email, google_id, avatar_url, ""),
                    )
                    user_id = cursor.fetchone()["id"]
                else:
                    cursor = db.execute(
                        "INSERT INTO users (username, email, google_id, avatar_url, password_hash) VALUES (?, ?, ?, ?, ?)",
                        (username, google_email, google_id, avatar_url, ""),
                    )
                    user_id = cursor.lastrowid

    session.clear()
    session['user_id'] = user_id
    return redirect(url_for('index'))


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(debug=debug, host="0.0.0.0", port=port)
