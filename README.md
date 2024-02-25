# Specommender (Under construction ....... )

This is a Flask-based web application for spectacles and sunglasses recommendations based on face type. Users can upload images of their faces or use the camera of their system to take a picture and get recommendations on glasses. The app also provides an admin view where the admin can upload new items to the database of the application.  
## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/timsinashok/specommender.git
   ```

2. Navigate to the project directory:
   ```bash
   cd specommender
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```bash
   python app.py
   ```

5. Open a web browser and navigate to [http://localhost:8001](http://localhost:8001) to access the application.
<!--
## Usage

- Add items: Navigate to the `/add` route to add items. Fill in the required fields including item name, description, price, and face type, and upload an image.
- View items: Navigate to the `/items` route to view all items stored in the database.
- Upload images: The application allows users to upload images for each item. Supported image formats include PNG, JPG, and JPEG.

## Features

- Add new items with descriptions, prices, face types, and images.
- Upload images for each item.
- View all items stored in the database.
- User-friendly interface for easy navigation and interaction.
-->
## Technologies Used

- **Flask**: Micro web framework for building web applications in Python.
- **SQLite**: Lightweight relational database management system used for storing item data.
- **HTML/CSS**: Frontend technologies for building user interfaces and styling web pages.
- **Werkzeug**: WSGI utility library for handling HTTP requests and responses.
- **Python**: Programming language used for backend development.
- **Roboflow API**: API to recognize face type from the image.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your suggested changes.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.
