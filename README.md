# CodeAlpha_SecureCodeReview

Secure code review of an intentionally vulnerable Python application, performed for the CodeAlpha Cyber Security Internship (Task 3).

## Overview
`vulnerable_app.py` is a small demo app (SQLite-based user login + a couple
of OS-interaction helpers) seeded with common real-world vulnerabilities.
It was reviewed using the static analysis tool **Bandit**, followed by a
manual review pass to catch what the tool missed.

## Tooling
- Language: Python 3
- Static analyzer: Bandit (`pip install bandit`)
- Command used: `bandit vulnerable_app.py -f txt -o bandit_report.txt`

## Findings

| # | Vulnerability | Severity | Found by | CWE | Fix |
|---|---|---|---|---|---|
| 1 | Hardcoded admin password | Low | Bandit | CWE-259 | Load from environment variables / secrets manager |
| 2 | Hardcoded API key | — | Manual review only | CWE-798 | Load from environment variables / secrets manager |
| 3 | Weak hashing (MD5) for passwords | High | Bandit | CWE-327 | Use bcrypt or argon2 with per-user salt |
| 4 | SQL Injection in `add_user` | Medium | Bandit | CWE-89 | Use parameterized queries (`?` placeholders) |
| 5 | SQL Injection in `login` | Medium | Bandit | CWE-89 | Use parameterized queries (`?` placeholders) |
| 6 | Command Injection via `os.popen` | High | Bandit | CWE-78 | Use `subprocess.run([...])` with a list, no shell |
| 7 | Command Injection via `shell=True` | High | Bandit | CWE-78 | Use `subprocess.run([...])` with a list, no shell |
| 8 | Plaintext secrets returned by `get_debug_info()` | — | Manual review only | CWE-200 | Never expose secrets through debug/info endpoints |

**Severity count:** 4 High, 2 Medium, 2 Low/unclassified.

## Key takeaway
Bandit's pattern-based detection (B105) flags variable names containing
words like "password", so `ADMIN_PASSWORD` was caught but `API_KEY` was
not, despite being equally sensitive. Static analysis tools catch known
patterns reliably but still need a manual review pass to catch
semantically sensitive data that doesn't match their keyword list.

## Example fix (SQL Injection)

Vulnerable:
    query = f"SELECT * FROM users WHERE username='{username}'"
    cursor = conn.execute(query)

Fixed:
    query = "SELECT * FROM users WHERE username=?"
    cursor = conn.execute(query, (username,))

## Screenshots
See the `screenshots/` folder for the Bandit scan output and report.

## Disclaimer
`vulnerable_app.py` is intentionally insecure and for educational
purposes only. Do not deploy or reuse these patterns.
## Before vs After (Bandit comparison)

| File | High | Medium | Low | Total |
|---|---|---|---|---|
| vulnerable_app.py | 4 | 2 | 2 | 8 |
| secure_app.py | 0 | 0 | ~1 (subprocess import notice) | ~1 |

Fixing the 7 issues Bandit flagged (plus the API key leak it missed)
brought the scan down from 8 findings to effectively zero real
vulnerabilities — the only remaining Low note is an informational
blacklist warning about importing `subprocess` at all, not an actual
flaw in how it's used.

## Files
- `vulnerable_app.py` — intentionally insecure version (for review)
- `secure_app.py` — fixed version applying all recommendations
- `bandit_report.txt` — Bandit output on the vulnerable version
- `bandit_report_secure.txt` — Bandit output on the fixed version
