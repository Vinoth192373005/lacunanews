# Lacuna

Lacuna is a Flask news aggregator with login, category search, clustered stories, and synthesized article roundups.

## Local Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your local environment file:

```bash
cp .env.example .env
```

Edit `.env` and configure your settings:

```bash
SECRET_KEY=your-random-secret
GOOGLE_CLIENT_ID=your-google-oauth-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-oauth-client-secret
```

> **Google OAuth Setup**:
> 1. In the Google Cloud Console, create OAuth 2.0 Client IDs for a Web Application.
> 2. Add Authorized Redirect URI: `http://127.0.0.1:5001/login/google/callback` (or `https://your-domain.com/login/google/callback` in production).
> 3. Copy Client ID and Client Secret into `.env`.

Run the app locally:

```bash
flask --app news run --port 5001
```

Open:

```text
http://127.0.0.1:5001
```

## Deployment

### Deploy to Vercel

1. **Deploy with Vercel CLI**:
   ```bash
   cd lacuna-vercel
   vercel
   ```

2. **Deploy via GitHub / Vercel Dashboard**:
   - Push this directory or the repository to GitHub.
   - Import the project into Vercel.
   - Set **Root Directory** to `lacuna-vercel` (if importing from root repo) or `./`.
   - Add Environment Variables in Project Settings:
     - `SECRET_KEY`: Long random string (e.g. `openssl rand -hex 32`)
     - `DATABASE_URL` *(Optional, recommended for persistent users)*: PostgreSQL / Neon / Supabase connection string.
     - `GOOGLE_CLIENT_ID` *(Optional, for Google Login)*: Google Cloud OAuth 2.0 Web Client ID.
     - `GOOGLE_CLIENT_SECRET` *(Optional, for Google Login)*: Google Cloud OAuth 2.0 Client Secret.

### Deploy to Render / Standard WSGI Host

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn news:app
```

Environment variables:

```bash
SECRET_KEY
DATABASE_URL
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
```

## Notes

The app uses SQLite by default for local login accounts. On free hosting platforms, local SQLite files may be temporary and can disappear after a redeploy or restart. For a university demo this is usually fine, but for a longer-running app you should move users to a hosted database.

The optional `sentence-transformers` model is not included in `requirements.txt` to keep deployment lighter. If it is not installed, the app automatically falls back to TF-IDF clustering.

## Automated Selenium Testing

The project includes an end-to-end (E2E) automated testing suite built with **Selenium WebDriver** and **pytest**, utilizing the Page Object Model (POM) pattern and isolated temporary test databases.

### Run All Selenium Tests (Headless)

```bash
pytest tests/ -v
```

### Run Tests in Interactive / Headed Mode

To watch the browser navigate and interact in real time:

```bash
pytest tests/ --headed -v
```

### Run Specific Test Modules

```bash
# Authentication & Form Validation
pytest tests/test_auth_selenium.py -v

# Story Feed, Navigation & Reader Modal
pytest tests/test_feed_selenium.py -v

# Side Drawer Settings, Theming & History
pytest tests/test_side_menu_selenium.py -v

# Full End-to-End User Journey
pytest tests/test_e2e_user_journey.py -v
```

## Android App

An Android Studio project is included in the `android/` folder. It is a native WebView wrapper for the hosted Flask app.

For emulator testing with the Flask server running locally, it loads:

```text
http://10.0.2.2:5001
```

After hosting the Flask app, update this value in:

```text
android/app/src/main/res/values/strings.xml
```

Replace `lacuna_url` with your hosted HTTPS URL, then build/run the app from Android Studio.
