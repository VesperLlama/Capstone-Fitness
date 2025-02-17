import cv2
import mediapipe as mp
import numpy as np
import math
import base64
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


def calculate_angle(img, p1, p2, p3, lmList):
    # Get the landmarks
    x1, y1 = lmList[p1][1:]
    x2, y2 = lmList[p2][1:]
    x3, y3 = lmList[p3][1:]

    # Calculate the Angle
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360

    # Draw the lines and circles
    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
    cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
    cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
    cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
    cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
    cv2.putText(
        img,
        str(int(angle)),
        (x2 - 50, y2 + 50),
        cv2.FONT_HERSHEY_PLAIN,
        2,
        (0, 0, 255),
        2,
    )
    return angle

start_time = time.time()
# Curl counter variables
counter = 0
count = 0
dir = 0
stage = None


# Setup Mediapipe instance
def process_frame(contents):
    global count, dir, pose

    # with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    # ret, frame = cap.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Recolor image to RGB
    img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
    results = pose.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    elapsed_time = time.time() - start_time
    timer_text = f"Time: {int(elapsed_time)} sec"

    if results.pose_landmarks:
        lmList = []
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])

        if len(lmList) != 0:
            # Calculate angle
            angle = calculate_angle(img, 11, 13, 15, lmList)
            angle_shoulder = calculate_angle(img, 13, 11, 23, lmList)

            per = np.interp(angle, (210, 310), (0, 100))
            bar = np.interp(angle, (220, 310), (h * 0.9, h * 0.1))

            # Check for dumbbell curls
            color = (255, 0, 255)
            if angle_shoulder>=0 and angle_shoulder<=20:
                if per == 100:
                    color = (0, 255, 0)
                    if dir == 0:
                        count += 0.5
                        dir = 1
                if per == 0:
                    color = (0, 255, 0)
                    if dir == 1:
                        count += 0.5
                        dir = 0

            # Draw the bar
            bar_x_start = int(w * 0.9)
            bar_x_end = int(w * 0.95)
            cv2.rectangle(
                img, (bar_x_start, int(h * 0.1)), (bar_x_end, int(bar)), color, 3
            )
            cv2.rectangle(
                img,
                (bar_x_start, int(bar)),
                (bar_x_end, int(h * 0.9)),
                color,
                cv2.FILLED,
            )
            cv2.putText(img, f'{int(per)}%', (int(w * 0.88), int(h * 0.05)), cv2.FONT_HERSHEY_SIMPLEX, 
                            0.8, color, 2, cv2.LINE_AA)
            
            # Draw the background rectangle dynamically
            count_text = str(int(count))
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 3
            thickness = 5

            # Calculate text size
            text_size = cv2.getTextSize(count_text, font, font_scale, thickness)[0]

            # Define box padding
            padding_x, padding_y = 20, 20  # Adjust as needed
            box_x, box_y = 30, 600  # Top-left position of the box
            box_width = text_size[0] + 2 * padding_x
            box_height = text_size[1] + 2 * padding_y

            # Draw the background rectangle
            cv2.rectangle(img, (box_x, box_y), (box_x + box_width, box_y + box_height), (0, 0, 0), cv2.FILLED)

            # Calculate text position (centered inside the box)
            text_x = box_x + padding_x
            text_y = box_y + text_size[1] + padding_y

            # Draw the count text
            cv2.putText(img, count_text, (text_x, text_y), font, font_scale, (0, 255, 0), thickness)


            # Calculate text size
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 2
            text_size = cv2.getTextSize(timer_text, font, font_scale, thickness)[0]
            
            # Define box padding
            padding = 10
            x, y = 30, 40  # Top-left corner
            box_width = text_size[0] + 2 * padding
            box_height = text_size[1] + 2 * padding

            # Draw the background rectangle
            cv2.rectangle(img, (x, y - text_size[1] - padding), (x + box_width, y + padding), (0, 0, 0), -1)

            # Draw the text
            cv2.putText(img, timer_text, (x + padding, y), font, font_scale, (0, 255, 0), thickness, cv2.LINE_AA)

    # Convert back to BGR for displaying in OpenCV
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    end_time = time.time()
    total_time = end_time - start_time

    _, buffer = cv2.imencode(".jpg", img)
    img_str = base64.b64encode(buffer).decode("utf-8")
    return img_str, count
