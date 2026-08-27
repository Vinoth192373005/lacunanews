import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DATABASE_PATH", "/tmp/lacuna.sqlite3")
os.environ.setdefault("VERCEL", "1")

import urllib.parse
from news import app as raw_app


class VercelPathMiddleware:
    """
    Normalizes WSGI PATH_INFO when Vercel serverless rewrites route all paths
    to /api/index (e.g. /, /login, /register, /roundup, /api/cluster, /api/comments, /static/*).
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        target_path = None

        # 1. Check HTTP_X_MATCHED_PATH / HTTP_X_VERCEL_MATCHED_PATH (Vercel edge router)
        for hdr in ("HTTP_X_MATCHED_PATH", "HTTP_X_VERCEL_MATCHED_PATH"):
            val = environ.get(hdr)
            if val:
                val_path = val.split("?")[0]
                if val_path and not val_path.startswith(("/api/index", "/api/index.py")):
                    target_path = "/" + val_path.lstrip("/")
                    break

        # 2. Check x-now-route-matches header (Vercel standard pattern)
        if not target_path and "HTTP_X_NOW_ROUTE_MATCHES" in environ:
            try:
                matches = urllib.parse.parse_qs(environ["HTTP_X_NOW_ROUTE_MATCHES"])
                if "1" in matches and matches["1"]:
                    target_path = "/" + matches["1"][0].lstrip("/")
                elif "0" in matches and matches["0"]:
                    target_path = "/" + matches["0"][0].lstrip("/")
            except Exception:
                pass

        # 3. Check X-Forwarded-Uri / X-Original-Url / REQUEST_URI
        if not target_path:
            for hdr in ("HTTP_X_FORWARDED_URI", "HTTP_X_ORIGINAL_URL", "REQUEST_URI", "RAW_URI"):
                val = environ.get(hdr)
                if val:
                    val_path = val.split("?")[0]
                    if val_path and not val_path.startswith(("/api/index", "/api/index.py")):
                        target_path = "/" + val_path.lstrip("/")
                        break

        # 4. Check __path query parameter if supplied
        query_string = environ.get("QUERY_STRING", "")
        if not target_path and "__path=" in query_string:
            qs_dict = urllib.parse.parse_qs(query_string, keep_blank_values=True)
            if "__path" in qs_dict:
                raw_val = qs_dict.pop("__path")[0]
                target_path = "/" + raw_val.lstrip("/")
                clean_pairs = []
                for k, vlist in qs_dict.items():
                    for v in vlist:
                        clean_pairs.append(f"{urllib.parse.quote(k)}={urllib.parse.quote(v)}")
                environ["QUERY_STRING"] = "&".join(clean_pairs)

        # 5. Fallback on PATH_INFO
        if not target_path:
            path_info = environ.get("PATH_INFO", "")
            if path_info.startswith("/api/index.py/"):
                target_path = "/" + path_info[len("/api/index.py/"):].lstrip("/")
            elif path_info.startswith("/api/index/"):
                target_path = "/" + path_info[len("/api/index/"):].lstrip("/")
            elif path_info in ("/api/index", "/api/index.py", "/api/index.py/"):
                target_path = "/"
            else:
                target_path = path_info or "/"

        environ["PATH_INFO"] = target_path

        return self.wsgi_app(environ, start_response)


# Wrap Flask's underlying WSGI application with the path normalizer
raw_app.wsgi_app = VercelPathMiddleware(raw_app.wsgi_app)
app = raw_app
