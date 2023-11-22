import cv2
import csv
import numpy as np

# Function to draw the skeleton
def draw_skeleton(frame, landmarks):
    # Define connections between landmarks
    # Update these connections according to your landmarks
    connections = [        
        (0, 1),   # nose to left_eye_inner
        (1, 2),   # left_eye_inner to left_eye
        (2, 3),   # left_eye to left_eye_outer
        (3, 7),   # left_eye_outer to left_ear
        (0, 4),   # nose to right_eye_inner
        (4, 5),   # right_eye_inner to right_eye
        (5, 6),   # right_eye to right_eye_outer
        (6, 8),   # right_eye_outer to right_ear
        (9, 10),  # left_mouth to right_mouth
        (11, 12), # left_shoulder to right_shoulder
        (11, 13), # left_shoulder to left_elbow
        (13, 15), # left_elbow to left_wrist
        (15, 17), # left_wrist to left_pinky
        (15, 19), # left_wrist to left_index
        (15, 21), # left_wrist to left_thumb
        (12, 14), # right_shoulder to right_elbow
        (14, 16), # right_elbow to right_wrist
        (16, 18), # right_wrist to right_pinky
        (16, 20), # right_wrist to right_index
        (16, 22), # right_wrist to right_thumb
        (11, 23), # left_shoulder to left_hip
        (12, 24), # right_shoulder to right_hip
        (23, 24), # left_hip to right_hip
        (23, 25), # left_hip to left_knee
        (25, 27), # left_knee to left_ankle
        (27, 29), # left_ankle to left_heel
        (29, 31), # left_heel to left_foot_index
        (24, 26), # right_hip to right_knee
        (26, 28), # right_knee to right_ankle
        (28, 30), # right_ankle to right_heel
        (30, 32)  # right_heel to right_foot_index
    ]
    for connection in connections:
        start, end = connection
        cv2.line(frame, (int(landmarks[start][0]), int(landmarks[start][1])),
                 (int(landmarks[end][0]), int(landmarks[end][1])), (0, 255, 0), 2)

# Read the CSV file
csv_file = open(r"C:\Users\napat\Documents\GitHub\Muscleman\posture_data.csv", mode='r')
csv_reader = csv.reader(csv_file)

# Create a blank canvas
canvas_height, canvas_width = 800, 800  # Adjust the size as needed
canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

# Process each row in the CSV
for row in csv_reader:
    # Clear the canvas
    canvas[:] = (0, 0, 0)

    landmarks = []

    # Parse each landmark in the row
    for landmark_str in row:
        # Remove parentheses and split by comma
        x, y, z, visibility = landmark_str.strip('()').split(', ')
        landmarks.append((float(x) * canvas_width, float(y) * canvas_height))

    # Draw landmarks and skeleton
    for landmark in landmarks:
        cv2.circle(canvas, (int(landmark[0]), int(landmark[1])), 5, (0, 0, 255), -1)

    draw_skeleton(canvas, landmarks)

    # Display the canvas
    cv2.imshow('Landmarks', canvas)
    if cv2.waitKey(20) & 0xFF == ord('q'):  # Press 'q' to exit
        break

csv_file.close()
cv2.destroyAllWindows()
