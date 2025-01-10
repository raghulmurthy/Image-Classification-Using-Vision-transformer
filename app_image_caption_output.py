# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 23:34:15 2024

@author: PC
"""




# import requests

# url = 'http://127.0.0.1:5000/predict'
# payload = {"features": [20, 100, 1, 0]}
# response = requests.post(url, json=payload)

# print(response.json())



# import requests

# # Define the URL of the Flask API endpoint
# url = 'http://127.0.0.1:5000/caption'

# # Path to the image you want to caption
# image_path = r"C:\Users\PC\Downloads\srk.jpg"

# # Open the image file in binary mode and send it as part of the request
# with open(image_path, 'rb') as img_file:
#     files = {'image': img_file}  # 'image' is the form field name expected by Flask
#     response = requests.post(url, files=files)

# # Check the response
# if response.status_code == 200:
#     # Parse and print the caption from the response
#     caption = response.json().get('caption', 'No caption found.')
#     print(f'Generated Caption: {caption}')
# else:
#     print(f"Error {response.status_code}: {response.text}")





import requests
import pyttsx3

def fetch_caption(image_path):
    """
    Fetches a caption for the image by sending a POST request to the Flask API.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: The generated caption or an error message.
    """
    url = 'http://127.0.0.1:5000/caption'  # Flask API endpoint

    # Open the image file and send it as part of the POST request
    with open(image_path, 'rb') as img_file:
        files = {'image': img_file}
        response = requests.post(url, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json().get('caption', 'No caption found.')
    else:
        return f"Error {response.status_code}: {response.text}"

def speak_caption(caption):
    """
    Converts text to speech and plays it immediately.

    Args:
        caption (str): The text to be converted to speech.

    Returns:
        None
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
        print(f"An error occurred: {e}")

# Example usage
image_path = r"C:\Users\PC\Downloads\srk.jpg"  # Update with the correct image path
caption = fetch_caption(image_path)

if caption:
    print(f"Generated Caption: {caption}")
    speak_caption(caption)
else:
    print("Failed to fetch caption.")
