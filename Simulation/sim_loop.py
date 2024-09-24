from sim_visualization import simulate_color_detection
from sim_deplacement import move_to_position
import time

def simulation_loop():
    global red_detected_flag, green_detected_flag
    while True:
        red_detected, green_detected = simulate_color_detection()

        if red_detected:
            print("Simulated: Red detected!")
            red_detected_flag = True

        if green_detected:
            print("Simulated: Green detected!")
            green_detected_flag = True

        # Simulate the robot's response to detected colors
        if red_detected_flag:
            # Move the "hexapod"
            move_to_position({1: 1, 7: 0, 9: 1})
            red_detected_flag = False
            
        if green_detected_flag:
            move_to_position({1: 0, 7: 1, 9: 0})
            green_detected_flag = False

        time.sleep(1)  # Simulate time delay in loop

simulation_loop()
