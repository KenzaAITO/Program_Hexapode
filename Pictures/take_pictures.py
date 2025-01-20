import cv2
import os
import time
from collections import deque
from threading import Thread

# Chemin du dossier pour sauvegarder les photos
photo_dir = "photos"
if not os.path.exists(photo_dir):
    os.makedirs(photo_dir)

# Fréquence de capture (20 ms)
capture_interval = 0.02  # 20 ms
buffer_duration = 1  # 1 seconde
buffer_size = int(buffer_duration / capture_interval)

# Buffer circulaire pour stocker les photos
photo_buffer = deque(maxlen=buffer_size)

# Initialisation de la caméra
camera = cv2.VideoCapture(0)  # 0 correspond à la première caméra connectée
if not camera.isOpened():
    raise RuntimeError("Impossible d'ouvrir la caméra. Vérifiez la connexion.")

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Résolution
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 50)  # Assurez une fréquence d'images suffisante

# Fonction pour capturer des photos
def capture_photos():
    photo_index = 0
    while True:
        ret, frame = camera.read()  # Capture une image
        if not ret:
            print("Erreur lors de la capture de l'image.")
            continue
        photo_path = os.path.join(photo_dir, f"photo_{photo_index:04d}.jpg")
        cv2.imwrite(photo_path, frame)  # Enregistre l'image
        photo_buffer.append(photo_path)  # Ajouter au buffer
        photo_index += 1
        time.sleep(capture_interval)

# Exemple de traitement de détection de couleurs
def process_photos():
    while True:
        if photo_buffer:
            photo_path = photo_buffer[0]  # Récupère la première image du buffer
            # Charger l'image pour traitement
            frame = cv2.imread(photo_path)
            if frame is not None:
                # Exemple : Détection de la couleur rouge (modifiez pour vos besoins)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                lower_red = (0, 120, 70)
                upper_red = (10, 255, 255)
                mask = cv2.inRange(hsv, lower_red, upper_red)
                detected = cv2.bitwise_and(frame, frame, mask=mask)
                print(f"Traitement de {photo_path} - Détection de couleur effectuée")
            else:
                print(f"Impossible de charger {photo_path}")
            time.sleep(0.1)  # Simule le traitement (ajustez en fonction de votre traitement réel)

# Lancement de la capture et du traitement dans des threads séparés
capture_thread = Thread(target=capture_photos, daemon=True)
processing_thread = Thread(target=process_photos, daemon=True)

capture_thread.start()
processing_thread.start()

# Garder le programme actif
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Arrêt du programme")
    camera.release()
    cv2.destroyAllWindows()
