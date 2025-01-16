import os
import time
from dynamixel_sdk import *

# Définir le modèle Dynamixel et les paramètres
DEVICES = [f"/dev/tty{i}" for i in range(0, 64)] + ["/dev/ttyUSB0"]  # Liste des ports à tester
BAUDRATE = 1000000
PROTOCOL_VERSION = 2.0
DXL_ID = 1  # ID du moteur à tester
ADDR_TORQUE_ENABLE = 64
ADDR_PRESENT_POSITION = 132

def test_dynamixel(port):
    # Initialiser le port et le paquet
    portHandler = PortHandler(port)
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    # Ouvrir le port
    if not portHandler.openPort():
        print(f"Failed to open the port: {port}")
        return False

    # Définir le baudrate
    if not portHandler.setBaudRate(BAUDRATE):
        print(f"Failed to change the baudrate on port: {port}")
        portHandler.closePort()
        return False

    # Activer le couple
    packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, 1)
    time.sleep(1)

    # Lire la position actuelle
    present_position, _, _ = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
    print(f"Current position on {port}: {present_position}")

    # Déplacer le moteur (exemple avec une position définie)
    goal_position = 2048  # Remplacez par la position souhaitée
    param_goal_position = [DXL_LOBYTE(DXL_LOWORD(goal_position)),
                           DXL_HIBYTE(DXL_LOWORD(goal_position)),
                           DXL_LOBYTE(DXL_HIWORD(goal_position)),
                           DXL_HIBYTE(DXL_HIWORD(goal_position))]

    packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, goal_position)
    time.sleep(1)

    # Lire la nouvelle position
    present_position, _, _ = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
    print(f"New position on {port}: {present_position}")

    # Désactiver le couple
    packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, 0)

    # Fermer le port
    portHandler.closePort()
    return True

# Itérer à travers chaque port pour tester
for port in DEVICES:
    print(f"Testing port: {port}")
    test_dynamixel(port)
