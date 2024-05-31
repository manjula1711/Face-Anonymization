# Face-Anonymization


Libraries: Uses OpenCV, MediaPipe, Streamlit, and NumPy.
Function: anonymize_face to blur detected faces.
Face Detection: Initialized with MediaPipe.
Streamlit UI: Sets up a title and an exit button.
Webcam Capture: Starts capturing video from the webcam.
Processing Loop:
Reads a frame.
Converts to RGB.
Detects faces.
Draws rectangles and blurs faces.
Displays the frame.
Checks for exit button click.
Resource Management: Releases webcam and closes windows when done.
