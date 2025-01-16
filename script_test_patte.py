from dynamixel_sdk import *
import time

DEVICENAME = "/dev/ttyUSB0"
BAUDRATE = 1000000
PROTOCOL_VERSION = 2.0
DXL_ID = 1  # ID du moteur à tester

ADDR_TORQUE_ENABLE = 64
ADDR_PRESENT_POSITION = 132

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

if not portHandler.openPort():
    print("Failed to open the port")
    quit()

if not portHandler.setBaudRate(BAUDRATE):
    print("Failed to change the baudrate")
    quit()

# Activer le couple
packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, 1)

time.sleep(1)

# Lire la position actuelle
present_position, _, _ = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
print(f"Current position: {present_position}")

# Désactiver le couple
packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, 0)

portHandler.closePort()
