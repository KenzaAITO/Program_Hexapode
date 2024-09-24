import random


def simulate_color_detection():
    # Simulate random detection of red or green
    red_detected = random.choice([True, False])
    green_detected = not red_detected if random.random() > 0.5 else False
    return red_detected, green_detected


def simulate_camera_input(color="red"):
    image = np.zeros((480, 640, 3), np.uint8)
    if color == "red":
        cv2.circle(image, (320, 240), 100, (0, 0, 255), -1)  # Red circle
    elif color == "green":
        cv2.circle(image, (320, 240), 100, (0, 255, 0), -1)  # Green circle
    return image
