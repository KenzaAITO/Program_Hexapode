import cv2
import time
from datetime import datetime

# Initialize variables
first_frame = None
status_list = [None, None]
times = []

# Set video source
video = cv2.VideoCapture(0)  # Use 0 for the default webcam or replace with RTSP link

while True:
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Set the initial frame for reference
    if first_frame is None:
        first_frame = gray
        continue

    # Calculate the difference between the current frame and the first frame
    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Find contours of the m
