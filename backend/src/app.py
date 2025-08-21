import os
import sqlite3

import flask
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI


info = Info(title="stocks API", version="1.0.0")
app = OpenAPI(__name__, info=info, doc_prefix="/api/openapi", doc_url="/openapi.json")

CORS(
    app,
    origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8085",
        "https://wsb.eldolfin.top",
        "http://tauri.localhost",
    ],
    supports_credentials=True,
)
app.config["UPLOAD_FOLDER"] = "/database/etoro_sheets"
app.config["SECRET_KEY"] = os.environ.get("BACKEND_AUTH_SECRET_KEY")
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 0


from .endpoints.auth import auth_bp
from .endpoints.compare import compare_bp
from .endpoints.stocks import cache, stocks_bp
from .models import User

cache.init_app(app)

app.register_api(auth_bp)
app.register_api(compare_bp)
app.register_api(stocks_bp)


print("Initializing database...")
with sqlite3.connect("/database/database.db") as conn:
    # TODO: create tables here
    pass


def create_app() -> flask.Flask:
    return app
