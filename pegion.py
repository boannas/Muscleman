import cv2
import mediapipe as mp
import numpy as np
import time
from PIL import ImageFont, ImageDraw, Image

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_lm = mp_pose.PoseLandmark

# Change path of font and image here kub isus
font_path = r"C:\Users\napat\Documents\GitHub\Muscleman\Material\Outfit-Bold.ttf"
font_pathReg = r"C:\Users\napat\Documents\GitHub\Muscleman\Material\Outfit-Regular.ttf"
font = ImageFont.truetype(font_path, size=48)
font2 = ImageFont.truetype(font_path, size=72)
font3 = ImageFont.truetype(font_pathReg, size=32)
font4 = ImageFont.truetype(font_pathReg, size=40)

# good = cv2.imread(r"C:\Users\napat\Documents\GitHub\Muscleman\image\good.png", cv2.IMREAD_UNCHANGED)
# turtle = cv2.imread(r"C:\Users\napat\Documents\GitHub\Muscleman\image\turtle.png", cv2.IMREAD_UNCHANGED)
# rabbit = cv2.imread(r"C:\Users\napat\Documents\GitHub\Muscleman\image\rabbit.png", cv2.IMREAD_UNCHANGED)

# turtle = cv2.resize(turtle, (65, 65))
# good = cv2.resize(good, (55, 55))
# rabbit = cv2.resize(rabbit, (80, 80))

buttons = [
(600, 1500, 500, 100, "Button 1"),
# (250, 100, 100, 40, "Button 2"),
]

buttons_clicked = set()

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

def find_velo(landmarks, start_time, prev_pos, prev_pos_R, prev_st,velo_list, velo_list2):
    # L_wrist = [landmarks[mp_lm.LEFT_WRIST.value].x,landmarks[mp_lm.LEFT_WRIST.value].y]
    # R_wrist = [landmarks[mp_lm.RIGHT_WRIST.value].x,landmarks[mp_lm.RIGHT_WRIST.value].y]
    # current = int(time.time() - start_time)
    # print(R_wrist[0]*1408,R_wrist[1]*1080,end='\r')
    # if current != prev_st :
    #     # print(current)
    #     pos_diff_x =  (L_wrist[0] - prev_pos[0]) * 640
    #     pos_diff_y = (L_wrist[1] - prev_pos[1]) *480
    #     velo = math.sqrt(pos_diff_x**2 + pos_diff_y**2)
    #     prev_st = current
    #     prev_pos = L_wrist
        
    #     return round(velo,2), prev_pos, prev_st
    L_shoulder = [landmarks[mp_lm  .LEFT_SHOULDER.value].x,landmarks[mp_lm.LEFT_SHOULDER.value].y]
    L_elbow = [landmarks[mp_lm.LEFT_ELBOW.value].x,landmarks[mp_lm.LEFT_ELBOW.value].y]
    L_wrist = [landmarks[mp_lm.LEFT_WRIST.value].x,landmarks[mp_lm.LEFT_WRIST.value].y]
    
    R_shoulder = [landmarks[mp_lm.RIGHT_SHOULDER.value].x,landmarks[mp_lm.RIGHT_SHOULDER.value].y]
    R_elbow = [landmarks[mp_lm.RIGHT_ELBOW.value].x,landmarks[mp_lm.RIGHT_ELBOW.value].y]
    R_wrist = [landmarks[mp_lm.RIGHT_WRIST.value].x,landmarks[mp_lm.RIGHT_WRIST.value].y]
    
    angle_L_arm = calculate_angle(L_shoulder, L_elbow, L_wrist)
    angle_R_arm = calculate_angle(R_shoulder, R_elbow, R_wrist)
    current = round((time.time() - start_time),1)
    if current != prev_st :
        velo = int(abs(angle_L_arm - prev_pos))
        velo_list.append(velo)
        velo = int(abs(angle_R_arm - prev_pos_R))
        velo_list2.append(velo)
        prev_st = current
        prev_pos = angle_L_arm
        prev_pos_R = angle_R_arm
        if len(velo_list) > 6 :
            out = sum(velo_list)/len(velo_list)
            out_R = sum(velo_list2)/len(velo_list2)
            velo_list = []
            velo_list2 = []
        return out, out_R, prev_pos, prev_pos_R, prev_st, velo_list, velo_list2
        
def handle_mouse_event(event, x, y, flags, param):
    global buttons_clicked

    if event == cv2.EVENT_LBUTTONDOWN:
        # Check if the click occurred within any of the button regions
        for button in buttons:
            button_x, button_y, button_width, button_height, button_text = button
            if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
                # print(f"Button '{button_text}' clicked!")
                buttons_clicked.add(button_text)

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle

