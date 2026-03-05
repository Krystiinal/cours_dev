import secrets
import sqlite3
from datetime import datetime, timedelta
from functools import wraps

from flask import redirect, request, url_for

# Durée de vie d'une session (30 minutes)
SESSION_LIFETIME = timedelta(minutes=30)


def get_db():
    return sqlite3.connect("db.sqlite")


def generate_session_id():
    """
    Génère un identifiant de session sécurisé.
    secrets.token_hex génère une chaîne aléatoire cryptographiquement sûre.
    """
    return secrets.token_hex(32)  # 64 caractères hexadécimaux


def create_session(user_id: str) -> str:
    """
    Crée une nouvelle session pour un utilisateur.
    Retourne le session_id à stocker dans le cookie.
    """
    session_id = generate_session_id()
    created_at = datetime.now().isoformat()
    expires_at = (datetime.now() + SESSION_LIFETIME).isoformat()

    conn = get_db()
    conn.execute(
        "INSERT INTO sessions (session_id, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
        (session_id, user_id, created_at, expires_at),
    )
    conn.commit()
    conn.close()

    return session_id


def get_session(session_id: str) -> dict | None:
    """
    Récupère les données d'une session.
    Retourne None si la session n'existe pas ou a expiré.
    """
    conn = get_db()
    row = conn.execute(
        "SELECT session_id, user_id, created_at, expires_at FROM sessions WHERE session_id = ?",
        (session_id,),
    ).fetchone()
    conn.close()

    if row is None:
        return None

    session = {
        "session_id": row[0],
        "user_id": row[1],
        "created_at": row[2],
        "expires_at": row[3],
    }

    # Vérifier si la session a expiré
    if datetime.now().isoformat() > session["expires_at"]:
        delete_session(session_id)
        return None

    return session


def delete_session(session_id: str) -> bool:
    """
    Supprime une session (déconnexion).
    Retourne True si la session existait.
    """
    conn = get_db()
    cursor = conn.execute(
        "DELETE FROM sessions WHERE session_id = ?",
        (session_id,),
    )
    conn.commit()
    conn.close()

    return cursor.rowcount > 0


def get_current_user(request) -> str | None:
    """
    Récupère l'utilisateur actuellement connecté à partir de la requête.
    Retourne None si l'utilisateur n'est pas connecté.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None

    session = get_session(session_id)
    if not session:
        return None

    return session["user_id"]


def login_required(f):
    """
    Décorateur qui protège une route.
    Redirige vers /login si l'utilisateur n'est pas connecté.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(url_for("auth.login_page"))
        return f(*args, **kwargs)

    return decorated_function
