import os
import sqlite3

import flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_openapi3 import Info, OpenAPI

from .auth import UPLOAD_FOLDER, auth_bp
from .stocks import cache, stocks_bp
from .user import User

info = Info(title="stocks API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(
    app,
    origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8085"],
    supports_credentials=True,
)
app.config["UPLOAD_FOLDER"] = "/database/etoro_sheets"
app.config["SECRET_KEY"] = os.environ.get("BACKEND_AUTH_SECRET_KEY")
app.config["CACHE_TYPE"] = "SimpleCache"

cache.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.register_api(auth_bp)
app.register_api(stocks_bp)


print("Initializing database...")
with sqlite3.connect("/database/database.db") as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            profile_picture TEXT
        )
    """)

# Create the profile pictures upload directory if it doesn't exist
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    with sqlite3.connect("/database/database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            return User(id=user[0], email=user[1], profile_picture=user[3])
        return None


def create_app() -> flask.Flask:
    return app
