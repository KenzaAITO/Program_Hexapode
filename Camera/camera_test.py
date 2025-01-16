import cv2
import numpy as np
import time

 
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
