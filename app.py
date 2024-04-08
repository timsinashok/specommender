from flask import Flask, render_template, request, redirect, url_for, flash
from inference_sdk import InferenceHTTPClient
from werkzeug.utils import secure_filename
import json
import os
import sqlite3 
import json


# Import the functions from db.py
from db import *

app = Flask(__name__)
app.secret_key = '34242' 

# Create the database if it doesn't exist
create_database()

# Populate the database if it is empty
populate_database()


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


@app.route('/search_result', methods=['POST'])  # Endpoint for form submission
def search_results():
    text_input = request.form['text_input']
    image_file = request.files['image_upload']

    if image_file:  # If an image is uploaded
        uploaded_image_path = "uploaded_image.jpg"
        image_file.save(uploaded_image_path)

        CLIENT = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key=model_api_key  # Replace with your actual API key
        )

        result = CLIENT.infer(uploaded_image_path, model_id="face-shape-detection/1")

        os.remove(uploaded_image_path)
        class_name = result['predictions'][0]['class']

        message = f"Detected face shape: {class_name}. \n  Here are the best suited glasses for you ....." 

        items = get_items_by_face_type(class_name)
        return render_template('results.html', result=message, items=items)

    elif text_input:  # If text input is provided
        if text_input in ['oval', 'round', 'square', 'heart', 'oblong', 'diamond']:
            items = get_items_by_face_type(text_input)
            message = f"Here are the best suited glasses for your face shape: {text_input}"

            return render_template('results.html', result=message, items=items)
    else:
        return "No input provided."


@app.route('/process_input', methods=['POST'])
def process_input():
    input_value = request.json['inputValue']
    # Process the input value here
    print('Received input:', input_value)
    return 'Input received successfully'


## setup for file UPLoads
UPLOAD_FOLDER = 'static/images'
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
            link = request.form['link']
            # Save other form data and file path to the database
            with sqlite3.connect("database.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO items \
                                (itemName, itemDescription, itemPrice, itemFaceType, imageName, destination) \
                                VALUES (?, ?, ?, ?, ?, ?)",
                               (item_name, item_description, item_price, item_face_type, filename, link))
                conn.commit()
                respo = item_name, filename, 'added successfully'
                print(respo)
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host="localhost", port=8001, debug=True)

