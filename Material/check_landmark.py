import cv2
import mediapipe as mp

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose

# Load the Pose model
pose = mp_pose.Pose()

# Initialize the webcam
cap = cv2.VideoCapture(0)  # 0 for default camera, you can specify a different camera index if needed

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame with Mediapipe Pose
    results = pose.process(frame)

    # Count the number of detected landmarks
    if results.pose_landmarks:
        num_landmarks = len(results.pose_landmarks.landmark)
    else:
        num_landmarks = 0

    # Draw the landmarks and connections manually
    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            h, w, c = frame.shape
            x, y = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        
        # Draw connections (lines between keypoints)
        for connection in mp_pose.POSE_CONNECTIONS:
            start_point = mp_pose.POSE_CONNECTIONS[connection][0]
            end_point = mp_pose.POSE_CONNECTIONS[connection][1]
            x1, y1 = int(results.pose_landmarks.landmark[start_point].x * w), int(results.pose_landmarks.landmark[start_point].y * h)
            x2, y2 = int(results.pose_landmarks.landmark[end_point].x * w), int(results.pose_landmarks.landmark[end_point].y * h)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Display the landmark count
        cv2.putText(frame, f"Landmarks: {num_landmarks}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Pose Detection', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
