"""
CodeAlpha Task 3 - Secure Version of the Demo Application
Fixes applied for every issue found in vulnerable_app.py (see README.md).
"""
import os
import sqlite3
import subprocess

import bcrypt

DB_PATH = "users_secure.db"

# --- Fix 1 & 2: Secrets loaded from environment, not hardcoded ---
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
API_KEY = os.environ.get("API_KEY")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, "
        "username TEXT, password TEXT)"
    )
    conn.commit()
    conn.close()


def add_user(username, password):
    # --- Fix 3: Strong hashing (bcrypt) with automatic per-user salt ---
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    conn = sqlite3.connect(DB_PATH)
    # --- Fix 4: Parameterized query, no string interpolation ---
    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed),
    )
    conn.commit()
    conn.close()


def login(username, password):
    conn = sqlite3.connect(DB_PATH)
    # --- Fix 5: Parameterized query here too ---
    cursor = conn.execute(
        "SELECT password FROM users WHERE username=?", (username,)
    )
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return False
    stored_hash = row[0]
    return bcrypt.checkpw(password.encode(), stored_hash)


def ping_host(host):
    # --- Fix 6: No shell, argument passed as a list, basic validation ---
    if not host.replace(".", "").isalnum():
        raise ValueError("Invalid host")
    result = subprocess.run(
        ["ping", "-c", "1", host], capture_output=True, text=True
    )
    return result.stdout


def run_backup(filename):
    # --- Fix 7: No shell, argument passed as a list ---
    subprocess.run(["tar", "-czf", "backup.tar.gz", filename], check=True)


# --- Fix 8: No function exposes secrets. get_debug_info() removed entirely. ---


if __name__ == "__main__":
    init_db()
    add_user("fares", "mypassword123")
    print("User added.")
    print("Login success:", login("fares", "mypassword123"))
