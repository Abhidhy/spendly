import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "spendly.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    # Demo user
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    demo_id = cursor.lastrowid

    demo_expenses = [
        (demo_id, 450.00,  "Food",          "2026-04-01", "Groceries"),
        (demo_id, 120.00,  "Transport",     "2026-04-03", "Metro pass"),
        (demo_id, 1200.00, "Bills",         "2026-04-05", "Electricity bill"),
        (demo_id, 800.00,  "Health",        "2026-04-07", "Pharmacy"),
        (demo_id, 350.00,  "Entertainment", "2026-04-10", "Movie night"),
        (demo_id, 2500.00, "Shopping",      "2026-04-12", "Clothes"),
        (demo_id, 180.00,  "Food",          "2026-04-15", "Restaurant dinner"),
        (demo_id, 95.00,   "Other",         "2026-04-18", "Miscellaneous"),
    ]

    # Abhimanyu — dummy expenses across last 6 months
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Abhimanyu", "abhimanyu@spendly.com", generate_password_hash("abhi1234")),
    )
    abhi_id = cursor.lastrowid

    abhi_expenses = [
        # November 2025
        (abhi_id, 3200.00, "Rent",          "2025-11-01", "Monthly rent"),
        (abhi_id, 650.00,  "Food",          "2025-11-05", "Groceries"),
        (abhi_id, 220.00,  "Transport",     "2025-11-10", "Fuel"),
        # December 2025
        (abhi_id, 3200.00, "Rent",          "2025-12-01", "Monthly rent"),
        (abhi_id, 1800.00, "Shopping",      "2025-12-15", "Winter clothes"),
        (abhi_id, 950.00,  "Food",          "2025-12-20", "Christmas dinner & groceries"),
        (abhi_id, 400.00,  "Entertainment", "2025-12-25", "OTT subscriptions + movie"),
        # January 2026
        (abhi_id, 3200.00, "Rent",          "2026-01-01", "Monthly rent"),
        (abhi_id, 700.00,  "Food",          "2026-01-08", "Groceries"),
        (abhi_id, 1100.00, "Bills",         "2026-01-12", "Electricity + internet"),
        (abhi_id, 500.00,  "Health",        "2026-01-18", "Doctor visit + medicines"),
        # February 2026
        (abhi_id, 3200.00, "Rent",          "2026-02-01", "Monthly rent"),
        (abhi_id, 850.00,  "Food",          "2026-02-07", "Groceries"),
        (abhi_id, 1400.00, "Shopping",      "2026-02-14", "Valentine gifts"),
        (abhi_id, 300.00,  "Transport",     "2026-02-20", "Cab rides"),
        # March 2026
        (abhi_id, 3200.00, "Rent",          "2026-03-01", "Monthly rent"),
        (abhi_id, 780.00,  "Food",          "2026-03-06", "Groceries"),
        (abhi_id, 600.00,  "Health",        "2026-03-14", "Gym membership"),
        (abhi_id, 250.00,  "Entertainment", "2026-03-22", "Concert tickets"),
        # April 2026
        (abhi_id, 3200.00, "Rent",          "2026-04-01", "Monthly rent"),
        (abhi_id, 900.00,  "Food",          "2026-04-05", "Groceries + dining out"),
        (abhi_id, 1300.00, "Bills",         "2026-04-10", "Electricity + water"),
        (abhi_id, 450.00,  "Transport",     "2026-04-18", "Fuel + metro"),
    ]

    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        demo_expenses,
    )
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        abhi_expenses,
    )
    conn.commit()
    conn.close()
