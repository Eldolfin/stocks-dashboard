from typing import Optional

from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id: int, email: str, profile_picture: Optional[str] = None) -> None:
        self.id = id
        self.email = email
        self.profile_picture = profile_picture
