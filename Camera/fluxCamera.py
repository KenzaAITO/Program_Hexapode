from picamera2 import Picamera2, Preview
import time

class Camera:
    def __init__(self):
        # Initialisation de la caméra
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration())

    def start_stream(self, duration=10):
        """Démarre le flux vidéo pendant une durée donnée (en secondes)."""
        print("Démarrage du flux vidéo...")
        self.picam2.start_preview(Preview.QTGL)  # Affichage dans une fenêtre
        self.picam2.start()
        time.sleep(duration)  # Durée du flux
        self.picam2.stop_preview()
        self.picam2.stop()
        print("Flux vidéo terminé.")

    def capture_image(self, filename="image.jpg"):
        """Capture une image et l'enregistre sous le nom spécifié."""
        print(f"Capture de l'image et enregistrement sous '{filename}'")
        self.picam2.configure(self.picam2.create_still_configuration())
        self.picam2.start()
        time.sleep(2)  # Temps pour laisser la caméra s'ajuster
        self.picam2.capture_file(filename)
        self.picam2.stop()
        print(f"Image enregistrée sous '{filename}'.")

# Exemple d'utilisation
if __name__ == "__main__":
    camera = Camera()
    camera.start_stream(duration=10)  # Lancer le flux vidéo pendant 10 secondes
    # camera.capture_image("photo.jpg")  # Décommentez pour capturer une image
