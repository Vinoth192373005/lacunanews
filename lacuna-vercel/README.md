# Lacuna Vercel

This project is configured for deployment on Vercel as a Python Serverless application.

## Deploy to Vercel

You can deploy either:
1. The **entire repository root**, or
2. The standalone `lacuna-vercel/` folder.

Both contain the necessary `vercel.json`, `api/index.py` serverless handler, `requirements.txt`, templates, and static assets.

### Environment Variables

Configure the following environment variables in your Vercel Project Settings (**Settings** > **Environment Variables**):

```text
SECRET_KEY       (Random string for session cookies, e.g. python -c "import secrets; print(secrets.token_hex(32))")
NEWSAPI_KEY      (Your NewsAPI API key)
GNEWS_KEY        (Your GNews API key)
DATABASE_URL     (PostgreSQL connection string, e.g. from Neon Postgres)
```

> **Database Note**: For persistent users and history across serverless instances, connect a PostgreSQL database such as **Neon Postgres** (available directly through Vercel Marketplace). If `DATABASE_URL` is omitted, the app safely falls back to `/tmp/lacuna.sqlite3` in serverless memory.

## Architecture

- `api/index.py`: Serverless WSGI entrypoint exposing `app` to `@vercel/python`.
- `vercel.json`: Uses modern Vercel `rewrites` to route all incoming HTTP traffic to `api/index.py`.
- `news.py`: Flask application with threadpool RSS feed fetching, TF-IDF summarization, and safe database lifecycle management.

