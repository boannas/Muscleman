import cv2
import numpy as np

# Colors (B, G, R)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def create_blank(width, height, color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in BGR"""
    image = np.zeros((height, width, 3), np.uint8)
    # Fill image with color
    image[:] = color

    return image


def draw_angle_circle_rounded(image):
    # Ellipse parameters
    radius = 100
    axes = (radius, radius)
    angle = 0
    startAngle = 0
    endAngle = 279
    thickness = 10

    # http://docs.opencv.org/modules/core/doc/drawing_functions.html#ellipse
    cv2.ellipse(image,(150,150), axes, angle, startAngle, endAngle, (255,0,255), thickness)


def draw_half_circle_no_round(image):
    # Ellipse parameters
    radius = 100
    axes = (radius, radius)
    angle = 0
    startAngle = 180
    endAngle = 360
    # When thickness == -1 -> Fill shape
    thickness = -1

    # Draw black half circle
    cv2.ellipse(image, (150,150), axes, angle, startAngle, endAngle, BLACK, thickness)

    axes = (radius - 20, radius - 20)
    # Draw a bit smaller white half circle
    cv2.ellipse(image, (150,150), axes, angle, startAngle, endAngle, WHITE, thickness)

# Create new blank 300x150 white image
width, height = 500, 300
image = create_blank(width, height, color=WHITE)
# draw_angle_circle_rounded(image)
draw_half_circle_no_round(image)
cv2.imshow('img',image)
cv2.waitKey(1000000)
# cv2.imwrite('half_circle_rounded.jpg', image)