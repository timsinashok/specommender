from flask import Flask, render_template, request, redirect, url_for
from inference_sdk import InferenceHTTPClient
import json
import os
import sqlite3 

from db import get_db

app = Flask(__name__)

# Initialize the database if it doesn't exist
connect = sqlite3.connect('database.db') 
cursor = connect.cursor()
cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='items'")
if cursor.fetchone()[0] == 0:
    connect.execute(
        "CREATE TABLE items ( itemId INTEGER PRIMARY KEY, itemName TEXT NOT NULL, itemDescription TEXT, itemPrice REAL NOT NULL, itemFaceType TEXT )"
    ) 
connect.close()

# Read the API key from the secrets.json file
def read_api_key(file_path):
    with open(file_path, 'r') as f:
        secrets = json.load(f)
    return secrets.get('api', {}).get('api_key')

model_api_key = read_api_key('secrets.json')


# Define the route for the main page
@app.route('/') 
@app.route('/home') 
def main():
    return render_template('main.html')


@app.route('/', methods=['POST'])
def process_image():
    # Get the uploaded image file from the request
    file = request.files['file']

    # Save the uploaded image to a temporary location
    uploaded_image_path = "uploaded_image.jpg"
    file.save(uploaded_image_path)

    # Initialize the InferenceHTTPClient
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key= model_api_key    )

    # Infer using the uploaded image
    result = CLIENT.infer(uploaded_image_path, model_id="face-shape-detection/1")

    # Remove the temporary uploaded image file
    os.remove(uploaded_image_path)

    class_name = result['predictions'][0]['class']

    return render_template('results.html', result=class_name)

# Define the route for the add_item page
@app.route('/add', methods=['GET', 'POST']) 
def add_item(): 
    if request.method == 'POST': 
        item_name = request.form['itemName'] 
        item_description = request.form['itemDescription'] 
        item_price = request.form['itemPrice']
        item_face_type = request.form['itemFaceType'] 
  
        with sqlite3.connect("database.db") as conn: 
            cursor = conn.cursor() 
            cursor.execute("INSERT INTO items \
                            (itemName, itemDescription, itemPrice, itemFaceType) \
                            VALUES (?, ?, ?, ?)",
                           (item_name, item_description, item_price, item_face_type)) 
            conn.commit() 
        return redirect(url_for('main')) 
    else: 
        return render_template('add_item.html') 

if __name__ == '__main__':
    app.run(host="localhost", port=8001, debug=True)


