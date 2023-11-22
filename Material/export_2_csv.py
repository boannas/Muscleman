import mediapipe as mp
import cv2
import csv

# Initialize MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

# OpenCV to read video
video = cv2.VideoCapture(r"C:\Users\napat\Downloads\test1.mp4")

# Prepare CSV file to write the keypoints data
csv_file = open('posture_data.csv', mode='w', newline='')
csv_writer = csv.writer(csv_file)

# Read video frame by frame
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Pose
    results = pose.process(frame_rgb)

    # Extract landmarks if any are detected
    if results.pose_landmarks:
        landmarks = []
        for landmark in results.pose_landmarks.landmark:
            landmarks.append((landmark.x, landmark.y, landmark.z, landmark.visibility))

        # Write landmarks to a CSV file
        csv_writer.writerow(landmarks)

# Close the video file and CSV file
video.release()
csv_file.close()
