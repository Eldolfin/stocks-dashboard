from pathlib import Path

from flask_login import login_required
from flask_openapi3 import APIBlueprint, Tag

from . import models
from .services.auth_service import AuthService, UPLOAD_FOLDER

auth_bp = APIBlueprint("auth", __name__, url_prefix="/api")

auth_tag = Tag(name="auth", description="Authentication endpoints")

auth_service = AuthService()


@auth_bp.post("/register", tags=[auth_tag])
def register(form: models.RegisterForm) -> tuple[dict, int]:
    return auth_service.register_user(form)


@auth_bp.post("/login", tags=[auth_tag])
def login(body: models.LoginBody) -> tuple[dict, int]:
    return auth_service.login_user(body)


@auth_bp.get("/user", tags=[auth_tag], responses={200: models.UserResponse})
@login_required
def get_user() -> tuple[dict, int]:
    return auth_service.get_current_user_info()


@auth_bp.post("/logout", tags=[auth_tag], responses={200: None})
@login_required
def logout() -> tuple[dict, int]:
    return auth_service.logout_current_user()


@auth_bp.post(
    "/profile/picture",
    tags=[auth_tag],
    responses={200: models.ProfilePictureResponse, 400: models.NotFoundResponse, 500: models.NotFoundResponse},
)
@login_required
def upload_profile_picture(form: models.ProfilePictureForm) -> tuple[dict, int]:
    return auth_service.upload_profile_picture(form)


@auth_bp.get("/profile/pictures/<user_email>/<filename>", tags=[auth_tag])
def get_profile_picture(path: models.ProfilePicturePathParams) -> Path:
    return auth_service.get_profile_picture_file(path)
