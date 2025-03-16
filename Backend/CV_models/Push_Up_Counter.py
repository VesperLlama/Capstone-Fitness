import cv2
import mediapipe as mp
import numpy as np
import base64
import time

# Initialize Mediapipe and pose estimation model
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Global variables for push-up tracking
progress = 0
going_down = False
going_up = False
rep_count = 0
start_time = time.time()
rep_start_time = None
rep_duration = 0
switch_percentage = False

def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def process_frame(contents):
    global rep_count, progress, going_down, going_up, rep_start_time, rep_duration, switch_percentage, start_time

    # Decode image from input bytes
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        landmarks = results.pose_landmarks.landmark

        # Optionally hide unwanted landmarks for clarity
        lndmrk_hide = [1,2,3,4,5,6,7,8,9,10,17,18,19,20,21,22,29,30,31,32]
        for id, lndmrk in enumerate(landmarks):
            if id in lndmrk_hide:
                lndmrk.visibility = 0

        # Get coordinates for side view calculation
        nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y]
        lshldr = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        rshldr = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        offset_angle = calculate_angle(lshldr, nose, rshldr)
        cv2.putText(image, f'Side view: {int(round(offset_angle,2))}', (700, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Get coordinates of key joints
        lshldr_land = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        rshldr_land = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        lhip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        rhip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        lknee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        rknee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        lankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        rankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        lelbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        relbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        lwrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        rwrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

        # Determine which side to use for feedback and calculations
        if lshldr_land.visibility and lhip.visibility:
            shldr_coords = [lshldr_land.x, lshldr_land.y]
            elbow_coords = [lelbow.x, lelbow.y]
            wrist_coords = [lwrist.x, lwrist.y]
            shldr_vert_angle = calculate_angle([lhip.x, lhip.y], [lshldr_land.x, lshldr_land.y], [lshldr_land.x, 0])
            hip_angle = calculate_angle([lshldr_land.x, lshldr_land.y], [lhip.x, lhip.y], [lknee.x, lknee.y])
            knee_angle = calculate_angle([lhip.x, lhip.y], [lknee.x, lknee.y], [lankle.x, lankle.y])
        elif rshldr_land.visibility and rhip.visibility:
            shldr_coords = [rshldr_land.x, rshldr_land.y]
            elbow_coords = [relbow.x, relbow.y]
            wrist_coords = [rwrist.x, rwrist.y]
            shldr_vert_angle = calculate_angle([rhip.x, rhip.y], [rshldr_land.x, rshldr_land.y], [rshldr_land.x, 0])
            hip_angle = calculate_angle([rshldr_land.x, rshldr_land.y], [rhip.x, rhip.y], [rknee.x, rknee.y])
            knee_angle = calculate_angle([rhip.x, rhip.y], [rknee.x, rknee.y], [rankle.x, rankle.y])
        else:
            shldr_vert_angle = hip_angle = knee_angle = None

        # Provide visual feedback based on body alignment
        if hip_angle and hip_angle > 150:
            cv2.putText(image, 'Straight back', (700, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(image, 'Bend back', (700, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if knee_angle and knee_angle > 130:
            cv2.putText(image, 'Straight knee', (850, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(image, 'Bend knee', (850, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Calculate elbow angle for push-up detection
        elbow_angle = calculate_angle(shldr_coords, elbow_coords, wrist_coords)
        min_angle = 70   # Deep push-up
        max_angle = 175  # Plank position

        # Update progress (used for visualizing push-up depth)
        if progress == 40:
            switch_percentage = True
        elif progress == 100 and elbow_angle > 162:
            switch_percentage = False

        if switch_percentage:
            progress = int(np.interp(elbow_angle, [min_angle, max_angle], [50, 100]))
        else:
            progress = int(np.interp(elbow_angle, [min_angle, max_angle], [50, 0]))

        # Track time spent at the lowest push-up position
        if progress >= 100 and rep_start_time is None:
            rep_start_time = time.time()
        elif progress < 100 and rep_start_time is not None:
            rep_duration = time.time() - rep_start_time
            rep_start_time = None

        # Detect push-up repetition based on movement
        if progress >= 50:
            going_down = True
        if going_down and progress == 0:
            going_up = True
        if going_down and going_up:
            rep_count += 1
            going_down = False
            going_up = False

        # Draw a progress bar and overlay metrics on the image
        bar_height = int(progress * 3)
        cv2.rectangle(image, (50, 400), (100, 400 - bar_height), (0, 255, 0), -1)
        cv2.rectangle(image, (50, 100), (100, 400), (255, 255, 255), 3)
        cv2.putText(image, f'{progress}%', (55, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(image, f'Elbow Angle: {int(elbow_angle)}', (700, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(image, f'Hold Time: {rep_duration:.2f}s', (700, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Encode the processed image to JPEG and then convert to a base64 string
    _, buffer = cv2.imencode(".jpg", image)
    img_str = base64.b64encode(buffer).decode("utf-8")
    return img_str, rep_count
