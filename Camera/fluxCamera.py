import cv2
import numpy as np

class Camera:
    def __init__(self):
        # Initialiser la capture vidéo depuis la caméra
        self.cap = cv2.VideoCapture(0)  # 0 correspond à la première caméra disponible

    def start_stream(self, detector):
        """Démarre le flux vidéo et transmet chaque frame au détecteur de couleur."""
        if not self.cap.isOpened():
            print("Impossible d'ouvrir la caméra")
            return

        print("Démarrage du flux vidéo...")

        while True:
            # Capture une frame de la caméra
            ret, frame = self.cap.read()
            if not ret:
                print("Erreur lors de la capture vidéo")
                break

            # Appliquer la détection de couleur sur la frame sans masquer les autres couleurs
            color_frame = detector.detect_colors(frame)

            # Afficher le flux original avec la détection de couleurs (rouge et vert accentués)
            cv2.imshow('Détection Rouge et Vert', color_frame)

            # Appuyer sur 'q' pour quitter
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Libérer la caméra et fermer les fenêtres
        self.cap.release()
        cv2.destroyAllWindows()
        print("Flux vidéo terminé.")


class ColorDetector:
    def __init__(self, lower_red1, upper_red1, lower_red2, upper_red2, lower_green, upper_green):
        """
        Initialise le détecteur de couleurs pour le rouge et le vert.
        :param lower_red1, upper_red1: Limites inférieures et supérieures pour une nuance de rouge (en HSV).
        :param lower_red2, upper_red2: Limites pour une autre nuance de rouge (en HSV).
        :param lower_green, upper_green: Limites pour le vert (en HSV).
        """
        self.lower_red1 = lower_red1
        self.upper_red1 = upper_red1
        self.lower_red2 = lower_red2
        self.upper_red2 = upper_red2
        self.lower_green = lower_green
        self.upper_green = upper_green

    def detect_colors(self, frame):
        """Accentue les couleurs rouges et vertes dans l'image tout en laissant les autres inchangées."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Masques pour les différentes nuances de rouge
        mask_red1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        mask_red2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)

        # Masque pour le vert
        mask_green = cv2.inRange(hsv, self.lower_green, self.upper_green)

        # Combine les deux masques rouges
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)

        # Trouver les pixels correspondant aux couleurs rouge et vert
        mask_combined = cv2.bitwise_or(mask_red, mask_green)

        # Créer une image où seules les zones rouges et vertes sont accentuées
        highlighted = frame.copy()
        highlighted[mask_combined > 0] = [0, 255, 0]  # Tu peux ajuster l'intensité ou les couleurs ici

        # Superpose les parties accentuées avec l'image d'origine
        result = cv2.addWeighted(frame, 0.7, highlighted, 0.3, 0)

        return result


# Exemple d'utilisation
if __name__ == "__main__":
    # Plages de couleurs pour le rouge en HSV (deux nuances de rouge)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Plages de couleurs pour le vert en HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    # Créer l'instance du détecteur de couleur pour le rouge et le vert
    color_detector = ColorDetector(lower_red1, upper_red1, lower_red2, upper_red2, lower_green, upper_green)

    # Créer une instance de la caméra et démarrer le flux vidéo avec détection de couleur
    camera = Camera()
    camera.start_stream(color_detector)
