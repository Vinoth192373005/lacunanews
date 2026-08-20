"""
Pytest configuration and fixtures for Lacuna Selenium E2E tests.
Provides live test server, database isolation, Selenium WebDriver management,
and authentication helpers.
"""

import os
import sys
import time
import socket
import tempfile
import threading
from typing import Generator
import pytest
from werkzeug.serving import make_server
from werkzeug.security import generate_password_hash

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import news
from news import app, init_db, get_db
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService


def pytest_addoption(parser):
    """Add custom CLI options for pytest."""
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run tests in headed mode (display browser window)",
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use for testing: chrome (default), safari, or arc",
    )


def find_free_port() -> int:
    """Find an available port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


class ServerThread(threading.Thread):
    """Thread running the Werkzeug WSGI server."""

    def __init__(self, app, host: str, port: int):
        super().__init__()
        self.server = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


SAMPLE_CLUSTERS = {
    "cluster_1": {
        "cluster_title": "Major Breakthrough in Quantum Computing Announced",
        "cluster_image": "https://picsum.photos/800/600",
        "consensus_summary": "Researchers achieve record coherence times in silicon-based quantum processors.",
        "query_score": 1.0,
        "articles": [
            {
                "title": "Major Breakthrough in Quantum Computing Announced",
                "url": "https://example.com/quantum-news",
                "published": "2026-08-18T08:00:00Z",
                "source": "TechDaily",
                "domain": "techdaily.com",
                "summary": "Quantum supremacy advances with new silicon qubit architecture."
            },
            {
                "title": "Quantum processor sets new benchmark for speed",
                "url": "https://example.com/quantum-benchmark",
                "published": "2026-08-18T07:30:00Z",
                "source": "ScienceWire",
                "domain": "sciencewire.org",
                "summary": "Benchmarking results confirm stable multi-qubit gates."
            }
        ]
    },
    "cluster_2": {
        "cluster_title": "Global Markets Rally Following Key Policy Decision",
        "cluster_image": "https://picsum.photos/800/601",
        "consensus_summary": "Stock indices surged across Europe and Asia amid easing economic forecasts.",
        "query_score": 0.8,
        "articles": [
            {
                "title": "Global Markets Rally Following Key Policy Decision",
                "url": "https://example.com/markets-rally",
                "published": "2026-08-18T06:45:00Z",
                "source": "MarketWatch",
                "domain": "marketwatch.com",
                "summary": "Stocks posted gains for the third consecutive session."
            }
        ]
    },
    "cluster_3": {
        "cluster_title": "Championship Finals Set After Thrilling Semi-Final Match",
        "cluster_image": "",
        "consensus_summary": "Underdogs secure a dramatic victory in extra time.",
        "query_score": 0.6,
        "articles": [
            {
                "title": "Championship Finals Set After Thrilling Semi-Final Match",
                "url": "https://example.com/sports-final",
                "published": "2026-08-18T05:20:00Z",
                "source": "SportsNet",
                "domain": "sportsnet.com",
                "summary": "Extra time goal propels team to the championship."
            }
        ]
    }
}

SAMPLE_SYNTHESIS = """Researchers and industry leaders have announced a groundbreaking advancement in silicon-based quantum computing, demonstrating coherence times that exceed previous benchmarks by an order of magnitude.

The breakthrough promises to accelerate the commercialization of fault-tolerant quantum algorithms, paving the way for advanced materials simulation, cryptography, and complex optimization problems."""


@pytest.fixture(scope="session")
def test_db_path() -> Generator[str, None, None]:
    """Create a temporary SQLite database file for the test session."""
    fd, path = tempfile.mkstemp(prefix="lacuna_test_", suffix=".sqlite3")
    os.close(fd)

    # Configure Flask app to use the test database
    app.config["TESTING"] = True
    app.config["DATABASE"] = path
    app.config["DATABASE_URL"] = ""
    app.config["SECRET_KEY"] = "selenium-test-secret-key"
    app.config["MOCK_CLUSTERS"] = SAMPLE_CLUSTERS
    app.config["MOCK_SYNTHESIZE"] = SAMPLE_SYNTHESIS
    news.USE_POSTGRES = False
    news._embedder = False

    with app.app_context():
        init_db()

    yield path

    # Teardown
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass


@pytest.fixture(scope="function", autouse=True)
def clean_db(test_db_path: str):
    """Ensure database is clean before each test function."""
    with get_db() as db:
        db.execute("DELETE FROM article_history")
        db.execute("DELETE FROM users")
    yield


@pytest.fixture(scope="session")
def live_server(test_db_path: str) -> Generator[str, None, None]:
    """Start the Flask app on a live background server with an ephemeral port."""
    host = "127.0.0.1"
    port = find_free_port()

    server_thread = ServerThread(app, host, port)
    server_thread.daemon = True
    server_thread.start()

    base_url = f"http://{host}:{port}"

    # Wait for server to become responsive
    max_retries = 30
    for _ in range(max_retries):
        try:
            with socket.create_connection((host, port), timeout=0.5):
                break
        except (OSError, ConnectionRefusedError):
            time.sleep(0.1)
    else:
        raise RuntimeError(f"Live server failed to start on {base_url}")

    yield base_url

    server_thread.shutdown()


@pytest.fixture(scope="function")
def driver(request) -> Generator[webdriver.Remote, None, None]:
    """Provide a configured Selenium WebDriver instance."""
    is_headed = request.config.getoption("--headed")
    browser_name = request.config.getoption("--browser").lower()

    chrome_options = ChromeOptions()
    if not is_headed:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1440,900")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    if browser_name == "arc" and os.path.exists("/Applications/Arc.app/Contents/MacOS/Arc"):
        chrome_options.binary_location = "/Applications/Arc.app/Contents/MacOS/Arc"

    try:
        web_driver = webdriver.Chrome(options=chrome_options)
    except Exception:
        # Fallback to Safari if Chrome is not immediately available
        try:
            web_driver = webdriver.Safari()
            web_driver.set_window_size(1440, 900)
        except Exception as e:
            raise RuntimeError(f"Could not initialize browser driver: {e}")

    web_driver.set_page_load_timeout(30)
    web_driver.implicitly_wait(2)

    yield web_driver

    try:
        web_driver.quit()
    except Exception:
        pass


@pytest.fixture
def create_test_user(test_db_path: str):
    """Helper fixture to insert a test user directly into the database."""
    def _create_user(username: str = "testuser", email: str = None, password: str = "TestPass123!", google_id: str = None, avatar_url: str = None):
        user_email = email if email is not None else f"{username}@example.com"
        with get_db() as db:
            password_hash = generate_password_hash(password) if password else ""
            cursor = db.execute(
                "INSERT INTO users (username, email, password_hash, google_id, avatar_url) VALUES (?, ?, ?, ?, ?)",
                (username, user_email, password_hash, google_id, avatar_url),
            )
            user_id = cursor.lastrowid
        return {"id": user_id, "username": username, "email": user_email, "password": password, "google_id": google_id, "avatar_url": avatar_url}

    return _create_user


@pytest.fixture
def authenticated_driver(driver, live_server, create_test_user):
    """Fixture providing a driver pre-authenticated and redirected to the Home page."""
    from tests.pages.auth_page import AuthPage
    from tests.pages.feed_page import FeedPage

    user = create_test_user(username="testrunner", password="Password123!")

    # Navigate and login
    auth_page = AuthPage(driver, live_server).open_login()
    auth_page.login(user["email"], user["password"])

    # Wait until redirected to home feed
    feed_page = FeedPage(driver, live_server)
    feed_page.find(*feed_page.WORDMARK, timeout=10)
    return driver, user
