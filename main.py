from Deplacement import HexapodMovement
from Pictures.take_pictures import ColorDetection, CameraManager
import time

def main():

    PHOTO_DIR = "./photos"
    BUFFER_SIZE = 10
    
    camera_manager = CameraManager(PHOTO_DIR, BUFFER_SIZE)
    camera_manager.run(interval=1)

    while True:
        red_detected_flag, green_detected_flag = check_camera()
 
        if red_detected_flag:
            print(f"redddd")

        if green_detected_flag:
            print(f"greeennnn")
               
        if not red_detected_flag and not green_detected_flag:
            print(f" no color ")
 
        time.sleep(1)  # Pause de 1 seconde entre chaque cycle


if __name__ == "__main__":
    main()
