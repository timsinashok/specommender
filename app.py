from flask import Flask, render_template, request, redirect, url_for, flash
from inference_sdk import InferenceHTTPClient
from werkzeug.utils import secure_filename
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
        "CREATE TABLE items ( itemId INTEGER PRIMARY KEY, itemName TEXT NOT NULL, itemDescription TEXT, itemPrice REAL NOT NULL, itemFaceType TEXT, imageName TEXT NOT NULL)") 
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
    return render_template('index.html')


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
    


## setup for file UPLoads
UPLOAD_FOLDER = 'assets/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# Ensure the upload folder exists, create if not
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, mode=777, exist_ok=True)
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(UPLOAD_FOLDER))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'itemImage' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['itemImage']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # saving image to the upload folder
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Save other form data and file path to the database
        if file and allowed_file(file.filename):
            item_name = request.form['itemName']
            item_description = request.form['itemDescription']
            item_price = request.form['itemPrice']
            item_face_type = request.form['itemFaceType']
            filename = secure_filename(file.filename)
            # Save other form data and file path to the database
            with sqlite3.connect("database.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO items \
                                (itemName, itemDescription, itemPrice, itemFaceType, imageName) \
                                VALUES (?, ?, ?, ?, ?)",
                               (item_name, item_description, item_price, item_face_type, filename))
                conn.commit()
            return redirect(url_for('main'))
    else:
        return render_template('add_item.html')

# Function to fetch all items from the database
def get_all_items():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
    return items

# Route to display all items
@app.route('/items')
def display_items():
    items = get_all_items()
    return render_template('display_items.html', items=items)

@app.route('/process_input', methods=['POST'])
def process_input():
    input_value = request.json['inputValue']
    # Process the input value here
    print('Received input:', input_value)
    return 'Input received successfully'



if __name__ == '__main__':
    app.run(host="localhost", port=8001, debug=True)




