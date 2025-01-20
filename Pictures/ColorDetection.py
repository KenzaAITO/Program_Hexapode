import cv2
import numpy as np

class ColorDetection:
    @staticmethod
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

    @staticmethod
    def analyze_photos(photo_path):
        #print(f"[INFO] Analyse de la photo : {photo_path}")
        image = cv2.imread(photo_path)

        if image is None:
            #print(f"[ERREUR] Impossible de lire la photo : {photo_path}")
            return

        red_detected, green_detected = ColorDetection.detect_color(image)

        if red_detected:
            print("[INFO] Rouge detecte!")
            return red_detected
        if green_detected:
            print("[INFO] Vert detecte!")
            return green_detected
        if not red_detected and not green_detected:
            print("[INFO] Aucune couleur detectee.")
