import os
import sys
from dynamixel_sdk import *  # Uses Dynamixel SDK library

# System-specific key listener
if os.name == "nt":
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import termios
    import tty
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


# Dynamixel Configuration
MY_DXL = "X_SERIES"  # Dynamixel model series
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
LEN_GOAL_POSITION = 4  # Data Byte Length
ADDR_PRESENT_POSITION = 132
LEN_PRESENT_POSITION = 4  # Data Byte Length
ADDR_PROFILE_VELOCITY = 112
ADDR_PROFILE_ACCELERATION = 108

# Movement positions (lift and rotate positions for each servo)
position_ranges = {
    "HB": (2200, 1210), "GD1": (2500, 3000), "GD3": (1650, 1150), "GD5": (890, 1390),
    "GD7": (1100, 600), "GD9": (1150, 1650), "GD11": (3000, 2500)
}

# Profile velocity and acceleration settings
PROFILE_VELOCITY = 70
PROFILE_ACCELERATION = 30

# General parameters
BAUDRATE = 1000000
PROTOCOL_VERSION = 2.0
DEVICENAME = "/dev/ttyUSB0"
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
DXL_MOVING_STATUS_THRESHOLD = 75

# Servo IDs for lift and rotate
LIFT_SERVOS = [2, 4, 6, 8, 10, 12]
ROTATE_SERVOS = [id - 1 for id in LIFT_SERVOS]  # IDs for rotate servos are one less than lift servos

# Goal positions for each lift and rotate servo
lift_positions = {id: position_ranges["HB"] for id in LIFT_SERVOS}
rotate_positions = {
    1: position_ranges["GD1"], 3: position_ranges["GD3"], 5: position_ranges["GD5"],
    7: position_ranges["GD7"], 9: position_ranges["GD9"], 11: position_ranges["GD11"]
}


def initialize_dynamixel(portHandler, packetHandler):
    """ Initialize port and configure baudrate. """
    if not portHandler.openPort():
        print("Failed to open the port")
        getch()
        quit()
    print("Succeeded to open the port")

    if not portHandler.setBaudRate(BAUDRATE):
        print("Failed to change the baudrate")
        getch()
        quit()
    print("Succeeded to change the baudrate")


def enable_torque(packetHandler, portHandler, servos):
    """ Enable torque for the given servos. """
    for dxl_id in servos:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
            portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE
        )
        check_comm_result(dxl_comm_result, dxl_error, dxl_id, packetHandler)


def disable_torque(packetHandler, portHandler, servos):
    """ Disable torque for the given servos. """
    for dxl_id in servos:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
            portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE
        )
        check_comm_result(dxl_comm_result, dxl_error, dxl_id, packetHandler)


def check_comm_result(comm_result, error, dxl_id, packetHandler):
    """ Check the communication result and handle errors. """
    if comm_result != COMM_SUCCESS:
        print(f"Error for Dynamixel {dxl_id}: {packetHandler.getTxRxResult(comm_result)}")
    elif error != 0:
        print(f"Error for Dynamixel {dxl_id}: {packetHandler.getRxPacketError(error)}")
    else:
        print(f"Dynamixel#{dxl_id} has been successfully connected")


def set_profile(packetHandler, portHandler, servos, velocity, acceleration):
    """ Set profile velocity and acceleration for the given servos. """
    for dxl_id in servos:
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
            portHandler, dxl_id, ADDR_PROFILE_VELOCITY, velocity
        )
        check_comm_result(dxl_comm_result, dxl_error, dxl_id, packetHandler)

        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
            portHandler, dxl_id, ADDR_PROFILE_ACCELERATION, acceleration
        )
        check_comm_result(dxl_comm_result, dxl_error, dxl_id, packetHandler)


def move_to_position(groupSyncWrite, ids_positions, packetHandler):
    """ Move servos to the target positions. """
    for dxl_id, position in ids_positions.items():
        goal_position = lift_positions[dxl_id][position] if dxl_id in LIFT_SERVOS else rotate_positions[dxl_id][position]
        param_goal_position = [
            DXL_LOBYTE(DXL_LOWORD(goal_position)),
            DXL_HIBYTE(DXL_LOWORD(goal_position)),
            DXL_LOBYTE(DXL_HIWORD(goal_position)),
            DXL_HIBYTE(DXL_HIWORD(goal_position)),
        ]

        if not groupSyncWrite.addParam(dxl_id, param_goal_position):
            print(f"GroupSyncWrite addParam failed for ID:{dxl_id}")
            quit()

    # Syncwrite goal position
    dxl_comm_result = groupSyncWrite.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Error during SyncWrite: {packetHandler.getTxRxResult(dxl_comm_result)}")

    # Clear syncwrite parameter storage
    groupSyncWrite.clearParam()


def main():
    # Initialize PortHandler and PacketHandler
    portHandler = PortHandler(DEVICENAME)
    packetHandler = PacketHandler(PROTOCOL_VERSION)
    groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
    groupSyncRead = GroupSyncRead(portHandler, packetHandler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

    initialize_dynamixel(portHandler, packetHandler)
    enable_torque(packetHandler, portHandler, LIFT_SERVOS + ROTATE_SERVOS)
    set_profile(packetHandler, portHandler, LIFT_SERVOS + ROTATE_SERVOS, PROFILE_VELOCITY, PROFILE_ACCELERATION)

    # Main movement loop
    try:
        while True:
            move_to_position(groupSyncWrite, {1: 1, 7: 1, 9: 1, 3: 0, 5: 0, 11: 0}, packetHandler)
            move_to_position(groupSyncWrite, {2: 0, 8: 0, 10: 0, 4: 1, 6: 1, 12: 1}, packetHandler)
            move_to_position(groupSyncWrite, {1: 0, 7: 0, 9: 0, 3: 1, 5: 1, 11: 1}, packetHandler)
            move_to_position(groupSyncWrite, {4: 0, 6: 0, 12: 0, 2: 1, 8: 1, 10: 1}, packetHandler)
    finally:
        disable_torque(packetHandler, portHandler, LIFT_SERVOS + ROTATE_SERVOS)
        portHandler.closePort()


if __name__ == "__main__":
    main()
