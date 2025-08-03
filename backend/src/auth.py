# ruff: noqa: ANN201

import sqlite3
from pathlib import Path

from flask import send_from_directory
from flask_login import current_user, login_required, login_user, logout_user
from flask_openapi3 import APIBlueprint, Tag
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from src import models
from src.user import User

UPLOAD_FOLDER = Path("/database/profile_pictures")

auth_bp = APIBlueprint("auth", __name__, url_prefix="/api")

auth_tag = Tag(name="auth", description="Authentication endpoints")


@auth_bp.post("/register", tags=[auth_tag])
def register(form: models.RegisterForm):
    email = form.email
    password = form.password

    if not email or not password:
        return {"error": "Email and password are required"}, 400

    with sqlite3.connect("/database/database.db") as conn:
        cursor = conn.cursor()
        try:
            hashed_password = generate_password_hash(password)
            profile_picture_path = None

            if form.profile_picture:
                file = form.profile_picture
                if file.filename != "":
                    user_upload_folder = UPLOAD_FOLDER / email
                    user_upload_folder.makedirs(exist_ok=True)
                    filename = secure_filename(file.filename)
                    profile_picture_path = user_upload_folder / filename
                    file.save(profile_picture_path)
                    # Store relative path in DB
                    profile_picture_path = email / filename

            cursor.execute(
                "INSERT INTO users (email, password, profile_picture) VALUES (?, ?, ?)",
                (email, hashed_password, profile_picture_path),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return {"error": "email already exists"}, 409
    return {}, 201


@auth_bp.post("/login", tags=[auth_tag])
def login(body: models.LoginBody):
    with sqlite3.connect("/database/database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (body.email,))
        user = cursor.fetchone()
        if user and check_password_hash(user[2], body.password):
            user_obj = User(id=user[0], email=user[1], profile_picture=user[3])
            login_user(user_obj)
            return models.LoginResponse(email=user_obj.email, profile_picture=user_obj.profile_picture).dict(), 200
        return models.NotFoundResponse(message="Invalid credentials").dict(), 401


@auth_bp.get("/user", tags=[auth_tag], responses={200: models.UserResponse})
@login_required
def get_user():
    return models.UserResponse(email=current_user.email, profile_picture=current_user.profile_picture).dict(), 200


@auth_bp.post("/logout", tags=[auth_tag], responses={200: None})
@login_required
def logout():
    logout_user()
    return {}, 200


@auth_bp.post(
    "/profile/picture",
    tags=[auth_tag],
    responses={200: models.ProfilePictureResponse, 400: models.NotFoundResponse, 500: models.NotFoundResponse},
)
@login_required
def upload_profile_picture(form: models.ProfilePictureForm):
    file = form.profile_picture
    if file.filename == "":
        return {"error": "No selected file"}, 400
    if file:
        user_upload_folder = UPLOAD_FOLDER / current_user.email
        user_upload_folder.makedirs(exist_ok=True)
        filename = secure_filename(file.filename)
        profile_picture_path = user_upload_folder / filename
        file.save(profile_picture_path)
        # Store relative path in DB
        profile_picture_path = current_user.email / filename
        with sqlite3.connect("/database/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET profile_picture = ? WHERE id = ?", (profile_picture_path, current_user.id))
            conn.commit()
        return models.ProfilePictureResponse(
            message="Profile picture updated successfully",
            profile_picture=profile_picture_path,
        ).dict(), 200
    return models.NotFoundResponse(message="Something went wrong").dict(), 500


@auth_bp.get("/profile/pictures/<user_email>/<filename>", tags=[auth_tag])
def get_profile_picture(path: models.ProfilePicturePathParams):
    return send_from_directory(UPLOAD_FOLDER / path.user_email, path.filename)
