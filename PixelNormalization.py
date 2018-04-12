from PIL import Image # py -m pip install Pillow
import numpy as np # py -m pip install numpy
from colorsys import hsv_to_rgb, rgb_to_hsv # for converting colors
from random import randrange # for generating random numbers

# things that you can change
r, g, b = 0.299, 0.587, 0.114 # rgb luminance weights, sum should be equal to 1
imagePath = "image.png" # image path.  Supports several file formats such as .jpg, .png etc.

# function to return the luminance value of a pixel (0 < R, G, B < 255)
def luminance(pixel):
	return (r * pixel[0] + g * pixel[1] + b * pixel[2]) / 255.0

# function to normalize the grayscale luminance value of a pixel
def normalize(pixel, k): # pixel RGB info, target luminance
	pixel = list(pixel[0 : 3]) # remove alpha component
	
	# turn a black pixel to something that is not black to avoid division by zero
	if sum(pixel) == 0:
		pixel = [1, 1, 1]
	
	RGB = [x / 255.0 for x in pixel] # pixel in RGB
	HSV = list(rgb_to_hsv(*RGB)) # pixel in HSV
	
	luminance = r * RGB[0] + g * RGB[1] + b * RGB[2] # luminance of the pixel
	newHSV = [HSV[0], HSV[1], HSV[2] * k / luminance] # get new pixel HSV value by normalizing the luminance
	
	# make sure Value is capped to 1, and decrease Saturation accordingly
	if (newHSV[2] > 1):
		H = newHSV[0] # hue
		
		# decrease Saturation
		if (H < 1.0 / 6):
			newHSV[1] = (r + g + b - k) / (b + g - 6 * g * H)
		elif (H < 2.0 / 6):
			newHSV[1] = (r + g + b - k) / (b - r + 6 * r * H) 
		elif (H < 3.0 / 6):
			newHSV[1] = (r + g + b - k) / (r + 3 * b - 6 * b * H)
		elif (H < 4.0 / 6):
			newHSV[1] = (r + g + b - k) / (r - 3 * g + 6 * g * H)
		elif (H < 5.0 / 6):
			newHSV[1] = (r + g + b - k) / (g + 5 * r - 6 * r * H)
		else:
			newHSV[1] = (r + g + b - k) / (g - 5 * b + 6 * b * H)
		
		# Value is capped to 1
		newHSV[2] = 1.0
	
	# get new pixel RGB value
	newRGB = hsv_to_rgb(*newHSV)
	newPixel = tuple([int(x * 255) for x in newRGB] + [255])
	return tuple(newPixel)



# ===== Read image from file =====
extensionIndex = imagePath.find('.') # position of the extension in the string
image = Image.open(imagePath) # load image
pixels = image.load() # load image pixels



# ===== Create new image with normalized luminance for every pixel =====
imageNew = Image.new(image.mode, image.size) # create new image
pixelsNew = imageNew.load() # load new image pixels

# loop through the pixels and set the pixels of the new image
for i in range(imageNew.size[0]):
	print("Editing column", i, "of", imageNew.size[0])
	for j in range(imageNew.size[1]):	
		pixelsNew[i, j] = normalize(pixels[i, j], 0.5)

# show and save new image
imageNew.show()
imageNew.save(imagePath[ : extensionIndex] + '2' + imagePath[extensionIndex : ])
imageNew.close()


# ===== Create new image with randomized color, but keeping the luminance value for each pixel =====
imageNew = Image.new(image.mode, image.size) # create new image
pixelsNew = imageNew.load() # load new image pixels

# loop through the pixels and set the pixels of the new image
for i in range(imageNew.size[0]):
	print("Editing column", i, "of", imageNew.size[0])
	for j in range(imageNew.size[1]):
		randomPixel = [randrange(0, 256) for _ in range(3)] # randomize random pixel
		pixelsNew[i, j] = normalize(randomPixel, luminance(pixels[i, j]))

# show and save new image
imageNew.show()
imageNew.save(imagePath[ : extensionIndex] + '3' + imagePath[extensionIndex : ])
imageNew.close()


# close image
image.close()
