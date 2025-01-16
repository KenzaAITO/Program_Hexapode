import cv2
import numpy as np 

class Camera:
    def __init__(self):
        # Initialiser la capture vidéo depuis la caméra
        print("init")
        #self.cap = cv2.VideoCapture(0)  # 0 correspond à la première caméra disponible
        self.cap = cv2.VideoCapture(f'/dev/video0')


    def start_stream(self):
        """Démarre le flux vidéo et transmet chaque frame au détecteur de couleur."""
        if not self.cap.isOpened():
            print("Impossible d'ouvrir la caméra")
            return

        print("Démarrage du flux vidéo...")

        while True:

            print("while true")
            # Capture une frame de la caméra
            ret, frame = self.cap.read()
            if not ret:
                print("Erreur lors de la capture vidéo")
                break

            # Appliquer la détection de couleur sur la frame
            #color_frame = detector.detect_color(frame)

            # Afficher le flux original et le flux avec la couleur détectée
            cv2.imshow('Flux Video Original', frame)
            #cv2.imshow('Détection de Couleur', color_frame)

            # Appuyer sur 'q' pour quitter
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Libérer la caméra et fermer les fenêtres
        self.cap.release()
        cv2.destroyAllWindows()
        print("Flux vidéo terminé.")


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


# Exemple d'utilisation
if __name__ == "__main__":
    # Plages de couleurs pour le rouge en HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Créer deux masques pour couvrir les différentes nuances de rouge
    lower_color_range = np.array([0, 120, 70])
    upper_color_range = np.array([180, 255, 255])

    # Créer l'instance du détecteur de couleur pour le rouge
    #color_detector = ColorDetector(lower_color_range, upper_color_range)

    # Créer une instance de la caméra et démarrer le flux vidéo avec détection de couleur
    camera = Camera()
    camera.start_stream()
