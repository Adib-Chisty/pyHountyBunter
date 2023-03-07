pyHountyBunter
----------------------------------------

This Python app allows you to extract text information from multiple images and compare it against a set of usernames stored in a text file.

### Requirements

To run this app, you need to have the following Python packages installed:

*   Pillow
*   pytesseract
*   tkinter

### Usage

1.  Launch the app by running the script in a Python environment that has the required packages installed.
    
2.  When prompted, select one or more image files that contain the text information you want to extract.
    
3.  When prompted, select a text file that contains a list of usernames, with one username per line. This file will be used to compare against the extracted usernames.
    
4.  The app will then loop over the selected image files, crop them, and extract text information using the pytesseract library.
    
5.  The extracted text information will be compared against the list of usernames in the text file. If a match is found, the username will be displayed in the console output.
    

Note that the accuracy of the text extraction depends on the quality of the images and the clarity of the text. If the images are of low resolution or the text is blurry, the extracted text may not be accurate. Additionally, if the text has unusual fonts or is distorted, the text extraction accuracy may be affected.

### Important Note

The code assumes that the area to be cropped from the image is known, and that the cropping coordinates are fixed. This means that the code may not work correctly with images of different resolutions or aspect ratios.

To ensure that the code works correctly with your images, it's necessary to edit the cropping coordinates based on the resolution and aspect ratio of the images being processed. The specific coordinates will depend on the location and size of the area containing the text information to be extracted.

We recommend that users carefully review the code and adjust the cropping coordinates to match the area containing the text in their specific images. This can be done by modifying the values of `x1`, `y1`, `x2`, and `y2` in the `image.crop()` method.

### License

This code is released under the MIT License. Please see the LICENSE file for details.
