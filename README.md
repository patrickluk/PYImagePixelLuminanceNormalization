# PYImagePixelLuminanceNormalization

## Introduction
The Python program takes an image as an input and outputs 2 images:

1. Normalize the luminance of every pixel of the image.  The modified image should be invisible in grayscale, or if you turn on grayscale filter on your screen.

Original Picture|Processed Picture|Processed Picture View in Grayscale
---|---|---
![Original Picture](<readme images/image_cat.png>)|![Processed Picture](<readme images/image_cat_normalized_luminance.png>)|![Processed Picture View in Grayscale](<readme images/image_cat_normalized_luminance_grayscale.png>)

2. Randomize the color, but keeping the luminance of every pixel of the image.  The modified image should be very noisy, but if you turn on grayscale filter on your screen, the noise goes away.

Original Picture|Processed Picture|Processed Picture View in Grayscale
---|---|---
![Original Picture](<readme images/image_cat.png>)|![Processed Picture](<readme images/image_cat_randomize_pixels.png>)|![Processed Picture View in Grayscale](<readme images/image_cat_randomize_pixels_grayscale.png>)

## Setup

The program works in Python 3.  Make sure you have `numpy`, `opencv-python` and `Pillow` installed.

    > pip install numpy
    > pip install opencv-python
    > pip install Pillow