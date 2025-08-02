from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, email, profile_picture):
        self.id = id
        self.email = email
        self.profile_picture = profile_picture
