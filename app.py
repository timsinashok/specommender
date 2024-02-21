from flask import Flask, render_template, request
from inference_sdk import InferenceHTTPClient
import os

app = Flask(__name__)

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
        api_key="JemAXJ2X7SOptsVPKxrG"
    )

    # Infer using the uploaded image
    result = CLIENT.infer(uploaded_image_path, model_id="face-shape-detection/1")

    # Remove the temporary uploaded image file
    os.remove(uploaded_image_path)

    return render_template('results.html', result=result)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)


