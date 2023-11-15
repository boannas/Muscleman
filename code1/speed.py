import cv2
import mediapipe as mp
import math
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

# # Set up screen config
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
prev_pos = [0,0]
start_time = time.time()
st = 0
## Setup mediapipe instance

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        try:
             # Capture the start time
            new_frame_time = time.time()
            
            landmarks = results.pose_landmarks.landmark
            mp_lm = mp_pose.PoseLandmark
            
            L_wrist = [landmarks[mp_lm.LEFT_WRIST.value].x,landmarks[mp_lm.LEFT_WRIST.value].y]
            
            current = round((time.time() - start_time),1)
            if current != st :
                # print(current)
                pos_diff_x =  (L_wrist[0] - prev_pos[0]) * 640
                pos_diff_y = (L_wrist[1] - prev_pos[1]) *480
                dist = math.sqrt(pos_diff_x**2 + pos_diff_y**2)
                # data.append(round(dist,2))
                # if len(data) > 2:
                #     out = sum(data)/len(data)
                #     data = []
                st =current
                prev_pos = L_wrist
                
                # prev_pos = L_wrist
            # print(current,end='\r')
            # print(current//1.5)
            # print(image.shape)
            # print(current//1)
            # print
            # print(current)
            # if current / 0.5 == :
            #     pos_diff_x =  (L_wrist[0] - prev_pos[0]) * 640
            #     pos_diff_y = (L_wrist[1] - prev_pos[1]) *480
            #     
            #     print(current)
            #     st = current
            #     print(dist)
            #     prev_pos = L_wrist

 
            cv2.putText(image, f"Speed : {round(dist,2)} px/ds", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Set the previous frame time to the current time
            

            
            
        except:
            pass


        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(255,216,0), thickness=2, circle_radius=2)
                                        )

        # cv2.imshow('Mediapipe ', image)
        # image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imshow('Mediapipe Feed', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()