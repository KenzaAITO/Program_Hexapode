import pygame
import numpy as np
from PIL import Image, ImageOps

class Camera:
    def __init__(self):
        # Initialiser la caméra avec pygame
        pygame.camera.init()
        self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (640, 480))
        self.cam.start()

    def start_stream(self, detector):
        """Démarre le flux vidéo et transmet chaque image au détecteur de couleur."""
        print("Démarrage du flux vidéo...")
        running = True

        while running:
            # Capture une image depuis la caméra
            img_surface = self.cam.get_image()

            # Convertir l'image Pygame en image PIL pour traitement
            img_array = pygame.surfarray.array3d(img_surface)
            img_pil = Image.fromarray(np.transpose(img_array, (1, 0, 2)))

            # Appliquer la détection de couleur
            color_image = detector.detect_color(img_pil)

            # Afficher l'image originale et celle avec la détection de couleur
            img_original = np.array(img_pil)
            img_detected = np.array(color_image)

            pygame.surfarray.blit_array(img_surface, np.transpose(img_detected, (1, 0, 2)))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        self.cam.stop()
        print("Flux vidéo terminé.")


class ColorDetector:
    def __init__(self, target_color, tolerance=60):
        """
        Initialise le détecteur de couleur avec la couleur cible et une tolérance.
        :param target_color: La couleur cible (en RGB) à détecter.
        :param tolerance: La tolérance pour la détection des couleurs.
        """
        self.target_color = target_color
        self.tolerance = tolerance

    def detect_color(self, image):
        """Détecte la couleur cible dans l'image et renvoie une nouvelle image avec la couleur détectée."""
        # Convertir l'image PIL en format numpy
        image_np = np.array(image)

        # Définir les limites pour la détection des couleurs
        lower_bound = np.maximum(self.target_color - self.tolerance, 0)
        upper_bound = np.minimum(self.target_color + self.tolerance, 255)

        # Créer un masque pour les pixels correspondant à la couleur cible
        mask = np.all(np.logical_and(image_np >= lower_bound, image_np <= upper_bound), axis=-1)

        # Appliquer le masque sur l'image originale
        result = np.zeros_like(image_np)
        result[mask] = image_np[mask]
        
        return Image.fromarray(result)


# Exemple d'utilisation
if __name__ == "__main__":
    # Couleur cible : rouge (en RGB)
    target_color = np.array([255, 0, 0])

    # Créer l'instance du détecteur de couleur
    color_detector = ColorDetector(target_color)

    # Créer une instance de la caméra et démarrer le flux vidéo avec détection de couleur
    camera = Camera()
    camera.start_stream(color_detector)
