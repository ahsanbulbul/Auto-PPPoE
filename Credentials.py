import sqlite3

def get_users(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    c = conn.cursor()

    c.execute("SELECT username, password FROM users")
    users = [dict(row) for row in c.fetchall()]

    conn.close()
    return users

def get_router(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT username, password FROM router WHERE id = 1")
    admin = c.fetchone()

    c.execute("SELECT ssid FROM router WHERE id = 1")
    ssid_row = c.fetchone()
    ssid = ssid_row["ssid"] if ssid_row else None

    conn.close()
    return dict(admin), ssid if admin else None
