from picamera2 import Picamera2, Preview
import time

# Initialisation de la caméra
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())

# Affichage de l'aperçu de la caméra dans une fenêtre
picam2.start_preview(Preview.QTGL)

# Démarrer la caméra
picam2.start()
time.sleep(10)  # Laisser le flux pendant 10 secondes

# Arrêter la caméra
picam2.stop()
print("Flux vidéo terminé.")
