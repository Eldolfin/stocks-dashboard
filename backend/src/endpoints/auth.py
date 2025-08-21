from flask import session, redirect, url_for, Response
from flask_openapi3 import APIBlueprint, Tag
import os
from authlib.integrations.flask_client import OAuth
from src.models import NotFoundResponse, ProfilePictureResponse
from src.app import app

oauth = OAuth(app)
authentik = oauth.register(
    name="authentik",
    client_id=os.environ["AUTHENTIK_CLIENT_ID"],
    client_secret=os.environ["AUTHENTIK_CLIENT_SECRET"],
    server_metadata_url=os.environ["AUTHENTIK_METADATA_URL"],
    client_kwargs={"scope": "openid profile email"},
)

auth_bp = APIBlueprint("auth", __name__, url_prefix="/api")
auth_tag = Tag(name="auth", description="Authentication endpoints")


# --- Helpers ---
def login_required(func):
    """Simple decorator to check OAuth session instead of flask-login"""
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return {"error": "unauthorized", "message": "You need to be logged in to access this api!"}, 401
        return func(*args, **kwargs)

    return wrapper


# --- Endpoints ---
@auth_bp.get("/login", tags=[auth_tag])
def login():
    redirect_uri = url_for("auth.auth_callback", _external=True)
    return authentik.authorize_redirect(redirect_uri)


@auth_bp.get("/callback", tags=[auth_tag])
def auth_callback():
    token = authentik.authorize_access_token()
    userinfo = authentik.userinfo()
    session["user"] = userinfo
    session["token"] = token
    return redirect("/")  # or frontend route


@auth_bp.get("/user", tags=[auth_tag])
@login_required
def get_user() -> tuple[dict, int]:
    return session["user"], 200


@auth_bp.post("/logout", tags=[auth_tag], responses={200: None})
@login_required
def logout() -> tuple[dict, int]:
    session.pop("user", None)
    session.pop("token", None)

    logout_url = os.environ.get("AUTHENTIK_LOGOUT_URL")
    if logout_url:
        return redirect(logout_url)
    return {"message": "logged out"}, 200


# Keep profile endpoints intact, just swap in new @login_required
@auth_bp.post(
    "/profile/picture",
    tags=[auth_tag],
    responses={200: ProfilePictureResponse, 400: NotFoundResponse, 500: NotFoundResponse},
)
@login_required
def upload_profile_picture(form):
    from src.services.auth_service import AuthService

    return AuthService().upload_profile_picture(form)


@auth_bp.get("/profile/pictures/<user_email>/<filename>", tags=[auth_tag])
def get_profile_picture(path):
    from src.services.auth_service import AuthService

    return AuthService().get_profile_picture_file(path)
