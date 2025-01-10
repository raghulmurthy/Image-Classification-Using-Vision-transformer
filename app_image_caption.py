# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 01:40:27 2024

@author: PC
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image
import torch
import joblib
import pyttsx3
import os

# Initialize Flask app
app = Flask(__name__)

# Load the model, tokenizer, and feature extractor from the .pkl file
pkl_file_path = './model.pkl'
model_data = joblib.load(pkl_file_path)

model = model_data['model']
tokenizer = model_data['tokenizer']
feature_extractor = model_data['feature_extractor']

# Move the model to the appropriate device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define generation parameters
max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

# Define folder for saving uploaded images
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_caption(image_path):
    # Open and preprocess the image
    image = Image.open(image_path)
    if image.mode != "RGB":
        image = image.convert(mode="RGB")
    
    # Extract features and move to the appropriate device
    pixel_values = feature_extractor(images=[image], return_tensors="pt").pixel_values.to(device)
    
    # Generate caption
    output_ids = model.generate(pixel_values, **gen_kwargs)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
    
    return caption

# Serve the homepage
@app.route('/')
def index():
    return render_template('Image_caption.html')

# Handle image captioning API
@app.route('/caption', methods=['POST'])
def caption():
    try:
        # Ensure an image file is included in the request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        # Save the image temporarily
        image = request.files['image']
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)

        # Generate a caption for the image
        caption = generate_caption(image_path)
        
        # Optionally, speak the caption
        speak_caption(caption)

        return render_template('Image_caption.html', image_path=image.filename, caption=caption)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Function to serve image
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

def speak_caption(caption):
    """
    Converts text to speech and plays it immediately.
    """
    try:
        # Initialize the text-to-speech engine
        engine = pyttsx3.init()
        
        # Set speech rate (optional)
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 50)  # Slowing down the rate
        
        # Set voice (optional, depending on the system configuration)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # Use the first available voice
        
        # Speak the caption
        engine.say(caption)
        
        # Wait for the speech to finish
        engine.runAndWait()
    
    except Exception as e:
        print(f"An error occurred while speaking: {e}")

if __name__ == '__main__':
    app.run(debug=True)
