from flask import Flask, render_template, request
from inference_sdk import InferenceHTTPClient
import json
import os

app = Flask(__name__)

def read_api_key(file_path):
    with open(file_path, 'r') as f:
        secrets = json.load(f)
    return secrets.get('api', {}).get('api_key')

model_api_key = read_api_key('secrets.json')

@app.route('/')
def upload_form():
    return render_template('upload_form.html')

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

if __name__ == '__main__':
    app.run(host="localhost", port=8001, debug=True)


