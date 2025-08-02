import os
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI
import sqlite3
from flask_login import LoginManager
from src.user import User
from src.auth import auth_bp
from src.stocks import stocks_bp, cache

info = Info(title="stocks API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, origins=["http://localhost:3000", "http://localhost:5173"])
app.config["UPLOAD_FOLDER"] = "./etoro_sheets"
# TODO: read from env
app.config["SECRET_KEY"] = 'supersecretkey'
app.config["CACHE_TYPE"] = "SimpleCache"

cache.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.register_api(auth_bp)
app.register_api(stocks_bp)


def init_db():
    with sqlite3.connect("/database/database.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                profile_picture TEXT
            )
        ''')
        conn.commit()


@login_manager.user_loader
def load_user(user_id):
    with sqlite3.connect("/database/database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            return User(id=user[0], email=user[1], profile_picture=user[3])
        return None


def create_app():
    init_db()
    return app
