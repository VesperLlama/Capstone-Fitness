import cv2
import mediapipe as mp
import numpy as np
import base64
import time

# Initialize Mediapipe pose model
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Squat tracking variables
squat_progress = 0
squat_down = False
squat_up = False

# Start workout timer
start_time = time.time()
rep_start_time = None  # Timer for lowest squat position
rep_duration = 0
switch_percentage = False

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    
    return angle

def process_frame(contents):
    global pose, squat_progress, squat_down, squat_up, switch_percentage, start_time
    rep_count = 0

    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    height, width, _ = image.shape  # Get frame dimensions

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        landmarks = results.pose_landmarks.landmark
        
        # Get key points
        lhip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        lknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        lankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        # Calculate knee angle
        knee_angle = calculate_angle(lhip, lknee, lankle)
        
        # Define progress based on squat depth
        min_angle, max_angle = 64, 170
        if switch_percentage:
            squat_progress = int(np.interp(knee_angle, [min_angle, max_angle], [50, 100]))
        else:
            squat_progress = int(np.interp(knee_angle, [min_angle, max_angle], [50, 0]))
        
        if squat_progress == 50:
            switch_percentage = True
        elif squat_progress == 100 and knee_angle > 178:
            switch_percentage = False
        
        # Detect full squat repetition
        if squat_progress == 50:
            squat_down = True
        if squat_down and squat_progress == 0:
            squat_up = True
        if squat_down and squat_up:
            rep_count = 1
            squat_down = False
            squat_up = False

        # Define positions for text alignment
        text_x, text_y = int(0.05 * width), 30
        line_spacing = 30  # Space between lines
        
        # Display information in top-left corner
        cv2.putText(image, f'Knee Angle: {int(knee_angle)}', (text_x, text_y + line_spacing), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Draw progress bar on RHS
        bar_x1, bar_y1 = int(0.9 * width), int(0.8 * height)
        bar_x2, bar_y2 = bar_x1 + 50, bar_y1 - int(squat_progress * 3)
        cv2.rectangle(image, (bar_x1, bar_y1), (bar_x2, bar_y2), (0, 255, 0), -1)
        cv2.rectangle(image, (bar_x1, bar_y1 - 300), (bar_x2, bar_y1), (255, 255, 255), 3)
        cv2.putText(image, f'{squat_progress}%', (bar_x1 + 5, bar_y1 - 320), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    _, buffer = cv2.imencode(".jpg", image)
    img_str = base64.b64encode(buffer).decode("utf-8")
    
    return img_str, rep_count
