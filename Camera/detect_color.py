import cv2
import numpy as np

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

class ColorDetector:
    def __init__(self, lower_color_range, upper_color_range):
        """
        Initialise le détecteur de couleur avec les plages HSV pour la couleur à détecter.
        :param lower_color_range: Limite inférieure de la plage de couleurs (en HSV).
        :param upper_color_range: Limite supérieure de la plage de couleurs (en HSV).
        """
        self.lower_color_range = lower_color_range
        self.upper_color_range = upper_color_range

    def detect_color(self, frame):
        """Applique la détection de couleur sur une image (frame) et renvoie le résultat."""
        # Convertit l'image de BGR à HSV (teinte, saturation, valeur)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Créer un masque pour les pixels correspondant à la plage de couleurs définie
        mask = cv2.inRange(hsv, self.lower_color_range, self.upper_color_range)

        # Appliquer le masque sur l'image d'origine
        result = cv2.bitwise_and(frame, frame, mask=mask)
        
        return result