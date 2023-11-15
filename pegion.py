import cv2
import mediapipe as mp
import numpy as np
import time
from PIL import ImageFont, ImageDraw, Image
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_lm = mp_pose.PoseLandmark
font_path = r"C:\Users\napat\Documents\GitHub\Muscleman\Material\Outfit-Bold.ttf"
good = cv2.imread(r"C:\Users\napat\Documents\GitHub\Muscleman\image\good.png", cv2.IMREAD_UNCHANGED)
turtle = cv2.imread(r"C:\Users\napat\Documents\GitHub\Muscleman\image\turtle.png", cv2.IMREAD_UNCHANGED)
rabbit = cv2.imread(r"C:\Users\napat\Documents\GitHub\Muscleman\image\rabbit.png", cv2.IMREAD_UNCHANGED)
    # # Draw turtle
turtle = cv2.resize(turtle, (70, 65))
good = cv2.resize(good, (55, 55))
rabbit = cv2.resize(rabbit, (80, 80))
# Percent = 0

def create_gradient_background(width, height, color1, color2):
    gradient_background = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(width):
        r = int(color1[0] * (width - i) / width + color2[0] * i / width)
        g = int(color1[1] * (width - i) / width + color2[1] * i / width)
        b = int(color1[2] * (width - i) / width + color2[2] * i / width)
        gradient_background[:, i] = [b, g, r]
    return gradient_background

def create_gradient_rectangle_on_background(background, x, y, width, height, color1, color2):
    for i in range(width):
        r = int(color1[0] * (width - i) / width + color2[0] * i / width)
        g = int(color1[1] * (width - i) / width + color2[1] * i / width)
        b = int(color1[2] * (width - i) / width + color2[2] * i / width)
        background[y:y + height, x + i] = [b, g, r]
    return background

def overlay_image(background, overlay, x, y):
    h, w = overlay.shape[:2]
    background[y:y+h, x:x+w] = overlay
    return background

def update_timer(frame,start_time):
    current_time = int(time.time() - start_time)
    time_string = time.strftime('%M:%S', time.gmtime(current_time))
    # cv2.putText(frame, time_string, (455,160), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 3)
    return time_string
    # cv2.imshow("Timer Window", frame)

def find_velo(landmarks, start_time, prev_pos, prev_st):
    L_wrist = [landmarks[mp_lm.LEFT_WRIST.value].x,landmarks[mp_lm.LEFT_WRIST.value].y]
    current = round((time.time() - start_time),1)
    if current != prev_st :
        # print(current)
        pos_diff_x =  (L_wrist[0] - prev_pos[0]) * 640
        pos_diff_y = (L_wrist[1] - prev_pos[1]) *480
        velo = math.sqrt(pos_diff_x**2 + pos_diff_y**2)
        prev_st = current
        prev_pos = L_wrist
        # print(prev_pos)
        return round(velo,2), prev_pos, prev_st

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle

