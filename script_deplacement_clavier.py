import keyboard
from Deplacement.deplacement_hexapode import HexapodMovement

def main():
    hexapod = HexapodMovement(port="/dev/ttyUSB0")
    
    print("Use the arrow keys to control the hexapod and press 'O' to rotate.")
    
    try:
        # Infinite loop to listen for key presses
        while True:
            if keyboard.is_pressed('up'):
                print("Moving forward")
                hexapod.forward()

            elif keyboard.is_pressed('down'):
                print("Moving backward")
                hexapod.backward()

            elif keyboard.is_pressed('left'):
                print("Moving left")
                hexapod.left()

            elif keyboard.is_pressed('right'):
                print("Moving right")
                hexapod.right()

            elif keyboard.is_pressed('o'):
                print("Rotating")
                hexapod.rotate('left')  # Change to 'right' if needed

            # Add a small delay to avoid excessive CPU usage
            keyboard.wait('esc')  # Press 'esc' to stop the loop
            break
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        hexapod.stop()  # Ensure hexapod stops when exiting
        hexapod.close()  # Close the port

if __name__ == "__main__":
    main()
