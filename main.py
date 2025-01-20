from Deplacement import HexapodMovement
from Pictures.take_pictures import ColorDetection, CameraManager
import time

def main():

    PHOTO_DIR = "./photos"
    BUFFER_SIZE = 10
    
    camera_manager = CameraManager(PHOTO_DIR, BUFFER_SIZE)

    while True:
        print("[INFO] Capture et analyse des photos...")
        camera_manager.capture_photo()
        detected_color = camera_manager.process_photos()

        if detected_color == "red":
            print("[MAIN ACTION] Action pour la couleur rouge.")
        elif detected_color == "green":
            print("[MAIN ACTION] Action pour la couleur verte.")
        elif detected_color == "none":
            print("[MAIN ACTION] Aucune couleur détectée.")

        time.sleep(1)


if __name__ == "__main__":
    main()
