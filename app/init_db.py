import sqlite3

def initialize_db(db_path='wallpaper_db.sqlite'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallpapers (
            id INTEGER PRIMARY KEY,
            description TEXT,
            resolution TEXT,
            image_data TEXT
        )
    ''')
    conn.commit()
    conn.close()
