from PIL import Image
import pytesseract
import tkinter as tk
from tkinter import filedialog
import json
import os
import cv2
import numpy as np
from fuzzywuzzy import fuzz

config_file_path = "config.json"

if os.path.isfile(config_file_path):
    # Prompt the user to choose whether to use the saved config file or input new file paths
    choice = (
        input(
            "A config file already exists. Do you want to use the saved file paths? (Y/N)"
        )
        .strip()
        .lower()
    )
    if choice == "y":
        # Read the file paths from the config file
        with open(config_file_path) as f:
            config = json.load(f)
            image_folder = config["image_folder"]
            dict_location = config["dict_location"]
    else:
        # Prompt the user to select a folder containing image files
        root = tk.Tk()
        root.withdraw()
        image_folder = filedialog.askdirectory(
            title="Select folder containing image files"
        )

        # Prompt the user for the location of the text file
        dict_location = filedialog.askopenfilename(title="Select dictionary file")

        # Save the file paths to a config file
        config = {"image_folder": image_folder, "dict_location": dict_location}

        with open(config_file_path, "w") as f:
            json.dump(config, f)
else:
    # Prompt the user to select a folder containing image files
    root = tk.Tk()
    root.withdraw()
    image_folder = filedialog.askdirectory(title="Select folder containing image files")

    # Prompt the user for the location of the text file
    dict_location = filedialog.askopenfilename(title="Select dictionary file")

    # Save the file paths to a config file
    config = {"image_folder": image_folder, "dict_location": dict_location}

    with open(config_file_path, "w") as f:
        json.dump(config, f)

# Read the usernames from the text file and create a set
with open(dict_location) as f:
    usernames = set(username.strip().lower() for username in f)

# Set custom Tesseract configuration options
custom_config = r"--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
# custom_config = r"--oem 3 --psm 6"

# Set fuzz matching threshold
threshold = 65

# Loop over the image files in the selected folder
hits = 0
for filename in os.listdir(image_folder):
    # Check that the file is an image
    if filename.endswith((".jpg", ".jpeg", ".png")):
        # Construct the full file path
        image_location = os.path.join(image_folder, filename)

        # Load the image using Pillow
        image = Image.open(image_location)

        # Crop the image
        # We assume that the area to be cropped is known, this is for cropping a source image of 2560x1440
        x1, y1 = 1965, 220
        x2, y2 = 2430, 1138
        cropped_image = image.crop((x1, y1, x2, y2))

        # Convert the cropped image to grayscale
        gray = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_BGR2GRAY)

        # Convert the image back to PIL Image format
        pil_image = Image.fromarray(gray)


        # Extract text from the cropped image using pytesseract with custom configuration
        text = pytesseract.image_to_string(
            pil_image, lang="eng", config=custom_config
        )

        # Convert the extracted text to lowercase
        text = text.lower()

        # Compare the extracted usernames against the set of usernames using fuzzy matching
        extracted_usernames = text.split()
        for extracted_username in extracted_usernames:
            for username in usernames:
                ratio = fuzz.token_sort_ratio(extracted_username, username)
                if  ratio > threshold:
                    hits += 1
                    print(
                        f"ALERT! Possible Match: {username} <-> {extracted_username} [match%={fuzz.token_sort_ratio(extracted_username, username)}]"
                    )

print(f"Found {hits} hits.")
