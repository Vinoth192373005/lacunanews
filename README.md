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
SECRET_KEY
```

Run the app locally:

```bash
flask --app news run --port 5001
```

Open:

```text
http://127.0.0.1:5001
```

## Deployment

For Render or similar Flask hosting:

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn news:app
```

Set these environment variables in your hosting dashboard:

```bash
SECRET_KEY
```

## Notes

The app uses SQLite by default for local login accounts. On free hosting platforms, local SQLite files may be temporary and can disappear after a redeploy or restart. For a university demo this is usually fine, but for a longer-running app you should move users to a hosted database.

The optional `sentence-transformers` model is not included in `requirements.txt` to keep deployment lighter. If it is not installed, the app automatically falls back to TF-IDF clustering.

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
