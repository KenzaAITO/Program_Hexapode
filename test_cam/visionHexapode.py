import subprocess
import time

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
            # Test de capture pour vérifier que la caméra est opérationnelle
            result = subprocess.run(["libcamera-still", "-t", "100", "-o", "/dev/null"],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                return True
            else:
                print("Erreur d'initialisation de la caméra :", result.stderr)
                return False
        except Exception as e:
            print("Exception lors de l'initialisation de la caméra :", e)
            return False

    def start_video_stream(self, duration=10):
        """
        Démarre un flux vidéo pour une durée donnée, adapté pour l'hexapode.
        :param duration: Durée du flux vidéo en secondes.
        """
        if not self.initialized:
            print("Erreur : La caméra n'est pas initialisée.")
            return
        
        try:
            print("Démarrage du flux vidéo")
            self.process = subprocess.Popen(
                ["libcamera-vid", "-t", f"{duration * 1000}", "--inline", "--nopreview", "-o", "-"]
            )
            time.sleep(duration)
            print("Flux vidéo en cours...")
        
        except Exception as e:
            print("Erreur lors du démarrage du flux vidéo :", e)
            self.stop_video_stream()

    def stop_video_stream(self):
        """
        Arrête le flux vidéo si celui-ci est en cours.
        """
        if self.process:
            print("Arrêt du flux vidéo...")
            self.process.terminate()
            self.process = None
            print("Flux vidéo arrêté")

    # def capture_image(self, filename="image.jpg"):
    #     """
    #     Capture une image et la sauvegarde sous le nom spécifié.
    #     :param filename: Nom du fichier de sortie pour l'image.
    #     """
    #     if not self.initialized:
    #         print("Erreur : La caméra n'est pas initialisée.")
    #         return
        
    #     try:
    #         print(f"Capture d'image pour l'hexapode : {filename}")
    #         subprocess.run(["libcamera-still", "-o", filename, "-t", "1000"])
    #         print(f"Image capturée et sauvegardée sous {filename}")
        
    #     except Exception as e:
    #         print("Erreur lors de la capture de l'image :", e)

# Exemple d'utilisation de la classe
if __name__ == "__main__":
    vision = VisionHexapode()
    
    if vision.initialized:
        # Démarrer un flux vidéo de 5 secondes
        vision.start_video_stream(duration=5)
        
        # Arrêter le flux vidéo
        vision.stop_video_stream()
