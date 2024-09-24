import random

def simulate_color_detection():
    # Simulate random detection of red or green
    red_detected = random.choice([True, False])
    green_detected = not red_detected if random.random() > 0.5 else False
    return red_detected, green_detected
