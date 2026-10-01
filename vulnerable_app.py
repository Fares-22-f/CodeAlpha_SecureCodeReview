"""
CodeAlpha Task 3 - Vulnerable Demo Application
WARNING: This file is intentionally insecure for a Secure Code Review
exercise. Do NOT use any of these patterns in real projects.
"""
import hashlib
import os
import sqlite3
import subprocess

DB_PATH = "users.db"

# --- Vulnerability 1: Hardcoded credentials ---
ADMIN_PASSWORD = "admin123"
API_KEY = "FAKE_API_KEY_FOR_DEMO_PURPOSES_ONLY"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, "
        "username TEXT, password TEXT)"
    )
    conn.commit()
    conn.close()


def add_user(username, password):
    # --- Vulnerability 2: Weak hashing algorithm (MD5) ---
    hashed = hashlib.md5(password.encode()).hexdigest()

    conn = sqlite3.connect(DB_PATH)
    # --- Vulnerability 3: SQL Injection (string formatting) ---
    query = f"INSERT INTO users (username, password) VALUES ('{username}', '{hashed}')"
    conn.execute(query)
    conn.commit()
    conn.close()


def login(username, password):
    hashed = hashlib.md5(password.encode()).hexdigest()
    conn = sqlite3.connect(DB_PATH)
    # --- Vulnerability 4: SQL Injection (another instance) ---
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{hashed}'"
    cursor = conn.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result is not None


def ping_host(host):
    # --- Vulnerability 5: Command Injection ---
    command = "ping -c 1 " + host
    output = os.popen(command).read()
    return output


def run_backup(filename):
    # --- Vulnerability 6: shell=True with unsanitized input ---
    subprocess.call(f"tar -czf backup.tar.gz {filename}", shell=True)


def get_debug_info():
    # --- Vulnerability 7: Information disclosure ---
    return {
        "db_path": os.path.abspath(DB_PATH),
        "admin_password": ADMIN_PASSWORD,
        "api_key": API_KEY,
    }


if __name__ == "__main__":
    init_db()
    add_user("fares", "mypassword123")
    print("User added.")
    print("Login success:", login("fares", "mypassword123"))
