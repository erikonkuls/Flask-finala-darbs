import sqlite3

def create_visits_db():
    """Create visits database and tables"""
    conn = sqlite3.connect("visits.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_visit_count (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            user_name TEXT,
            total_visits INTEGER DEFAULT 0,
            last_visit TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def record_visit(user_id=None, user_name="anonymous"):
    """Record a user visit to the database"""
    try:
        conn = sqlite3.connect("visits.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM user_visit_count WHERE user_id = ?",
            (user_id,)
        )

        if cursor.fetchone():
            cursor.execute(
                "UPDATE user_visit_count SET total_visits = total_visits + 1, last_visit = CURRENT_TIMESTAMP WHERE user_id = ?",
                (user_id,)
            )
        else:
            if user_id:
                cursor.execute(
                    "INSERT INTO user_visit_count (user_id, user_name, total_visits, last_visit) VALUES (?, ?, 1, CURRENT_TIMESTAMP)",
                    (user_id, user_name)
                )

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error recording visit: {e}")
        return False

def get_user_visits(user_id):
    """Get total visits for a user"""
    try:
        conn = sqlite3.connect("visits.db")
        cursor = conn.cursor()
        cursor.execute("SELECT total_visits, last_visit FROM user_visit_count WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result if result else (0, None)
    except Exception as e:
        print(f"Error getting user visits: {e}")
        return (0, None)

def get_all_user_visits():
    """Get all users and their visit counts"""
    try:
        conn = sqlite3.connect("visits.db")
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, user_name, total_visits, last_visit FROM user_visit_count ORDER BY total_visits DESC")
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"Error getting all user visits: {e}")
        return []

if __name__ == "__main__":
    create_visits_db()
