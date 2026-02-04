from src.db import get_connection


def add_user(username, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()


def get_user(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password FROM users WHERE username = ?",
            (username,)
        )
        result = cursor.fetchone()
        if result:
            return {
                "id": result[0],
                "username": result[1],
                "password": result[2]
            }
        return None


def user_exists(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM users WHERE username = ?",
            (username,)
        )
        return cursor.fetchone() is not None
