import sqlite3
import os
import click
from flask import current_app, g

# Create the database if it doesn't exist
def create_database():
    if not os.path.exists("database.db"):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                itemName TEXT NOT NULL,
                itemDescription TEXT,
                itemPrice REAL,
                itemFaceType TEXT,
                imageName TEXT
            )
        """)
        conn.commit()
        conn.close()




def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()