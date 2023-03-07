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
with open(dict_location) as f:
    usernames = set([username.strip() for username in f.readlines()])

# Loop over the selected image files
for image_location in image_paths:
    # Load the image using Pillow
    image = Image.open(image_location)

    # Crop the image
    # We assume that the area to be cropped is known
    cropped_image = image.crop((x1, y1, x2, y2))

    # Extract text from the cropped image using pytesseract
    text = pytesseract.image_to_string(cropped_image, lang='eng')

    # Compare the extracted usernames against the set of usernames
    extracted_usernames = text.split()
    for username in extracted_usernames:
        if username in usernames:
            print("Username found: " + username)
