from PIL import Image # py -m pip install Pillow
import numpy as np # py -m pip install numpy
from colorsys import hsv_to_rgb, rgb_to_hsv

# function to normalize the grayscale luminance value of a pixel
def normalize(pixel):
	pixel = list(pixel[0 : 3]) # remove alpha component
	
	 # turn a black pixel to something that is not black to avoid division by zero
	if sum(pixel) == 0:
		pixel = [1, 1, 1]

	r, g, b = 0.299, 0.587, 0.114 # rgb weights, sum should be equal to 1
	
	RGB = [x / 255.0 for x in pixel] # pixel in RGB
	HSV = list(rgb_to_hsv(*RGB)) # pixel in HSV
	
	weighted = r * RGB[0] + g * RGB[1] + b * RGB[2] # weighted sum
	
	# get new pixel HSV value
	k = 0.50 # target luminance of pixel
	newHSV = [HSV[0], HSV[1], HSV[2] * k / weighted]
	
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

image = Image.open("image.png") # load image
pixels = image.load() # load image pixels

imageNew = Image.new(image.mode, image.size) # create new image
pixelsNew = imageNew.load() # load new image pixels

# loop through the pixels and set the pixels of the new image
rows = imageNew.size[0]
for i in range(rows):
	print("Editing line", i, "of", rows)
	for j in range(imageNew.size[1]):	
		pixelsNew[i, j] = normalize(pixels[i, j])

# show and save new image
imageNew.show()
imageNew.save("image2.png")

# close images
imageNew.close()
image.close()
