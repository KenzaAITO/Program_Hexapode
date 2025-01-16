import cv2

# Essaye d'ouvrir les périphériques vidéo
for i in range(5):  # Change le nombre selon le nombre de caméras que tu as
    cap = cv2.VideoCapture(f'/dev/video{i}')
    if cap.isOpened():
        print(f'Caméra ouverte sur {i}: /dev/video{i}')
        ret, frame = cap.read()
        if ret:
            cv2.imshow(f'Flux de la caméra sur /dev/video{i}', frame)
            cv2.waitKey(0)  # Attendre une touche pour fermer
        cap.release()
    else:
        print(f'Impossible d\'ouvrir la caméra sur /dev/video{i}')
