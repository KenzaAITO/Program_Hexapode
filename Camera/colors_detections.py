import cv2
import numpy as np

class Vision:
    def __init__(self, camera_index=0):
        # Initialiser la caméra
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception("Could not open video device")

    def get_frame(self):
        # Lire une image de la caméra
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Could not read frame")
        return frame

    def release(self):
        # Libérer la caméra
        self.cap.release()
        cv2.destroyAllWindows()


class ColorDetection:
    def __init__(self, lower_color, upper_color):
        self.lower_color = np.array(lower_color)
        self.upper_color = np.array(upper_color)

    def detect(self, frame):
        # Convertir l'image en espace de couleur HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Créer un masque pour la détection de la couleur
        mask = cv2.inRange(hsv, self.lower_color, self.upper_color)

        # Appliquer le masque à l'image
        result = cv2.bitwise_and(frame, frame, mask=mask)

        return mask, result


if __name__ == "__main__":
    # Définir la plage de couleur à détecter (rouge dans cet exemple)
    lower_red = [0, 120, 70]
    upper_red = [10, 255, 255]

    # Créer des instances des classes
    vision = Vision()
    color_detection = ColorDetection(lower_red, upper_red)

    try:
        while True:
            # Obtenir une image de la caméra
            frame = vision.get_frame()

            # Détecter la couleur
            mask, result = color_detection.detect(frame)

            # Afficher les résultats
            cv2.imshow('Frame', frame)
            cv2.imshow('Mask', mask)
            cv2.imshow('Result', result)

            # Quitter avec la touche 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Libérer les ressources
        vision.release()