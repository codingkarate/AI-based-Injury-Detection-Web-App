import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils


def extract_keypoints(image_path):
    """
    Takes an image path, runs MediaPipe Pose,
    and returns list of keypoints (landmarks).
    """
    image = cv2.imread(image_path)
    if image is None:
        return {"error": "Image not found"}

    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process with MediaPipe
    results = pose.process(image_rgb)

    if not results.pose_landmarks:
        return {"error": "No person detected"}

    # Extract (x, y, z, visibility) for each landmark
    landmarks = [
        {
            "id": idx,
            "x": lm.x,
            "y": lm.y,
            "z": lm.z,
            "visibility": lm.visibility
        }
        for idx, lm in enumerate(results.pose_landmarks.landmark)
    ]

    return {"landmarks": landmarks}
