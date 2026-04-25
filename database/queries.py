from database.db import get_db
from datetime import date, timedelta


def get_user_by_id(user_id):
    """Return basic profile info for a user, or None if not found."""
    conn = get_db()
    row = conn.execute(
        "SELECT name, email, created_at FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    if row is None:
        return None
    from datetime import datetime
    dt = datetime.fromisoformat(row["created_at"])
    member_since = dt.strftime("%B %Y")
    return {
        "name": row["name"],
        "email": row["email"],
        "member_since": member_since,
    }


def get_summary_stats(user_id):
    """Return total spent, transaction count, and top category for a user."""
    conn = get_db()
    row = conn.execute(
        """
        SELECT
            COALESCE(SUM(amount), 0) AS total_spent,
            COUNT(*) AS transaction_count
        FROM expenses
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchone()

    total_spent = row["total_spent"]
    transaction_count = row["transaction_count"]

    if transaction_count == 0:
        conn.close()
        return {"total_spent": 0, "transaction_count": 0, "top_category": "—"}

    top_row = conn.execute(
        """
        SELECT category, SUM(amount) AS cat_total
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
        ORDER BY cat_total DESC
        LIMIT 1
        """,
        (user_id,),
    ).fetchone()

    conn.close()
    return {
        "total_spent": total_spent,
        "transaction_count": transaction_count,
        "top_category": top_row["category"],
    }


def get_recent_transactions(user_id, limit=10):
    """Return the most recent expenses for a user, newest first."""
    conn = get_db()
    rows = conn.execute(
        """
        SELECT date, description, category, amount
        FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC, id DESC
        LIMIT ?
        """,
        (user_id, limit),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_category_breakdown(user_id):
    """Return per-category totals with integer percentages that sum to 100."""
    conn = get_db()
    rows = conn.execute(
        """
        SELECT category AS name, SUM(amount) AS amount
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
        ORDER BY amount DESC
        """,
        (user_id,),
    ).fetchall()
    conn.close()

    if not rows:
        return []

    categories = [{"name": row["name"], "amount": row["amount"]} for row in rows]
    grand_total = sum(c["amount"] for c in categories)

    for c in categories:
        c["pct"] = int(c["amount"] / grand_total * 100)

    # Largest category absorbs rounding remainder so pct values sum to 100
    remainder = 100 - sum(c["pct"] for c in categories)
    categories[0]["pct"] += remainder

    return categories


def get_top_categories_last_6_months(user_id, limit=3):
    """Return the top N categories by spend for the last 6 months."""
    since = (date.today().replace(day=1) - timedelta(days=1)).replace(day=1)
    # go back 6 full months from start of current month
    month = since.month - 5
    year = since.year
    if month <= 0:
        month += 12
        year -= 1
    since_str = f"{year:04d}-{month:02d}-01"

    conn = get_db()
    rows = conn.execute(
        """
        SELECT category AS name, SUM(amount) AS amount
        FROM expenses
        WHERE user_id = ?
          AND date >= ?
        GROUP BY category
        ORDER BY amount DESC
        LIMIT ?
        """,
        (user_id, since_str, limit),
    ).fetchall()
    conn.close()

    if not rows:
        return []

    categories = [{"name": row["name"], "amount": row["amount"]} for row in rows]
    grand_total = sum(c["amount"] for c in categories)
    for c in categories:
        c["pct"] = int(c["amount"] / grand_total * 100)
    remainder = 100 - sum(c["pct"] for c in categories)
    categories[0]["pct"] += remainder
    return categories
