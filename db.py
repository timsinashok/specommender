import sqlite3
import os
import click
from flask import current_app, g
import json

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
                imageName TEXT,
                destination TEXT
            )
        """)
        conn.commit()
        conn.close()


def populate_database():
    if is_database_empty():
        print("Starting with an empty database.......")
        print("Adding data to the database.......")

        # Read item data from the JSON file
        with open("data.json", "r") as json_file:
            items_data = json.load(json_file)

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            
        for item_data in items_data:
            cursor.execute("INSERT INTO items (itemName, itemDescription, itemPrice, itemFaceType, imageName, destination) VALUES (?, ?, ?, ?, ?, ?)",
                    (item_data["itemName"], item_data["itemDescription"], item_data["itemPrice"], item_data["itemFaceType"], item_data["imageName"], item_data['destination']))

        # Commit changes and close connection
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

# Function to check if the database is empty
def is_database_empty():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0]
    return count == 0


def get_items_by_face_type(face_type):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE itemFaceType = ?", (face_type,))
        items = cursor.fetchall()
        
    # Convert the list of tuples to a list of dictionaries
    items_dict = []
    for item in items:
        item_dict = {
            'id': item[0],
            'itemName': item[1],
            'itemDescription': item[2],
            'itemPrice': item[3],
            'itemFaceType': item[4],
            'imageName': item[5],
            'destination': item[6]
        }
        items_dict.append(item_dict)
        
    return items_dict