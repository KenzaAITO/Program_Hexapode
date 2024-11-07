from Deplacement import HexapodMovement

def main():
    hexapod = HexapodMovement(port="/dev/ttyUSB0")

    try:
        hexapod.forward()
        hexapod.left()
        hexapod.rotate('right')
        hexapod.backward()
        hexapod.right()
        hexapod.rotate('left')
        
    finally:
        hexapod.stop()
        hexapod.close()

if __name__ == "__main__":
    main()
