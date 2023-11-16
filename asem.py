import cv2
import mediapipe as mp
import numpy as np
import time
import pegion as pg

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

ex_name, er_1, er_2, er_3, L_stg, R_stg= "", "", "", "", "" , ""
L_cnt, R_cnt, velo, prev_st = 0, 0, 0, 0
prev_pos = [0,0]

# Create a gradient background
background = pg.create_gradient_background(1080, 1920, (45, 45, 45),(45, 45, 45))
result_image = pg.create_gradient_rectangle_on_background(background,
                        0, 0, 1080, 200, (7, 25, 82), (8, 131, 149))

# Zoomer configuration
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 786)
start_time = time.time()

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        t = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        try: 
            # Assign landmarks point 
            landmarks = results.pose_landmarks.landmark

            # Result from ex function
            L_cnt, R_cnt, er_1, er_2, er_3, L_stg, R_stg, ex_name = pg.dumbbell_curl(image,L_stg, R_stg, L_cnt, R_cnt, landmarks)
            velo, prev_pos, prev_st = pg.find_velo(landmarks, start_time, prev_pos, prev_st)
        except:
            pass
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(255,216,0), thickness=2, circle_radius=2))
        image = cv2.flip(cv2.rotate(cv2.resize(image,(1408,1080)),cv2.ROTATE_90_COUNTERCLOCKWISE),1)
        result_image = pg.overlay_image(background.copy(), image, 0, 200)
    
        
        
        result_image = pg.disp(result_image, ex_name, L_cnt, R_cnt, er_1, er_2, er_3, start_time, velo,10,L_stg)
        # Display the frame
        cv2.imshow("Camera Video on Background", result_image)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break
# Display the result
cv2.imshow("Background with Image", background)
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
