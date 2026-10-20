import os

from flask import json, jsonify
from app import app
from app import db
from app.models import Menu

APP_VERSION = "1.1.0"

@app.route('/')
def home():
    return jsonify({ "status": "ok" })

@app.route('/health')
def health():
    """Health check used to confirm the deployed app is up and connected to its database."""
    try:
        db.session.execute('SELECT 1')
        database = "connected"
    except Exception:
        database = "unavailable"
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION,
        # The CD job bakes GIT_COMMIT into the deployed image and checks this value
        # to confirm that the commit it just tested is the one now running.
        "commit": os.environ.get("GIT_COMMIT", "local"),
        "database": database
    })

@app.route('/menu')
def menu():
    today = Menu.query.first()
    if today:
        body = { "today_special": today.name }
        status = 200
    else:
        body = { "error": "Sorry, the service is not available today." }
        status = 404
    return jsonify(body), status
