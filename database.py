import sqlite3

def connect_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users(
        username TEXT,
        password TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS student(
        first_name TEXT,
        last_name TEXT,
        address TEXT)""")

    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users VALUES('admin','1234')")

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect("students.db")