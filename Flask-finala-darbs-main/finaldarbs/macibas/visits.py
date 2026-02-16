import sqlite3
from datetime import datetime

def create_visits_db():
    """Create visits database and tables"""
    conn = sqlite3.connect("visits.db")
    cursor = conn.cursor()

    # Table for tracking individual visits
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_name TEXT,
            route TEXT,
            visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT
        )
    """)

    # Table for visit summary per user
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_visit_count (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            user_name TEXT,
            total_visits INTEGER DEFAULT 0,
            last_visit TIMESTAMP
        )
    """)

    # Table for visit summary per route
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS route_visit_count (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route TEXT UNIQUE,
            total_visits INTEGER DEFAULT 0,
            last_visit TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def record_visit(user_id=None, user_name="anonymous", route="/", ip_address=None):
    """Record a user visit to the database"""
    try:
        conn = sqlite3.connect("visits.db")
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO visit_log (user_id, user_name, route, ip_address) VALUES (?, ?, ?, ?)",
            (user_id, user_name, route, ip_address)
        )
        
        # Update or insert user visit count
        cursor.execute(
            "SELECT id FROM user_visit_count WHERE user_id = ?",
            (user_id,)
        )
        
        if cursor.fetchone():
            # User exists, update count
            cursor.execute(
                "UPDATE user_visit_count SET total_visits = total_visits + 1, last_visit = CURRENT_TIMESTAMP WHERE user_id = ?",
                (user_id,)
            )
        else:
            # New user, insert
            if user_id:
                cursor.execute(
                    "INSERT INTO user_visit_count (user_id, user_name, total_visits, last_visit) VALUES (?, ?, 1, CURRENT_TIMESTAMP)",
                    (user_id, user_name)
                )
        
        # Update or insert route visit count
        cursor.execute(
            "SELECT id FROM route_visit_count WHERE route = ?",
            (route,)
        )
        
        if cursor.fetchone():
            # Route exists, update count
            cursor.execute(
                "UPDATE route_visit_count SET total_visits = total_visits + 1, last_visit = CURRENT_TIMESTAMP WHERE route = ?",
                (route,)
            )
        else:
            # New route, insert
            cursor.execute(
                "INSERT INTO route_visit_count (route, total_visits, last_visit) VALUES (?, 1, CURRENT_TIMESTAMP)",
                (route,)
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


def get_route_visits(route):
    """Get total visits for a route"""
    try:
        conn = sqlite3.connect("visits.db")
        cursor = conn.cursor()
        cursor.execute("SELECT total_visits, last_visit FROM route_visit_count WHERE route = ?", (route,))
        result = cursor.fetchone()
        conn.close()
        return result if result else (0, None)
    except Exception as e:
        print(f"Error getting route visits: {e}")
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


def get_all_route_visits():
    """Get all routes and their visit counts"""
    try:
        conn = sqlite3.connect("visits.db")
        cursor = conn.cursor()
        cursor.execute("SELECT route, total_visits, last_visit FROM route_visit_count ORDER BY total_visits DESC")
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"Error getting all route visits: {e}")
        return []


def get_visit_history(limit=100):
    """Get recent visit history"""
    try:
        conn = sqlite3.connect("visits.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, user_name, route, visit_time, ip_address FROM visit_log ORDER BY visit_time DESC LIMIT ?",
            (limit,)
        )
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"Error getting visit history: {e}")
        return []


if __name__ == "__main__":
    create_visits_db()
