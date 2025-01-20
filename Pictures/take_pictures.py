import cv2
import os
from collections import deque
import time
import numpy as np

# Configuration
PHOTO_DIR = "./photos"  # Dossier pour enregistrer les photos
BUFFER_SIZE = 10               # Nombre de photos à conserver dans le buffer
INTERVAL = 2                   # Intervalle entre les captures (en secondes)

# Couleurs à détecter
def detect_color(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Définir les plages HSV pour les couleurs rouge et vert
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])

    # Masques pour détecter les couleurs
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Trouver les contours pour chaque couleur
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Détecter si une couleur est présente (taille minimale du contour > 1000 px)
    red_detected = any(cv2.contourArea(contour) > 1000 for contour in contours_red)
    green_detected = any(cv2.contourArea(contour) > 1000 for contour in contours_green)

    return red_detected, green_detected

# Fonction pour assurer l'existence du répertoire
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Capture des photos avec buffer circulaire
def capture_photos_with_buffer():
    ensure_directory_exists(PHOTO_DIR)

    # Initialiser la caméra avec GStreamer
    gst_pipeline = (
        "libcamerasrc ! "
        "video/x-raw, width=1920, height=1080, framerate=30/1 ! "
        "videoconvert ! appsink"
    )
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("[ERREUR] Impossible d'accéder à la caméra.")
        return

    # Buffer circulaire pour stocker les noms de fichiers
    buffer = deque(maxlen=BUFFER_SIZE)

    try:
        while True:
            print("[INFO] Capture d'une photo...")
            ret, frame = cap.read()
            if not ret:
                print("[ERREUR] Impossible de lire une image depuis la caméra.")
                break

            # Créer un nom de fichier basé sur l'horodatage
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            photo_path = os.path.join(PHOTO_DIR, f"photo_{timestamp}.jpg")

            # Enregistrer la photo
            cv2.imwrite(photo_path, frame)
            print(f"[INFO] Photo sauvegardée : {photo_path}")

            # Ajouter au buffer circulaire
            buffer.append(photo_path)

            # Supprimer les fichiers hors du buffer
            if len(buffer) == BUFFER_SIZE:
                oldest_photo = buffer.popleft()
                if os.path.exists(oldest_photo):
                    os.remove(oldest_photo)
                    print(f"[INFO] Fichier supprimé du buffer : {oldest_photo}")

            # Analyser les images dans leur ordre d'arrivée
            print("[INFO] Détection des couleurs sur les images...")
            for photo in list(buffer):
                image = cv2.imread(photo)
                red_detected, green_detected = detect_color(image)

                if red_detected:
                    print(f"[INFO] Rouge détecté dans l'image : {photo}")
                if green_detected:
                    print(f"[INFO] Vert détecté dans l'image : {photo}")
                if not red_detected and not green_detected:
                    print(f"[INFO] Aucune couleur détectée dans l'image : {photo}")

            # Pause avant la prochaine capture
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("[INFO] Arrêt manuel par l'utilisateur.")

    finally:
        cap.release()
        print("[INFO] Ressources libérées.")

if __name__ == "__main__":
    capture_photos_with_buffer()
