from flask_login import login_user, logout_user, login_required, current_user
import sqlite3
import hashlib
from src.user import User
from src import models
from flask_openapi3 import APIBlueprint, Tag

auth_bp = APIBlueprint('auth', __name__, url_prefix='/api')

auth_tag = Tag(name="auth", description="Authentication endpoints")


@auth_bp.post('/register', tags=[auth_tag])
def register(body: models.RegisterBody):
    with sqlite3.connect('/database/database.db') as conn:
        cursor = conn.cursor()
        try:
            hashed_password = hashlib.sha256(
                body.password.encode()).hexdigest()
            profile_picture = f"https://www.gravatar.com/avatar/{
                hashlib.md5(body.email.encode()).hexdigest()}?d=identicon&s=512"
            cursor.execute("INSERT INTO users (email, password, profile_picture) VALUES (?, ?, ?)",
                           (body.email, hashed_password, profile_picture))
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
        if user and user[2] == hashlib.sha256(body.password.encode()).hexdigest():
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
