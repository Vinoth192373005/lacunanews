"""
Helper script to start the Lacuna Flask app on a specified test port.
"""
import sys
import os
import argparse

# Add workspace root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from news import app, init_db

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start Lacuna Test Server")
    parser.add_argument("--port", type=int, default=5001, help="Port to run test server")
    args = parser.parse_args()

    # Initialize isolated SQLite database
    init_db()
    
    print(f"Starting Lacuna Flask server on http://127.0.0.1:{args.port} ...", flush=True)
    app.run(host="127.0.0.1", port=args.port, debug=False, use_reloader=False)
