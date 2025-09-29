import cv2
import mediapipe as mp
import math
import random

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = [a.x, a.y]
    b = [b.x, b.y]
    c = [c.x, c.y]

    radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
    angle = abs(radians*180.0/math.pi)
    if angle > 180:
        angle = 360 - angle
    return angle

# Dummy risk detection
def detect_injury_risk(landmarks):
    try:
        left_elbow_angle = calculate_angle(
            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        )

        # Simple rule: if elbow angle is too small or too large, risk increases
        if left_elbow_angle < 40 or left_elbow_angle > 160:
            risk = random.randint(60, 90)  # high risk
            fault = "Improper elbow angle"
        else:
            risk = random.randint(10, 30)  # low risk
            fault = "Good posture"

        return {"risk_percent": risk, "fault": fault}

    except Exception as e:
        return {"risk_percent": 0, "fault": "No posture detected"}

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Run dummy risk detection
        output = detect_injury_risk(results.pose_landmarks.landmark)
        print(output)  # Print to terminal

    cv2.imshow('Pose Detection + Dummy Risk', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
