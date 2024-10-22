import cv2

class Camera:
    def __init__(self):
        # Initialiser la capture vidéo depuis la caméra
        self.cap = cv2.VideoCapture(0)  # 0 correspond à la première caméra disponible

    def start_stream(self):
        """Démarre le flux vidéo et affiche l'aperçu dans une fenêtre."""
        if not self.cap.isOpened():
            print("Impossible d'ouvrir la caméra")
            return

        print("Démarrage du flux vidéo...")

        while True:
            # Lire une image (frame) de la caméra
            ret, frame = self.cap.read()
            if not ret:
                print("Erreur lors de la capture vidéo")
                break

            # Afficher l'image capturée dans une fenêtre
            cv2.imshow('Flux Vidéo', frame)

            # Arrêter le flux si la touche 'q' est appuyée
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Libérer la caméra et fermer la fenêtre
        self.cap.release()
        cv2.destroyAllWindows()
        print("Flux vidéo terminé.")

# Exemple d'utilisation
if __name__ == "__main__":
    camera = Camera()
    camera.start_stream()
