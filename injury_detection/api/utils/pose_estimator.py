import cv2
import mediapipe as mp
import numpy as np
import tempfile
import math
import os

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    """Calculate the angle between three points"""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle


def analyze_video(video_file):
    """
    Analyze an uploaded video and return injury-risk result.
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            for chunk in video_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        cap = cv2.VideoCapture(tmp_path)
        pose = mp_pose.Pose()

        total_frames = 0
        improper_frames = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            total_frames += 1

            # Convert the frame to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark

                # Landmarks for left elbow
                shoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                         lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                         lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                angle = calculate_angle(shoulder, elbow, wrist)

                # If elbow angle outside normal range, mark as improper
                if angle < 40 or angle > 170:
                    improper_frames += 1

        cap.release()
        pose.close()
        os.remove(tmp_path)

        # Compute risk percentage
        if total_frames == 0:
            return {"risk_percent": 0, "fault": "No frames detected"}

        risk_percent = int((improper_frames / total_frames) * 100)

        if risk_percent > 60:
            fault = "Improper elbow angle"
        else:
            fault = "Good posture"

        return {"risk_percent": risk_percent, "fault": fault}

    except Exception as e:
        return {"error": str(e)}
