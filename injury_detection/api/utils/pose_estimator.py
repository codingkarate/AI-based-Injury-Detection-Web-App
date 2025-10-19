import cv2
import mediapipe as mp
import numpy as np
from collections import Counter
import tkinter as tk
from tkinter import messagebox

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-8)
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return angle

# Dummy risk detection logic
def analyze_pose(landmarks):
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

    angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    if angle < 160:  # example threshold
        return 75, "Improper elbow angle"
    else:
        return 20, "Good form"

# Popup window using Tkinter
def show_popup(average_risk, common_fault):
    root = tk.Tk()
    root.withdraw()  # hide main window
    messagebox.showinfo("Risk Analysis Result",
                        f"✅ Pose Analysis Complete\n\n"
                        f"📊 Average Risk: {average_risk:.2f}%\n"
                        f"⚠️ Most Common Fault: {common_fault}")
    root.destroy()

# Main camera loop
def run_pose_estimation():
    cap = cv2.VideoCapture(0)
    risk_values = []
    fault_messages = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
                )
                risk, fault = analyze_pose(results.pose_landmarks.landmark)
                risk_values.append(risk)
                fault_messages.append(fault)

            cv2.putText(image, "Press 'q' to STOP", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Pose Estimation', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

    if risk_values:
        average_risk = sum(risk_values) / len(risk_values)
        common_fault = Counter(fault_messages).most_common(1)[0][0]
        show_popup(average_risk, common_fault)
    else:
        show_popup(0, "No pose detected")

if __name__ == "__main__":
    run_pose_estimation()