def accuracy(L_shoulder, R_shoulder, angle_L_body, angle_R_body):
    right = round(L_shoulder[0],2)*100
    left = round(R_shoulder[0],2)*100
    angle_L = round(angle_L_body,2)
    angle_R = round(angle_R_body,2)
    compare_mean = abs((left - right) / 2)
    if abs(compare_mean) > 1.5 or angle_L > 20.0 or angle_R > 20.0:
        score_accuracy = 80
    if abs(compare_mean) > 3.0 or angle_L > 25.0 or angle_R > 25.0:
        score_accuracy = 60
    if abs(compare_mean) > 4.0 or angle_L > 27.0 or angle_R > 27.0:
        score_accuracy = 40
    if abs(compare_mean) > 5.0 or angle_L > 30.0 or angle_R > 30.0:
        score_accuracy = 0
    if abs(compare_mean) < 1.5 and angle_L < 20.0 and angle_R > 20.0:
        score_accuracy = 100
    # print(score_accuracy)
    return score_accuracy
  
def disp(result_image, ex_name, L_counter, R_counter, er_1, er_2, er_3, start_time, Percent, time_L, time_R,prev, cnt, last_time, img, color_velo, x_position, y_position, sp):

    current_time = time.time()
    if (current_time - last_time) >= 2 :
        # print(current_time - last_time)
        print(time_R)
        if (time_L < 0.18 and time_L != 0) or (time_R < 0.18 and time_R != 0):
            sp = "Too Fast"
            last_time = time.time() 
        elif time_L > 0.4 or time_R > 0.4:
            sp = "Too Slow"
            last_time = time.time() 
        else :
            sp = ""
    top_left_x = 0  # Change as needed
    top_left_y = 900  # Change as needed
    bottom_right_x = 75  # Change as needed
    bottom_right_y = 1110  # Change as needed

    # Define the color (BGR format) and thickness
    rectangle_color = (0, 0, 0)  
    error = (68,49,190) 
    ER = 0.9    
 
    overlay = result_image.copy()

    cv2.rectangle(overlay, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), rectangle_color, 100)
    if er_1 != "":
        cv2.rectangle(overlay, (30, 480), (390, 530),error, 50)
    if er_2 != "":    
        cv2.rectangle(overlay, (30, 590), (410, 640),error, 50)
    elif sp != "" and er_1 == "" and er_2 == "":
        cv2.rectangle(overlay, (30, 370), (390, 420),error, 50)
    
    if er_3 != "":
        cv2.rectangle(overlay, (30, 700), (410, 750),error, 50)
   
    cv2.addWeighted(overlay, ER, result_image, 1 - ER, 0, result_image)
    cv2.rectangle(result_image, (0, 1476), (1080, 1920), (45,45,45), 100)
    cv2.circle(result_image,(420,1480),30,(255,255,255),3)
    cv2.rectangle(result_image, (100, 1635), (900, 1635), (161,247,242), 70)
    cv2.rectangle(result_image, (100, 1635), (900, 1635), (45,45,45), 60)
    cv2.rectangle(result_image, (100, 1730), (900, 1730), (161,247,242), 70)
    cv2.rectangle(result_image, (460, 125), (620, 160), (0,0,0), 100)
    
    # draw_half_circle_no_round(result_image,100,(330,80),60,color_velo,(97,49,6))
    # draw_half_circle_no_round(result_image,Percent,(115,80),60,(159,162,53),(82,25,7))
     
    # height, width, channels = img.shape
    # roi = result_image[y_position:y_position+height, x_position:x_position+width]
    # for c in range(0, 3):
    #     roi[:, :, c] = roi[:, :, c] * (1 - img[:, :, 3] / 255.0) + img[:, :, c] * (img[:, :, 3] / 255.0)
    
    # for button in buttons:
    #     button_x, button_y, button_width, button_height, _ = button
    #     cv2.rectangle(result_image, (button_x, button_y), (button_x + button_width, button_y + button_height), (149, 131, 8), -1)
    # if buttons_clicked:
    #     # print(buttons_clicked)
    #     if buttons_clicked == {'Button 1'}:
    #         L_counter = 0
    #         R_counter = 0
    #     # if buttons_clicked == {'Button 2'}:
    #     #     R_counter = 0
    #     buttons_clicked.clear()
        
    # pil_img = Image.fromarray(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
    # draw = ImageDraw.Draw(pil_img)
    # draw.text((478, 30), "Time", font=font, fill=(255, 255, 255))
    # draw.text((700, 130), "Set", font=font3, fill=(255, 255, 255))
    # draw.text((800, 130), "L Rep", font=font3, fill=(255, 255, 255))
    # draw.text((930, 130), "R Rep", font=font3, fill=(255, 255, 255))
    # draw.text((280, 130), "Speed", font=font3, fill=(255, 255, 255))
    # draw.text((50, 130), "Accuracy", font=font3, fill=(255, 255, 255))

    # draw.text((710, 35), "1", font=font2, fill=(255, 255, 255))
    # draw.text((820, 35), str(L_counter), font=font2, fill=(255, 255, 255))
    # draw.text((950, 35), str(R_counter), font=font2, fill=(255, 255, 255))
    # draw.text((87, 60), str(Percent), font=font3, fill=(255, 255, 255))
    # draw.text((600, 1500), str(ex_name), font=font2, fill=(255, 255, 255))
    # draw.text((80, 1640), str(time_L), font=font2, fill=(255, 255, 255))
    # draw.text((80, 1720), str(time_R), font=font2, fill=(255, 255, 255))
    # draw.text((80, 1800), er_3, font=font2, fill=(255, 255, 255))

    # draw.text((994, 223), "i", font=font, fill=(255, 255, 255),align='center')
    pil_img = Image.fromarray(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    draw.text((478, 80), "Time", font=font, fill=(255, 255, 255))
    draw.text((25, 900), "Set", font=font3, fill=(255, 255, 255))
    draw.text((20, 1000), "L Rep", font=font3, fill=(255, 255, 255))
    draw.text((20, 1100), "R Rep", font=font3, fill=(255, 255, 255))
    # # draw.text((280, 130), "Speed", font=font3, fill=(255, 255, 255))
    # # draw.text((50, 130), "Accuracy", font=font3, fill=(255, 255, 255))
    if sp != "" and er_1 == "" and er_2 == "":
        draw.text((20, 370), sp, font=font4, fill=(255, 255, 255))

    draw.text((40, 850), "1", font=font, fill=(255, 255, 255))
    draw.text((40, 950), str(L_counter), font=font, fill=(255, 255, 255))
    draw.text((40, 1050),str(R_counter), font=font, fill=(255, 255, 255))
    # draw.text((95, 60),  str(Percent), font=font, fill=(255, 255, 255))
    draw.text((64, 1450), str(ex_name), font=font, fill=(255, 255, 255))
    draw.text((20, 480), er_1, font=font4, fill=(255, 255, 255))
    draw.text((20, 590), er_2, font=font4, fill=(255, 255, 255))
    draw.text((20, 700), er_3, font=font4, fill=(255, 255, 255))
    draw.text((415, 1450), "i", font=font, fill=(255, 255, 255),align='center')
    draw.text((415, 1605), "PAUSE", font=font, fill=(255, 255, 255))
    draw.text((415, 1700), "FINISH", font=font, fill=(45, 45, 45))
    time_str = update_timer(result_image,start_time)        
    draw.text((438, 130), time_str, font=font2, fill=(255, 255, 255))
    result_image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    time_str = update_timer(result_image,start_time)        
    # draw.text((438, 80), time_str, font=font2, fill=(255, 255, 255))
    # result_image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    return result_image, L_counter, R_counter, prev, cnt, last_time,img, color_velo, x_position, y_position, sp

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

def calibrate(landmarks, time_ref) :
    nose = [landmarks[mp_lm.NOSE.value].x,landmarks[mp_lm.NOSE.value].y]
    current_time = time.time()
    if (current_time - time_ref) >= 0.5 :
        if nose[0] > 0.75 :
            cali_1 = "Go back"
        elif nose[0] < 0.7 :
            cali_1 = "Go forward"
        else :
            cali_1 = "Ok isus"
        if nose[1] > 0.45 and nose[1] < 0.55 :
            cali_2 = "KO"
        elif nose[1] < 0.45 :
            cali_2 = "Slide Left"
        else :
            cali_2 = "Slide Right"
        time_ref = time.time()
    return time_ref, cali_1, cali_2
    
    
    
def dumbbell_curl(image, stage, R_stage, counter, R_counter,landmarks,time_temp, time_temp_R):
    time_out, time_out_R = 0,0
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
    acc = (accuracy(L_shoulder, R_shoulder, angle_L_body, angle_R_body))
    if abs(dif_shoulder) < 2:
        e3 = ""
        
    elif dif_shoulder > 0 :
        e3 = "Please stand straight"
        cv2.line(image,tuple(np.multiply(L_shoulder, [1024, 768]).astype(int)),
                 tuple(np.multiply(R_shoulder, [1024, 768]).astype(int)),(0,155,255),10)
        # cv2.circle()
    else :
        cv2.line(image,tuple(np.multiply(L_shoulder, [1024, 768]).astype(int)),
                 tuple(np.multiply(R_shoulder, [1024, 768]).astype(int)),(0,155,255),10)
        e3 = "! Please stand straight"
        
        
    if angle_L_body > 30:
        e1 = "! Close your Left Arm"
        cv2.circle(image,tuple(np.multiply(L_shoulder, [1024, 768]).astype(int)),8,(0,0,255),15)
    else :
        e1 = ""        
        
    if angle_R_body > 30:
        e2 = "! Close your Right Arm"
        cv2.circle(image,tuple(np.multiply(R_shoulder, [1024, 768]).astype(int)),8,(0,0,255),15)
    else :
        e2 = ""
        
    if angle_L_arm > 165:
        stage = "down"
        time_temp = time.time()
        # print(time_temp,end='\r')
    elif angle_L_arm < 30 and stage =='down':
        stage="up"
        time_out = time.time() - time_temp
        # print(time_out,end='\r')
        counter +=1
                
    if angle_R_arm > 165:
        R_stage = "R_down"
        time_temp_R = time.time()
    elif angle_R_arm < 30 and R_stage =='R_down':
        R_stage="R_up"
        time_out_R = time.time() - time_temp_R
        # print(time_out_R,end='\r')
        R_counter +=1
    return counter, R_counter, e1, e2, e3, stage, R_stage, ex, acc, time_temp, time_temp_R, time_out, time_out_R

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