def disp(result_image,ex_name, L_counter, R_counter, er_1,er_2,er_3,start_time,velo,Percent):
    font = ImageFont.truetype(font_path, size=48)
    font2 = ImageFont.truetype(font_path, size=72)
    font3 = ImageFont.truetype(font_path, size=32)

    cv2.circle(result_image,(1000,255),37,(149,131,8),-1)
    x_position = 290  # Adjust this as needed
    y_position =37  # Adjust this as needed
    current = int(time.time() - start_time)
    if velo > 50 :
        img = rabbit
        color_velo = (0,155,255)
    elif velo <10:
        img = turtle
        color_velo = (0,155,255)
    else :
        img = good
        color_velo = (159,162,53)
    draw_half_circle_no_round(result_image,100,(330,80),60,color_velo,(97,49,6))
    draw_half_circle_no_round(result_image,Percent,(115,80),60,(159,162,53),(82,25,7))
    height, width, channels = img.shape
    roi = result_image[y_position:y_position+height, x_position:x_position+width]
    for c in range(0, 3):
        roi[:, :, c] = roi[:, :, c] * (1 - img[:, :, 3] / 255.0) + img[:, :, c] * (img[:, :, 3] / 255.0)
    
    
    pil_img = Image.fromarray(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    draw.text((478, 30), "Time", font=font, fill=(255, 255, 255))
    draw.text((740, 130), "Set", font=font3, fill=(255, 255, 255))
    draw.text((900, 130), "Rep", font=font3, fill=(255, 255, 255))
    draw.text((280, 130), "Speed", font=font3, fill=(255, 255, 255))
    draw.text((50, 130), "Accuracy", font=font3, fill=(255, 255, 255))

    draw.text((750, 35), "1", font=font2, fill=(255, 255, 255))
    draw.text((845, 35), str(L_counter), font=font2, fill=(255, 255, 255))
    draw.text((970, 35), str(R_counter), font=font2, fill=(255, 255, 255))
    draw.text((87, 60), str(Percent), font=font3, fill=(255, 255, 255))
    # draw.text((330, 1700), str(ex_name), font=font2, fill=(255, 255, 255))
    draw.text((330, 1650), er_1, font=font2, fill=(255, 255, 255))
    draw.text((330, 1750), er_2, font=font2, fill=(255, 255, 255))
    draw.text((330, 1850), er_3, font=font2, fill=(255, 255, 255))

    draw.text((994, 223), "i", font=font, fill=(255, 255, 255),align='center')
   
    time_str = update_timer(result_image,start_time)        
    draw.text((438, 80), time_str, font=font2, fill=(255, 255, 255))
    result_image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    return result_image

def draw_half_circle_no_round(image,per,pos,radius, out_color,in_color):

    # Ellipse parameters
    axes = (radius-5, radius-5)
    angle = 0
    startAngle = -90
    endAngle = (per/100*360) + startAngle
    # When thickness == -1 -> Fill shape
    thickness = -1

    # Draw black half circle
    cv2.ellipse(image, pos, axes, angle, startAngle, endAngle, out_color, thickness)
# (159,162,53)
    axes = (radius - 20, radius - 20)
    # Draw a bit smaller white half circle
    cv2.ellipse(image, pos, axes, angle, startAngle, endAngle+1, in_color, thickness)

def dumbbell_curl(image, stage, R_stage, counter, R_counter,landmarks):
    ex = "Dumbbell curl"
    # Left parts
    L_shoulder = [landmarks[mp_lm.LEFT_SHOULDER.value].x,landmarks[mp_lm.LEFT_SHOULDER.value].y]
    L_elbow = [landmarks[mp_lm.LEFT_ELBOW.value].x,landmarks[mp_lm.LEFT_ELBOW.value].y]
    L_wrist = [landmarks[mp_lm.LEFT_WRIST.value].x,landmarks[mp_lm.LEFT_WRIST.value].y]
    L_hip = [landmarks[mp_lm.LEFT_HIP.value].x,landmarks[mp_lm.LEFT_HIP.value].y]
    
    # Right parts
    R_shoulder = [landmarks[mp_lm.RIGHT_SHOULDER.value].x,landmarks[mp_lm.RIGHT_SHOULDER.value].y]
    R_elbow = [landmarks[mp_lm.RIGHT_ELBOW.value].x,landmarks[mp_lm.RIGHT_ELBOW.value].y]
    R_wrist = [landmarks[mp_lm.RIGHT_WRIST.value].x,landmarks[mp_lm.RIGHT_WRIST.value].y]
    R_hip = [landmarks[mp_lm.RIGHT_HIP.value].x,landmarks[mp_lm.RIGHT_HIP.value].y]
    
    # Different of shoulder pos Y
    dif_shoulder = (L_shoulder[0] - R_shoulder[0]) *100

    # Calculate angle
    angle_L_arm = calculate_angle(L_shoulder, L_elbow, L_wrist)
    angle_L_body = calculate_angle(L_elbow,L_shoulder,L_hip)
    angle_R_arm = calculate_angle(R_shoulder,R_elbow,R_wrist)
    angle_R_body = calculate_angle(R_elbow,R_shoulder,R_hip)

    if abs(dif_shoulder) < 2:
        e3 = "Neutral"
        
    elif dif_shoulder > 0 :
        e3 = "L Rising"
        cv2.circle(image,tuple(np.multiply(L_shoulder, [1024, 768]).astype(int)),8,(0,0,255),15)
    else :
        e3 = "R Rising"
        cv2.circle(image,tuple(np.multiply(R_shoulder, [1024, 768]).astype(int)),8,(0,0,255),15)
        
    if angle_L_body > 30:
        e1 = "Left Error"
    else :
        e1 = ""        
        
    if angle_R_body > 30:
        e2 = "Right Error"
    else :
        e2 = ""
        
    if angle_L_arm > 160:
        stage = "down"
    elif angle_L_arm < 30 and stage =='down':
        stage="up"
        counter +=1
                
    if angle_R_arm > 160:
        R_stage = "R_down"
    elif angle_R_arm < 30 and R_stage =='R_down':
        R_stage="R_up"
        R_counter +=1
    return counter, R_counter, e1, e2, e3, stage, R_stage, ex

def lateral_raises(image, stage, R_stage, counter, R_counter,landmarks):

    ex = "lateral raises"

    # Left parts
    L_shoulder = [landmarks[mp_lm.LEFT_SHOULDER.value].x,landmarks[mp_lm.LEFT_SHOULDER.value].y]
    L_elbow = [landmarks[mp_lm.LEFT_ELBOW.value].x,landmarks[mp_lm.LEFT_ELBOW.value].y]
    L_wrist = [landmarks[mp_lm.LEFT_WRIST.value].x,landmarks[mp_lm.LEFT_WRIST.value].y]
    L_hip = [landmarks[mp_lm.LEFT_HIP.value].x,landmarks[mp_lm.LEFT_HIP.value].y]
    
    # Right parts
    R_shoulder = [landmarks[mp_lm.RIGHT_SHOULDER.value].x,landmarks[mp_lm.RIGHT_SHOULDER.value].y]
    R_elbow = [landmarks[mp_lm.RIGHT_ELBOW.value].x,landmarks[mp_lm.RIGHT_ELBOW.value].y]
    R_wrist = [landmarks[mp_lm.RIGHT_WRIST.value].x,landmarks[mp_lm.RIGHT_WRIST.value].y]
    R_hip = [landmarks[mp_lm.RIGHT_HIP.value].x,landmarks[mp_lm.RIGHT_HIP.value].y]

    # Different of shoulder pos Y
    dif_shoulder = (L_shoulder[0] - R_shoulder[0]) *100

    # Calculate angle
    angle_L_arm = calculate_angle(L_shoulder, L_elbow, L_wrist)
    angle_L_body = calculate_angle(L_elbow,L_shoulder,L_hip)
    angle_R_arm = calculate_angle(R_shoulder,R_elbow,R_wrist)
    angle_R_body = calculate_angle(R_elbow,R_shoulder,R_hip)
    if abs(dif_shoulder) < 2:
        e3 = "Neutral"
        
    elif dif_shoulder > 0 :
        e3 = "L Rising"
        cv2.circle(image,tuple(np.multiply(L_shoulder, [1024, 768]).astype(int)),8,(0,0,255),15)
    else :
        e3 = "R Rising"
        cv2.circle(image,tuple(np.multiply(R_shoulder, [1024, 768]).astype(int)),8,(0,0,255),15)
        
    if angle_L_body < 30:
        stage = "down"
    elif angle_L_body > 85 and stage =='down':
        stage="up"
        counter +=1
    if angle_L_arm < 160 :
        e1 = "Left Arm Error"    
    if angle_L_body > 110 and stage == 'up':
        e1 = "Left too high"
    
    if angle_R_body < 30:
        R_stage = "down"
    elif angle_R_body > 85 and R_stage =='down':
        R_stage="up"
        R_counter +=1
    if angle_R_arm < 160 :
        e2 = "Right Arm Error"
    if angle_R_body > 110 and R_stage == 'up':
        e2 = "Right to high"
    return counter, R_counter,e1,e2, e3, stage, R_stage, ex
    
def seated_press(image, stage, R_stage, counter, R_counter, landmarks):
    
    ex = "seated press"

    # Left parts
    L_shoulder = [landmarks[mp_lm.LEFT_SHOULDER.value].x,landmarks[mp_lm.LEFT_SHOULDER.value].y]
    L_elbow = [landmarks[mp_lm.LEFT_ELBOW.value].x,landmarks[mp_lm.LEFT_ELBOW.value].y]
    L_wrist = [landmarks[mp_lm.LEFT_WRIST.value].x,landmarks[mp_lm.LEFT_WRIST.value].y]
    L_hip = [landmarks[mp_lm.LEFT_HIP.value].x,landmarks[mp_lm.LEFT_HIP.value].y]
    
    # Right parts
    R_shoulder = [landmarks[mp_lm.RIGHT_SHOULDER.value].x,landmarks[mp_lm.RIGHT_SHOULDER.value].y]
    R_elbow = [landmarks[mp_lm.RIGHT_ELBOW.value].x,landmarks[mp_lm.RIGHT_ELBOW.value].y]
    R_wrist = [landmarks[mp_lm.RIGHT_WRIST.value].x,landmarks[mp_lm.RIGHT_WRIST.value].y]
    R_hip = [landmarks[mp_lm.RIGHT_HIP.value].x,landmarks[mp_lm.RIGHT_HIP.value].y]

    # Different of shoulder pos Y
    dif_shoulder = (L_shoulder[0] - R_shoulder[0]) *100

    # Calculate angle
    angle_L_arm = calculate_angle(L_shoulder, L_elbow, L_wrist)
    angle_L_body = calculate_angle(L_elbow,L_shoulder,L_hip)
    angle_R_arm = calculate_angle(R_shoulder,R_elbow,R_wrist)
    angle_R_body = calculate_angle(R_elbow,R_shoulder,R_hip)
    
    if abs(dif_shoulder) < 2:
        e3 = "Neutral"
        
    elif dif_shoulder > 0 :
        e3 = "L Rising"
        cv2.circle(image,tuple(np.multiply(L_shoulder, [768, 1024]).astype(int)),10,(0,0,255),15)
    else :
        e3 = "R Rising"
        cv2.circle(image,tuple(np.multiply(R_shoulder, [768, 1024]).astype(int)),10,(0,0,255),15)
        
    if angle_L_body < 85 :
        stage = "down"
    elif angle_L_body > 155 and stage =='down':
        stage="up"
        counter +=1
    if angle_L_arm < 150 and angle_L_body >160:
        e1 = "Left Arm Error"   
    
    if angle_R_body < 85:
        R_stage = "down"
    elif angle_R_body > 155 and R_stage =='down':
        R_stage="up"
        R_counter +=1
    if angle_R_arm < 150 and angle_R_body >160:
        e2 = "Right Arm Error"  
        
    return counter, R_counter,e1,e2, e3, stage, R_stage, ex