import os
import time
from collections import deque
from Pictures.ColorDetection import ColorDetection

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