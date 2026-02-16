import sqlite3

def create_database():
    conn = sqlite3.connect("./database.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            surname TEXT,
            phone TEXT,
            email TEXT,
            password TEXT
        )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
