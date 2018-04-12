# PYImagePixelLuminanceNormalization
The Python program takes an image as an input and outputs 2 images:

1. normalize the luminance of every pixel of the image.  The modified image should be invisible in grayscale, or if you turn on grayscale filter on your screen.
2. randomize the color, but keeping the luminance of every pixel of the image.  The modified image should be very noisy, but if you turn on grayscale filter on your screen, the noise goes away.

Works in Python 3 or Python 2.  Make sure you have both `Pillow` and `numpy` installed.

    > pip install Pillow
    > pip install numpy
