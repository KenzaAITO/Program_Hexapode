import os
import time
import cv2
import numpy as np
from collections import deque

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

class CameraManager:
    def __init__(self, photo_dir, buffer_size=10):
        self.photo_dir = photo_dir
        self.photo_buffer = deque(maxlen=buffer_size)
        self.ensure_directory_exists()

    def ensure_directory_exists(self):
        if not os.path.exists(self.photo_dir):
            os.makedirs(self.photo_dir)

    def capture_photo(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        photo_path = os.path.join(self.photo_dir, f"photo_{timestamp}.jpg")
        print(f"[INFO] Capture de la photo : {photo_path}")

        os.system(f"libcamera-still -o {photo_path} -t 1 ")

        self.photo_buffer.append(photo_path)
        return photo_path

    def process_photos(self):
        #print("[INFO] Analyse des photos dans le buffer...")
        for photo in list(self.photo_buffer):
            ColorDetection.analyze_photos(photo)

    def run(self, interval=0.1):
        while True:
            photo_path = self.capture_photo()
            self.process_photos()
            #print("[INFO] Attente avant la prochaine capture...")
            time.sleep(interval)

if __name__ == "__main__":
    PHOTO_DIR = "./photos"
    BUFFER_SIZE = 10

    camera_manager = CameraManager(PHOTO_DIR, BUFFER_SIZE)
    camera_manager.run(interval=1)