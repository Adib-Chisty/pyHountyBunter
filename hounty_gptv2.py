from PIL import Image
import pytesseract
import tkinter as tk
from tkinter import filedialog
import json
import os

config_file_path = "config.json"

if os.path.isfile(config_file_path):
    # Prompt the user to choose whether to use the saved config file or input new file paths
    choice = input("A config file already exists. Do you want to use the saved file paths? (Y/N)").strip().lower()
    if choice == "y":
        # Read the file paths from the config file
        with open(config_file_path) as f:
            config = json.load(f)
            image_paths = config["image_paths"]
            dict_location = config["dict_location"]
    else:
        # Prompt the user to select multiple image files
        root = tk.Tk()
        root.withdraw()
        image_paths = filedialog.askopenfilenames(title="Select image files")

        # Prompt the user for the location of the text file
        dict_location = filedialog.askopenfilename(title="Select dictionary file")

        # Save the file paths to a config file
        config = {
            "image_paths": list(image_paths),
            "dict_location": dict_location
        }

        with open(config_file_path, "w") as f:
            json.dump(config, f)
else:
    # Prompt the user to select multiple image files
    root = tk.Tk()
    root.withdraw()
    image_paths = filedialog.askopenfilenames(title="Select image files")

    # Prompt the user for the location of the text file
    dict_location = filedialog.askopenfilename(title="Select dictionary file")

    # Save the file paths to a config file
    config = {
        "image_paths": list(image_paths),
        "dict_location": dict_location
    }

    with open(config_file_path, "w") as f:
        json.dump(config, f)

# Read the usernames from the text file and create a set
with open(dict_location) as f:
    usernames = set([username.strip().lower() for username in f.readlines()])

# Loop over the selected image files
for image_location in image_paths:
    # Load the image using Pillow
    image = Image.open(image_location)

    # Crop the image
    # We assume that the area to be cropped is known
    cropped_image = image.crop((x1, y1, x2, y2))

    # Extract text from the cropped image using pytesseract
    text = pytesseract.image_to_string(cropped_image, lang='eng')

    # Convert the extracted text to lowercase
    text = text.lower()

    # Compare the extracted usernames against the set of usernames
    extracted_usernames = text.split()
    for username in extracted_usernames:
        if username.lower() in usernames:
            print("Username found: " + username)
