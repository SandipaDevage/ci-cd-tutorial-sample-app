"""Entrypoint for the Vercel staging deployment.

Vercel looks for a top-level ``app`` variable in ``index.py`` and serves it as a
serverless function. Locally, keep using ``flask run`` or ``gunicorn app:app``.
"""
import os

if os.environ.get("VERCEL"):
    # Only /tmp is writable on Vercel, so the SQLite database lives there.
    os.environ.setdefault("DATABASE_URL", "sqlite:////tmp/app.db")

from app import app, db  # noqa: E402
from seed import Seeder  # noqa: E402

# A fresh serverless instance starts with an empty /tmp: create the table and
# seed today's special so /menu has something to return.
db.create_all()
Seeder().populate_database()
