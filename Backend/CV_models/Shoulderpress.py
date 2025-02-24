import cv2
import mediapipe as mp
import numpy as np
import math
import base64


def calculate_angle(img, p1, p2, p3, lmList):
    x1, y1 = lmList[p1][1:]
    x2, y2 = lmList[p2][1:]
    x3, y3 = lmList[p3][1:]

    angle = math.degrees(
        abs(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    )
    if angle > 180:
        angle = 360 - angle

    # Draw landmarks & lines
    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
    cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
    for point in [p1, p2, p3]:
        cx, cy = lmList[point][1:]
        cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 15, (0, 0, 255), 2)

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


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


def process_frame(contents):
    global pose
    count = 0
    dir = 0
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(frame)
    # frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    height, width, _ = frame.shape

    if results.pose_landmarks:
        lmList = [
            [id, int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])]
            for id, lm in enumerate(results.pose_landmarks.landmark)
        ]
        if len(lmList) != 0:
            angle_right = calculate_angle(frame, 12, 14, 16, lmList)
            angle_left = calculate_angle(frame, 11, 13, 15, lmList)
            shldr_angle_left = calculate_angle(frame, 13, 11, 23, lmList)
            shldr_angle_right = calculate_angle(frame, 14, 12, 24, lmList)

            per_left = np.interp(angle_right, (70, 125), (100, 0))
            bar_left = np.interp(angle_right, (75, 125), (100, height * 0.9))
            per_right = np.interp(angle_left, (70, 125), (100, 0))
            bar_right = np.interp(angle_left, (75, 125), (100, height * 0.9))

            color_right, color_left = (255, 0, 255), (255, 0, 255)
            if (shldr_angle_left >= 85 and shldr_angle_left <= 170) and (
                shldr_angle_right >= 85 and shldr_angle_right <= 170
            ):
                if per_right == 100 and per_left == 100:
                    color_right = color_left = (0, 255, 0)
                    if dir == 0:
                        count = 0.5
                        dir = 1
                if per_right == 0 and per_left == 0:
                    color_right = color_left = (0, 255, 0)
                    if dir == 1:
                        count = 0.5
                        dir = 0

            x_right = int(width * 0.90)
            x_right_end = int(width * 0.94)

            x_left = int(width * 0.04)
            x_left_end = int(width * 0.08)

            y_top = int(height * 0.14)
            y_bottom = int(height * 0.95)

            # Right Bar
            cv2.rectangle(
                frame, (x_right, y_top), (x_right_end, y_bottom), color_right, 3
            )
            cv2.rectangle(
                frame,
                (x_right, int(bar_right)),
                (x_right_end, y_bottom),
                color_right,
                cv2.FILLED,
            )
            cv2.putText(
                frame,
                f"{int(per_right)}%",
                (x_right - 15, y_top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color_right,
                2,
                cv2.LINE_AA,
            )

            # Left Bar
            cv2.rectangle(frame, (x_left, y_top), (x_left_end, y_bottom), color_left, 3)
            cv2.rectangle(
                frame,
                (x_left, int(bar_left)),
                (x_left_end, y_bottom),
                color_left,
                cv2.FILLED,
            )
            cv2.putText(
                frame,
                f"{int(per_left)}%",
                (x_left - 5, y_top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color_left,
                2,
                cv2.LINE_AA,
            )

            # Enhanced Timer Box
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 2
            padding_x, padding_y = 10, 10

            # Enhanced Curl Count Box
            count_text = str(int(count))
            font_scale = 3
            thickness = 5
            text_size = cv2.getTextSize(count_text, font, font_scale, thickness)[0]
            box_x, box_y = 30, 600
            box_width = text_size[0] + 2 * padding_x
            box_height = text_size[1] + 2 * padding_y

            cv2.rectangle(
                frame,
                (box_x, box_y),
                (box_x + box_width, box_y + box_height),
                (0, 0, 0),
                cv2.FILLED,
            )
            text_x = box_x + padding_x
            text_y = box_y + text_size[1] + padding_y
            cv2.putText(
                frame,
                count_text,
                (text_x, text_y),
                font,
                font_scale,
                (0, 255, 0),
                thickness,
            )

    _, buffer = cv2.imencode(".jpg", frame)
    img_str = base64.b64encode(buffer).decode("utf-8")
    return img_str, count
