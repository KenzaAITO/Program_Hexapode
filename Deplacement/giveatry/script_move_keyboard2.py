import keyboard
from hexapod_movement import HexapodMovement
import time

def main():
    hexapod = HexapodMovement(port="/dev/ttyUSB0")
    
    try:
        print("Control the hexapod using the arrow keys. 'O' to rotate. Press 'Esc' to stop.")
        
        # Initialize a dictionary to track key states
        key_states = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'o': False
        }
        
        # Infinite loop to listen for key presses
        while True:
            # Check if the 'up' arrow key is pressed
            if keyboard.is_pressed('up') and not key_states['up']:
                key_states['up'] = True
                print("Moving forward")
                hexapod.forward()
            
            # When the key is released, stop the movement
            if not keyboard.is_pressed('up') and key_states['up']:
                key_states['up'] = False
                hexapod.stop()
            
            # Check if the 'down' arrow key is pressed
            if keyboard.is_pressed('down') and not key_states['down']:
                key_states['down'] = True
                print("Moving backward")
                hexapod.backward()

            if not keyboard.is_pressed('down') and key_states['down']:
                key_states['down'] = False
                hexapod.stop()

            # Check if the 'left' arrow key is pressed
            if keyboard.is_pressed('left') and not key_states['left']:
                key_states['left'] = True
                print("Moving left")
                hexapod.left()
            
            if not keyboard.is_pressed('left') and key_states['left']:
                key_states['left'] = False
                hexapod.stop()

            # Check if the 'right' arrow key is pressed
            if keyboard.is_pressed('right') and not key_states['right']:
                key_states['right'] = True
                print("Moving right")
                hexapod.right()
            
            if not keyboard.is_pressed('right') and key_states['right']:
                key_states['right'] = False
                hexapod.stop()

            # Check if the 'O' key is pressed for rotation
            if keyboard.is_pressed('o') and not key_states['o']:
                key_states['o'] = True
                print("Rotating")
                hexapod.rotate('left')  # Change to 'right' if needed
            
            if not keyboard.is_pressed('o') and key_states['o']:
                key_states['o'] = False
                hexapod.stop()

            # Exit the loop if 'Esc' is pressed
            if keyboard.is_pressed('esc'):
                print("Exiting...")
                break
            
            # Add a small delay to prevent high CPU usage
            time.sleep(0.01)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        hexapod.stop()  # Ensure hexapod stops when exiting
        hexapod.close()  # Close the port

if __name__ == "__main__":
    main()
