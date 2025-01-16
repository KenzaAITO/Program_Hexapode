import subprocess
import time
import cv2
import numpy as np


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
        """
        Applique la détection de couleur sur une image (frame) et renvoie True si la couleur est détectée.
        :param frame: Image (BGR) sur laquelle appliquer la détection.
        :return: Booléen indiquant si la couleur est détectée.
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_color_range, self.upper_color_range)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return any(cv2.contourArea(contour) > 1000 for contour in contours)


class VisionHexapode:
    def __init__(self):
        """
        Initialise la caméra pour l'hexapode avec une vérification de l'état de la caméra.
        """
        print("Initialisation de la caméra.")
        self.process = None
        self.initialized = self.initialize_camera()
        if self.initialized:
            print("Caméra initialisée avec succès.")
        else:
            print("Erreur : Impossible d'initialiser la caméra.")

    def initialize_camera(self):
        """
        Vérifie que la caméra est correctement connectée et prête.
        Retourne True si l'initialisation est réussie, sinon False.
        """
        try:
            result = subprocess.run(
                ["libcamera-still", "-t", "10", "-o", "/dev/null"],
                capture_output=True, text=True
            )
            return result.returncode == 0
        except Exception as e:
            print("Exception lors de l'initialisation de la caméra :", e)
            return False

    def start_video_stream(self, duration, color_detector):
        """
        Démarre un flux vidéo pour une durée donnée, avec détection de couleur en temps réel.
        :param duration: Durée du flux vidéo en secondes.
        :param color_detector: Instance de la classe ColorDetector.
        """
        if not self.initialized:
            print("Erreur : La caméra n'est pas initialisée.")
            return

        try:
            print("Démarrage du flux vidéo...")
            cap = cv2.VideoCapture(0)  # Index de la caméra
            start_time = time.time()

            while time.time() - start_time < duration:
                ret, frame = cap.read()
                if not ret:
                    print("Erreur : Impossible de lire la frame.")
                    break

                # Applique la détection de couleur
                detected = color_detector.detect_color(frame)
                if detected:
                    print("Couleur détectée !")

                # Affiche le flux vidéo (facultatif)
                cv2.imshow("Flux vidéo", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):  # Quitter avec 'q'
                    break

            cap.release()
            cv2.destroyAllWindows()
            print("Flux vidéo terminé.")

        except Exception as e:
            print("Erreur lors du flux vidéo :", e)

    def stop_video_stream(self):
        """
        Arrête le flux vidéo si celui-ci est en cours.
        """
        if self.process:
            print("Arrêt du flux vidéo...")
            self.process.terminate()
            self.process = None
            print("Flux vidéo arrêté")


# Exemple d'utilisation
if __name__ == "__main__":
    # Définir les plages HSV pour le rouge
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Instancier le détecteur de couleur
    color_detector = ColorDetector(lower_red, upper_red)

    # Instancier la classe VisionHexapode
    vision = VisionHexapode()

    if vision.initialized:
        # Démarrer un flux vidéo de 10 secondes avec détection de couleur
        vision.start_video_stream(duration=10, color_detector=color_detector)

        # Arrêter le flux vidéo
        vision.stop_video_stream()
