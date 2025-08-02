from flask_login import login_user, logout_user, login_required, current_user
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from src.user import User
from src import models
from flask_openapi3 import APIBlueprint, Tag
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/database/profile_pictures'

auth_bp = APIBlueprint('auth', __name__, url_prefix='/api')

auth_tag = Tag(name="auth", description="Authentication endpoints")


@auth_bp.post('/register', tags=[auth_tag])
def register(form: models.RegisterForm):
    email = form.email
    password = form.password

    if not email or not password:
        return {'error': 'Email and password are required'}, 400

    with sqlite3.connect('/database/database.db') as conn:
        cursor = conn.cursor()
        try:
            hashed_password = generate_password_hash(password)
            profile_picture_path = None

            if form.profile_picture:
                file = form.profile_picture
                if file.filename != '':
                    filename = secure_filename(file.filename)
                    profile_picture_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(profile_picture_path)

            cursor.execute("INSERT INTO users (email, password, profile_picture) VALUES (?, ?, ?)",
                           (email, hashed_password, profile_picture_path))
            conn.commit()
        except sqlite3.IntegrityError:
            return {'error': 'email already exists'}, 409
    return {}, 201


@auth_bp.post('/login', tags=[auth_tag])
def login(body: models.LoginBody):
    with sqlite3.connect('/database/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (body.email,))
        user = cursor.fetchone()
        if user and check_password_hash(user[2], body.password):
            user_obj = User(id=user[0], email=user[1], profile_picture=user[3])
            login_user(user_obj)
            return {}, 200
        return {'error': 'Invalid credentials'}, 401


@auth_bp.get('/user', tags=[auth_tag])
@login_required
def get_user():
    return {'email': current_user.email, 'profile_picture': current_user.profile_picture}


@auth_bp.post('/logout', tags=[auth_tag])
@login_required
def logout():
    logout_user()
    return {}, 200


@auth_bp.post('/profile/picture', tags=[auth_tag])
@login_required
def upload_profile_picture(form: models.ProfilePictureForm):
    file = form.profile_picture
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    if file:
        filename = secure_filename(file.filename)
        profile_picture_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(profile_picture_path)
        with sqlite3.connect('/database/database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET profile_picture = ? WHERE id = ?",
                           (profile_picture_path, current_user.id))
            conn.commit()
        return {'message': 'Profile picture updated successfully', 'profile_picture': profile_picture_path}, 200
    return {'error': 'Something went wrong'}, 500
