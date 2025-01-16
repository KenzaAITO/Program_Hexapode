import cv2

# Ouvrir le flux vidéo de la caméra
cap = cv2.VideoCapture('libcamera-vid -t 0 --inline --output -')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Afficher le flux vidéo
    cv2.imshow('Camera Stream', frame)

    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la caméra et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()