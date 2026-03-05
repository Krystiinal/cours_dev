import os
import sqlite3
import argparse
from datetime import datetime


def get_migration_files():
    files = [f for f in os.listdir("migrations") if f.lower().endswith(".sql")]
    return sorted(files)


def parse_migration(filename):
    with open(f"migrations/{filename}") as f:
        content = f.read()

    if "-- UP" not in content or "-- DOWN" not in content:
        raise ValueError(
            f"{filename} : format invalide, attendu :\n"
            "  -- UP\n"
            "  <sql>\n"
            "  -- DOWN\n"
            "  <sql>"
        )

    parts = content.split("-- DOWN")
    up_sql = parts[0].replace("-- UP", "").strip()
    down_sql = parts[1].strip()

    return {"up": up_sql, "down": down_sql}


def ensure_migrator_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS migrator_version (
            version TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL
        )
    """)
    conn.commit()


def get_version(conn):
    row = conn.execute("SELECT version, applied_at FROM migrator_version").fetchone()
    return row  # (version, applied_at) ou None si aucune migration


def set_version(conn, version):
    applied_at = datetime.now().isoformat()
    conn.execute("DELETE FROM migrator_version")
    conn.execute(
        "INSERT INTO migrator_version (version, applied_at) VALUES (?, ?)",
        (version, applied_at),
    )
    conn.commit()


def execute_command():
    parser = argparse.ArgumentParser(description="Outil de migration SQLite")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("version")
    subparsers.add_parser("status")
    subparsers.add_parser("up")
    subparsers.add_parser("down")
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("name")

    args = parser.parse_args()

    conn = sqlite3.connect("db.sqlite")
    ensure_migrator_table(conn)

    if args.command == "version":
        row = get_version(conn)
        if row:
            print(f"Version actuelle : {row[0]} (appliquée le {row[1]})")
        else:
            print("Aucune migration appliquée.")
    elif args.command == "status":
        current = get_version(conn)
        current_version = current[0] if current else None

        files = get_migration_files()

        print(f"{'Version':<10} {'Fichier':<45} {'Statut'}")
        print("-" * 70)

        for filename in files:
            version = filename[:3]
            if current_version is None or version > current_version:
                statut = "en attente"
            else:
                statut = "appliquée"
            print(f"{version:<10} {filename:<45} {statut}")
    elif args.command == "up":
        current = get_version(conn)
        current_version = current[0] if current else None

        files = get_migration_files()
        pending = [
            f for f in files if current_version is None or f[:3] > current_version
        ]

        if not pending:
            print("Aucune migration en attente.")
        else:
            for filename in pending:
                print(f"Applying {filename}...")
                migration = parse_migration(filename)
                conn.executescript(migration["up"])
                set_version(conn, filename[:3])
                print("  -> OK")
            print(f"\n{len(pending)} migration(s) appliquée(s).")
    elif args.command == "down":
        pass  # TODO
    elif args.command == "create":
        files = get_migration_files()

        if files:
            last_version = int(files[-1][:3])
            next_version = str(last_version + 1).zfill(3)
        else:
            next_version = "001"

        slug = args.name.strip().replace(" ", "_")
        filename = f"{next_version}_{slug}.sql"
        filepath = f"migrations/{filename}"

        with open(filepath, "w") as f:
            f.write("-- UP\n\n-- DOWN\n")

        print(f"Migration créée : {filepath}")
    else:
        parser.print_help()


if __name__ == "__main__":
    execute_command()
