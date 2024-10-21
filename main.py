from Deplacement import HexapodMovement

def main():
    hexapod = HexapodMovement(port="/dev/ttyUSB0")

    try:
        hexapod.forward()
        # Add delays or condition checks to complete movements
        hexapod.backward()
        hexapod.left()
        hexapod.right()
        hexapod.rotate('left')
        hexapod.rotate('right')
    finally:
        hexapod.stop()
        hexapod.close()

if __name__ == "__main__":
    main()
