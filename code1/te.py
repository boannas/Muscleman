import cv2

# Load the foreground (transparent) image
foreground = cv2.imread(r"C:\Users\TADTAWAN\Desktop\work\studio\code1\turtle.png", cv2.IMREAD_UNCHANGED)

# Load the background image on which you want to overlay the foreground
background = cv2.imread(r"C:\Users\TADTAWAN\Pictures\Fibolian\IMG_3467.JPG")

# Get the dimensions of the foreground image
height, width, channels = foreground.shape

# Specify the position where you want to overlay the foreground on the background
x_position = 100  # Adjust this as needed
y_position = 200  # Adjust this as needed

# Create a region of interest (ROI) for the foreground on the background
roi = background[y_position:y_position+height, x_position:x_position+width]

# Combine the foreground and background using alpha blending
for c in range(0, 3):
    roi[:, :, c] = roi[:, :, c] * (1 - foreground[:, :, 3] / 255.0) + foreground[:, :, c] * (foreground[:, :, 3] / 255.0)

# Update the background with the overlaid image
background[y_position:y_position+height, x_position:x_position+width] = roi

# Display or save the result
cv2.imshow('Result', background)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the result to a file
cv2.imwrite('result_image.jpg', background)
