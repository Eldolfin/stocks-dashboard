import sqlite3
from pathlib import Path

from flask import send_from_directory  # type: ignore
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash  # type: ignore
from werkzeug.utils import secure_filename  # type: ignore

from src import models
from src.database.auth_repository import AuthRepository

UPLOAD_FOLDER = Path("/database/profile_pictures")

class AuthService:
    def __init__(self) -> None:
        self.auth_repository = AuthRepository()

    def register_user(self, form: models.RegisterForm) -> tuple[dict, int]:
        email = form.email
        password = form.password

        if not email or not password:
            return {"error": "Email and password are required"}, 400

        try:
            hashed_password = generate_password_hash(password)
            profile_picture_path = None

            if form.profile_picture:
                file = form.profile_picture
                if file.filename is None:
                    return {"error": "profile picture should have a filename"}, 401

                if file.filename != "":
                    user_upload_folder = UPLOAD_FOLDER / email
                    user_upload_folder.mkdir(exist_ok=True)
                    filename = secure_filename(file.filename)
                    profile_picture_path = Path(user_upload_folder) / filename
                    file.save(profile_picture_path)
                    # Store relative path in DB
                    profile_picture_path = Path(email) / filename

            self.auth_repository.insert_user(email, hashed_password, profile_picture_path)
        except sqlite3.IntegrityError:
            return {"error": "email already exists"}, 409
        return {}, 201

    def login_user(self, body: models.LoginBody) -> tuple[dict, int]:
        user = self.auth_repository.get_user_by_email(body.email)
        if user and check_password_hash(user[2], body.password):
            user_obj = models.User(id=user[0], email=user[1], profile_picture=user[3])
            login_user(user_obj)
            return {"result": "OK"}, 200
        return models.NotFoundResponse(message="Invalid credentials").dict(), 401

    def get_current_user_info(self) -> tuple[dict, int]:
        return models.UserResponse(email=current_user.email, profile_picture=current_user.profile_picture).dict(), 200

    def logout_current_user(self) -> tuple[dict, int]:
        logout_user()
        return {}, 200

    def upload_profile_picture(self, form: models.ProfilePictureForm) -> tuple[dict, int]:
        file = form.profile_picture
        if file.filename == "":
            return {"error": "No selected file"}, 400
        if file:
            if file.filename is None:
                return {"error": "profile picture should have a filename"}, 401
            user_upload_folder = UPLOAD_FOLDER / current_user.email
            user_upload_folder.mkdir(exist_ok=True)
            filename = secure_filename(file.filename)
            profile_picture_path = user_upload_folder / filename
            file.save(profile_picture_path)
            # Store relative path in DB
            profile_picture_path = Path(current_user.email) / filename
            self.auth_repository.update_profile_picture(current_user.id, profile_picture_path)
            return models.ProfilePictureResponse(
                message="Profile picture updated successfully",
                profile_picture=str(profile_picture_path),
            ).dict(), 200
        return models.NotFoundResponse(message="Something went wrong").dict(), 500

    def get_profile_picture_file(self, path: models.ProfilePicturePathParams) -> Path:
        return send_from_directory(UPLOAD_FOLDER / path.user_email, path.filename)
