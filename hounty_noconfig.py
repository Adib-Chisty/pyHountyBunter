from PIL import Image
import pytesseract
import tkinter as tk
from tkinter import filedialog

# Prompt the user to select multiple image files
root = tk.Tk()
root.withdraw()
image_paths = filedialog.askopenfilenames(title="Select image files")

# Prompt the user for the location of the text file
dict_location = filedialog.askopenfilename(title="Select dictionary file")


# Read the usernames from the text file and create a set
print("Reading usernames from target set...")
with open(dict_location) as f:
    usernames = set([username.strip().lower() for username in f.readlines()])

print("Checking images...")
# Loop over the selected image files
for i, image_location in enumerate(image_paths):
    # Load the image using Pillow
    image = Image.open(image_location)

    # Crop the image
    # We assume that the area to be cropped is known, this is for cropping a source image of 2560x1440
    x1, y1 = 1965, 220
    x2, y2 = 2430, 1138
    cropped_image = image.crop((x1, y1, x2, y2))

    # Set custom Tesseract configuration options
    custom_config = r'--oem 3 --psm 6'

    # Extract text from the cropped image using pytesseract with custom configuration
    text = pytesseract.image_to_string(cropped_image, lang='eng', config=custom_config) 
    text = text.lower()

    # Compare the extracted usernames against the set of usernames
    extracted_usernames = text.split()
    for username in extracted_usernames:
        if username in usernames:
            print("ALERT! Found Hounty: " + username)

print('fin.')

