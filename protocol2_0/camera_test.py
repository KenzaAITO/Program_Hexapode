import cv2
import numpy as np
import time


def detect_color(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
 
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])
 
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
 
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
    red_detected = any(cv2.contourArea(contour) > 1000 for contour in contours_red)
    green_detected = any(cv2.contourArea(contour) > 1000 for contour in contours_green)
 
    return red_detected, green_detected
 
def check_camera():
    cap = cv2.VideoCapture(0)  # Utiliser l'index approprié pour votre caméra
 
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la caméra.")
        return False, False
 
    ret, frame = cap.read()
    cap.release()
 
    if not ret:
        print("Erreur: Impossible de capturer l'image.")
        return False, False
 
    return detect_color(frame)
 
# Initialiser les flags de contrôle du robot
red_detected_flag = False
green_detected_flag = False
 


if __name__ == "__main__":

    while True:
        red_detected_flag, green_detected_flag = check_camera()
 
        if red_detected_flag:
            print(f"redddd")

        if green_detected_flag:
            print(f"greeennnn")
               
        if not red_detected_flag and not green_detected_flag:
            print(f" no color ")
 
        time.sleep(1)  # Pause de 1 seconde entre chaque cycle
