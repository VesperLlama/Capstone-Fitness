import cv2
import mediapipe as mp
import numpy as np
import math
import base64

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
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img)

    if results.pose_landmarks:
        lmList = []
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])

        if len(lmList) != 0:
            # Calculate angle
            angle = calculate_angle(img, 12, 14, 16, lmList)

            per = np.interp(angle, (210, 310), (0, 100))
            bar = np.interp(angle, (220, 310), (h * 0.9, h * 0.1))

            # Check for dumbbell curls
            color = (255, 0, 255)
            if per == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count = 0.5
                    dir = 1
                else:
                    count = 0
            if per == 0:
                color = (0, 255, 0)
                if dir == 1:
                    count = 0.5
                    dir = 0
                else:
                    count = 0

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
            cv2.putText(
                img,
                f"{int(per)} %",
                (int(w * 0.88), int(h * 0.05)),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                color,
                2,
            )

    # Convert back to BGR for displaying in OpenCV
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    _, buffer = cv2.imencode(".jpg", img)
    img_str = base64.b64encode(buffer).decode("utf-8")
    return img_str, count
