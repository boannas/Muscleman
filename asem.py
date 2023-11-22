import cv2
import mediapipe as mp
import numpy as np
import time
import pegion as pg

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
good = cv2.imread(r"C:\Users\napat\Documents\GitHub\Muscleman\image\good.png", cv2.IMREAD_UNCHANGED)
good = cv2.resize(good, (55, 55))
img = good
x= 1
ex_name, er_1, er_2, er_3, L_stg, R_stg, sp= "", "", "", "", "" , "", ""
color_velo = (159,162,53)
x_position, y_position, last_time, stage, cnt, prev, t_L, t_R, time_temp, time_temp_R = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
L_cnt, R_cnt, velo, velo_R, prev_st, prev_pos, prev_pos_R, acc, time_ref = 0, 0, 0, 0, 0, 0, 0, 0, 0


# Create a gradient background
background = pg.create_gradient_background(1080, 1920, (45, 45, 45),(45, 45, 45))
# result_image = pg.create_gradient_rectangle_on_background(background,
#                         0, 0, 1080, 200, (7, 25, 82), (8, 131, 149))

# Zoomer configuration
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 786)
start_time = time.time()

cv2.namedWindow('Muscle man')
cv2.setMouseCallback('Muscle man', pg.handle_mouse_event)

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
        if x == 1 :
            try: 
                # Assign landmarks point 
                landmarks = results.pose_landmarks.landmark

                # Result from ex function
                L_cnt, R_cnt, er_1, er_2, er_3, L_stg, R_stg, ex_name, acc, time_temp, time_temp_R, t_L, t_R = pg.dumbbell_curl(image,L_stg, R_stg, L_cnt, R_cnt, landmarks,time_temp, time_temp_R)
                # velo, velo_R, prev_pos, prev_pos_R, prev_st, vel_l, vel_r = pg.find_velo(landmarks, start_time, prev_pos, prev_pos_R, prev_st, vel_l, vel_r)
            except:
                pass
            
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(255,216,0), thickness=2, circle_radius=2))
            
            image = cv2.flip(cv2.rotate(cv2.resize(image,(1408,1080)),cv2.ROTATE_90_COUNTERCLOCKWISE),1)
            result_image = pg.overlay_image(background.copy(), image, 0, 80)
            
            result_image, L_cnt, R_cnt, prev, cnt, last_time, img, color_velo, x_position, y_position, sp = pg.disp(result_image, ex_name, L_cnt, R_cnt, er_1, er_2, er_3, start_time, acc, t_L, t_R,prev, cnt, last_time, img, color_velo,x_position, y_position, sp)
            # Display the frame
            # result_image = cv2.resize(result_image,(result_image.shape[1]//2,result_image.shape[0]//2))
            cv2.imshow("Muscle man", result_image)
        else :
            try: 
                # Assign landmarks point 
                landmarks = results.pose_landmarks.landmark
                # print(len(landmarks),end='\r')
                # Result from ex function
                # L_cnt, R_cnt, er_1, er_2, er_3, L_stg, R_stg, ex_name, acc, time_temp, time_temp_R, t_L, t_R = pg.dumbbell_curl(image,L_stg, R_stg, L_cnt, R_cnt, landmarks,time_temp, time_temp_R)
                # velo, velo_R, prev_pos, prev_pos_R, prev_st, vel_l, vel_r = pg.find_velo(landmarks, start_time, prev_pos, prev_pos_R, prev_st, vel_l, vel_r)
                time_ref, cal1, cal2 = pg.calibrate(landmarks, time_ref)
                print(cal1 , cal2)
            except:
                pass
            
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(255,216,0), thickness=2, circle_radius=2))
            
            image = cv2.flip(cv2.rotate(cv2.resize(image,(1408,1080)),cv2.ROTATE_90_COUNTERCLOCKWISE),1)
            result_image = pg.overlay_image(background.copy(), image, 0, 200)
            # print(landmarks.
            # Display the frame
            result_image = cv2.resize(result_image,(result_image.shape[1]//2,result_image.shape[0]//2))
            cv2.imshow("Muscle man", result_image)
        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break
# Display the result
# cv2.imshow("Background with Image", background)
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()