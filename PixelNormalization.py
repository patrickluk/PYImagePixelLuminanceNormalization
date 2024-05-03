from PIL import Image  # py -m pip install Pillow
import numpy as np  # py -m pip install numpy
import cv2

# image path.  Supports several file formats such as .jpg, .png etc.
IMAGE_PATH = "image.png"

# BGR luminance weights, sum should be equal to 1 for all channels
LUMINANCE_WEIGHTS = np.array([0.114, 0.587, 0.299])

# used for avoiding division by zero
EPSILON = 1e-10


# gets a new image that normalizes the grayscale luminance value for each pixel of the image
def scale_rgb(image):
    # calculate the target luminance for each pixel
    target_luminance = np.min(LUMINANCE_WEIGHTS)

    # add a small epsilon to each pixel channel so it does not result in divide by zero
    adjusted_image = image + EPSILON

    # calculate the current luminance for each pixel
    current_luminance = np.tensordot(adjusted_image, LUMINANCE_WEIGHTS, axes=([2], [0]))

    # calculate the scale that need to be applied to current pixels
    luminance_scale = (target_luminance / current_luminance)[:, :, np.newaxis]

    # adjust the BGR channels based on the luminance difference
    adjusted_image = (adjusted_image * luminance_scale * 255.0).astype(np.uint8)

    return adjusted_image


# gets a new image that randomizes the pixel colors for each pixel of the image, but keeping the same luminance
def randomize_rgb(image):
    # calculate the target luminance for each pixel
    target_luminance = np.tensordot(image / 255.0, LUMINANCE_WEIGHTS, axes=([2], [0]))

    # generate a new adjusted image
    adjusted_image = np.zeros(image.shape)

    # randomize B channel.  Make sure the target luminance can be met
    b_minimum = (target_luminance - np.sum(LUMINANCE_WEIGHTS[1:])) / LUMINANCE_WEIGHTS[
        0
    ]
    b_maximum = target_luminance / LUMINANCE_WEIGHTS[0]
    b_range = np.clip(np.stack((b_minimum, b_maximum), axis=2), 0.0, 1.0)
    adjusted_image[:, :, 0] = np.random.uniform(b_range[..., 0], b_range[..., 1])

    # randomize G channel.  Make sure the target luminance can be met
    g_minimum = (
        target_luminance
        - adjusted_image[:, :, 0] * LUMINANCE_WEIGHTS[0]
        - LUMINANCE_WEIGHTS[2]
    ) / LUMINANCE_WEIGHTS[1]
    g_maximum = (
        target_luminance - adjusted_image[:, :, 0] * LUMINANCE_WEIGHTS[0]
    ) / LUMINANCE_WEIGHTS[1]
    g_range = np.clip(np.stack((g_minimum, g_maximum), axis=2), 0.0, 1.0)
    adjusted_image[:, :, 1] = np.random.uniform(g_range[..., 0], g_range[..., 1])

    # the R channel is determined because the target luminance must be met
    adjusted_image[:, :, 2] = (
        target_luminance
        - np.sum(
            adjusted_image[..., :2] * LUMINANCE_WEIGHTS[np.newaxis, np.newaxis, :2],
            axis=2,
        )
    ) / LUMINANCE_WEIGHTS[2]

    # scale the image pixels
    adjusted_image = (adjusted_image * 255.0).astype(np.uint8)

    return adjusted_image


# load the BGR image
extension_index = IMAGE_PATH.find(".")  # position of the extension in the string
image = cv2.imread(IMAGE_PATH)

# create new image with normalized luminance for every pixel
normalized_luminance_image = scale_rgb(image)
normalized_luminance_image_path = (
    f"{IMAGE_PATH[:extension_index]}_normalized_luminance{IMAGE_PATH[extension_index:]}"
)
cv2.imwrite(normalized_luminance_image_path, normalized_luminance_image)
preview_image = Image.open(normalized_luminance_image_path)  # load image
preview_image.show()
preview_image.close()

# create new image with normalized luminance for every pixel
randomize_pixels_image = randomize_rgb(image)
randomize_pixels_image_path = (
    f"{IMAGE_PATH[:extension_index]}_randomize_pixels{IMAGE_PATH[extension_index:]}"
)
cv2.imwrite(randomize_pixels_image_path, randomize_pixels_image)
preview_image = Image.open(randomize_pixels_image_path)  # load image
preview_image.show()
preview_image.close()
