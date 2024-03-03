import sqlite3


def get_wallpapers(db_path='wallpaper_db.sqlite'):
    """
    Fetches all wallpapers from the database.

    :param db_path: The path to the SQLite database file.
    :return: A list of tuples, each representing a wallpaper record.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute a query to select all records from the wallpapers table
    cursor.execute("SELECT id, description, resolution, image_data FROM wallpapers")

    # Fetch all rows of the query result
    wallpapers = cursor.fetchall()

    # Close the connection to the database
    conn.close()

    return wallpapers
