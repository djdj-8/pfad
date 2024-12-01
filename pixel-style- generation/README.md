# Pixel Style Transfer Web Application

This Flask web application allows users to take a photo and receive a stylized version of it in the Pixel style. It utilizes the Dreamshaper model and LoRA (Low-Rank Adaptation) weights for image-to-image translation.

## Prerequisites

- Python 3.x
- Flask
- diffusers
- torch
- PIL
- flask_cors
- os

## Installation

1. Clone the repository:


2. Navigate to the project directory:
cd pixel-style-transfer


3. Install the required dependencies:
pip install -r requirements.txt


## Running the Application

To start the Flask application, run the following command in your terminal:
python app.py


The application will be available at `http://127.0.0.1:5000/`.

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000/`.
2. Press the space bar to take a picture
3. The application will process the image and display the stylized Pixar version.
4. Press q to download the generated image

## Troubleshooting

- If you encounter issues with the LoRA weights file, ensure that it is located in the project directory or update the `lora_weights_path` variable with the correct path.
- If the application does not start, check the terminal for error messages and ensure that all dependencies are correctly installed.