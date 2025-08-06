import sqlite3
from pathlib import Path


class AuthRepository:
    def __init__(self, db_path: str = "/database/database.db") -> None:
        self.db_path = db_path

    def _execute_query(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def get_user_by_email(self, email: str) -> tuple | None:
        cursor = self._execute_query("SELECT * FROM users WHERE email = ?", (email,))
        return cursor.fetchone()

    def get_user_by_id(self, user_id: int) -> tuple | None:
        cursor = self._execute_query("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

    def insert_user(self, email: str, hashed_password: str, profile_picture_path: Path | None) -> None:
        self._execute_query(
            "INSERT INTO users (email, password, profile_picture) VALUES (?, ?, ?)",
            (email, hashed_password, str(profile_picture_path) if profile_picture_path else None),
        )

    def update_profile_picture(self, user_id: int, profile_picture_path: Path) -> None:
        self._execute_query(
            "UPDATE users SET profile_picture = ? WHERE id = ?",
            (str(profile_picture_path), user_id),
        )
