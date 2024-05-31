import cv2
import mediapipe as mp
import streamlit as st
import numpy as np

def anonymize_face(frame, face_rect):
    x, y, w, h = face_rect

    # Ensure face_roi is within frame boundaries
    if x >= 0 and y >= 0 and x + w <= frame.shape[1] and y + h <= frame.shape[0]:
        face_roi = frame[y:y+h, x:x+w]
        if face_roi.size != 0:  # Check if face_roi is not empty
            blur_radius = min(w, h) // 8  # Dynamically calculate blur radius
            blur_radius = max(blur_radius, 1)  # Ensure minimum blur radius
            blurred_face = cv2.GaussianBlur(face_roi, (blur_radius * 2 + 1, blur_radius * 2 + 1), 0)
            frame[y:y+h, x:x+w] = blurred_face

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

st.title("Face Anonymization")

cap = cv2.VideoCapture(0)

exit_button_clicked = False

with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while not exit_button_clicked:
        ret, frame = cap.read()
        if not ret:
            st.error("Unable to capture frame.")
            break

        # Convert the image to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image with MediaPipe
        results = face_detection.process(frame_rgb)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                             int(bboxC.width * iw), int(bboxC.height * ih)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face_rect = (x, y, w, h)
                anonymize_face(frame, face_rect)

        # Display the frame with the anonymized faces
        st.image(frame, channels="BGR")

        # Create a unique key for the exit button
        exit_button_key = "exit_button_" + str(hash(frame.tostring()))

        # Add an exit button with a unique key
        if st.button("Exit", key=exit_button_key):
            exit_button_clicked = True

        # Break out of the loop after processing one frame
        break

if not cap.isOpened():
    cap.release()
    cv2.destroyAllWindows()
