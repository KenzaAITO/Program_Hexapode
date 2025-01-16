import cv2
import numpy as np
import os
import time
import threading
from dynamixel_sdk import *  # Uses Dynamixel SDK library

MY_DXL = 'X_SERIES'  # X330 (5.0 V recommended), X430, X540, 2X430
 

ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
LEN_GOAL_POSITION = 4  # Data Byte Length
ADDR_PRESENT_POSITION = 132
LEN_PRESENT_POSITION = 4  # Data Byte Length

ADDR_PROFILE_VELOCITY = 112  # Profile Velocity
ADDR_PROFILE_ACCELERATION = 108  # Profile Acceleration
 
# Movement positions
DXL_MINIMUM_POSITION_VALUE_HB = 2200

DXL_MAXIMUM_POSITION_VALUE_HB = 1210

DXL_MINIMUM_POSITION_VALUE_GD1 = 2500

DXL_MAXIMUM_POSITION_VALUE_GD1 = 3000

DXL_MINIMUM_POSITION_VALUE_GD3 = 1650

DXL_MAXIMUM_POSITION_VALUE_GD3 = 1150

DXL_MINIMUM_POSITION_VALUE_GD5 = 890

DXL_MAXIMUM_POSITION_VALUE_GD5 = 1390

DXL_MINIMUM_POSITION_VALUE_GD7 = 1100

DXL_MAXIMUM_POSITION_VALUE_GD7 = 600

DXL_MINIMUM_POSITION_VALUE_GD9 = 1150

DXL_MAXIMUM_POSITION_VALUE_GD9 = 1650

DXL_MINIMUM_POSITION_VALUE_GD11 = 3000

DXL_MAXIMUM_POSITION_VALUE_GD11 = 2500
 
# Set the profile velocity and acceleration
PROFILE_VELOCITY = 50
PROFILE_ACCELERATION = 10
 
BAUDRATE = 1000000
 
# Protocol version
PROTOCOL_VERSION = 2.0
 
# Dynamixel IDs for lift and rotate
LIFT_SERVOS = [2, 4, 6, 8, 10, 12]
ROTATE_SERVOS = [id - 1 for id in LIFT_SERVOS]
 
# Port
DEVICENAME = '/dev/ttyUSB0'
 
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
DXL_MOVING_STATUS_THRESHOLD = 80
 
# Goal positions for lifting and rotating
lift_positions = {
    2: [DXL_MINIMUM_POSITION_VALUE_HB, DXL_MAXIMUM_POSITION_VALUE_HB],
    4: [DXL_MINIMUM_POSITION_VALUE_HB, DXL_MAXIMUM_POSITION_VALUE_HB],
    6: [DXL_MINIMUM_POSITION_VALUE_HB, DXL_MAXIMUM_POSITION_VALUE_HB],
    8: [DXL_MINIMUM_POSITION_VALUE_HB, DXL_MAXIMUM_POSITION_VALUE_HB],
    10: [DXL_MINIMUM_POSITION_VALUE_HB, DXL_MAXIMUM_POSITION_VALUE_HB],
    12: [DXL_MINIMUM_POSITION_VALUE_HB, DXL_MAXIMUM_POSITION_VALUE_HB]
}
 
rotate_positions = {
    1: [DXL_MINIMUM_POSITION_VALUE_GD1, DXL_MAXIMUM_POSITION_VALUE_GD1],
    3: [DXL_MINIMUM_POSITION_VALUE_GD3, DXL_MAXIMUM_POSITION_VALUE_GD3],
    5: [DXL_MINIMUM_POSITION_VALUE_GD5, DXL_MAXIMUM_POSITION_VALUE_GD5],
    7: [DXL_MINIMUM_POSITION_VALUE_GD7, DXL_MAXIMUM_POSITION_VALUE_GD7],
    9: [DXL_MINIMUM_POSITION_VALUE_GD9, DXL_MAXIMUM_POSITION_VALUE_GD9],
    11: [DXL_MINIMUM_POSITION_VALUE_GD11, DXL_MAXIMUM_POSITION_VALUE_GD11]
}
 
# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)
 
# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)
 
# Initialize GroupSyncWrite instance
groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
 
# Initialize GroupSyncRead instance for Present Position
groupSyncRead = GroupSyncRead(portHandler, packetHandler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
 
# Open port
if not portHandler.openPort():
    print("Failed to open the port")
    exit()
print("Succeeded to open the port")
 
# Set port baudrate
if not portHandler.setBaudRate(BAUDRATE):
    print("Failed to change the baudrate")
    exit()
print("Succeeded to change the baudrate")
 
# Enable Dynamixel Torque
for dxl_id in LIFT_SERVOS + ROTATE_SERVOS:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Error enabling torque for Dynamixel {dxl_id}: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"Error enabling torque for Dynamixel {dxl_id}: {packetHandler.getRxPacketError(dxl_error)}")
    else:
        print(f"Dynamixel#{dxl_id} has been successfully connected")
 
# Set profile velocity and acceleration
for dxl_id in LIFT_SERVOS + ROTATE_SERVOS:
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dxl_id, ADDR_PROFILE_VELOCITY, PROFILE_VELOCITY)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Error setting profile velocity for Dynamixel {dxl_id}: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"Error setting profile velocity for Dynamixel {dxl_id}: {packetHandler.getRxPacketError(dxl_error)}")
 
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dxl_id, ADDR_PROFILE_ACCELERATION, PROFILE_ACCELERATION)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Error setting profile acceleration for Dynamixel {dxl_id}: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"Error setting profile acceleration for Dynamixel {dxl_id}: {packetHandler.getRxPacketError(dxl_error)}")
 
# Add parameter storage for present position values
for dxl_id in LIFT_SERVOS + ROTATE_SERVOS:
    dxl_addparam_result = groupSyncRead.addParam(dxl_id)
    if not dxl_addparam_result:
        print(f"[ID:{dxl_id:03d}] groupSyncRead addparam failed")
        exit()
 
def move_to_position(ids_positions):
    for dxl_id, position in ids_positions.items():
        if dxl_id in LIFT_SERVOS:
            goal_position = lift_positions[dxl_id][position]
        elif dxl_id in ROTATE_SERVOS:
            goal_position = rotate_positions[dxl_id][position]
        else:
            continue
 
        param_goal_position = [
            DXL_LOBYTE(DXL_LOWORD(goal_position)),
            DXL_HIBYTE(DXL_LOWORD(goal_position)),
            DXL_LOBYTE(DXL_HIWORD(goal_position)),
            DXL_HIBYTE(DXL_HIWORD(goal_position))
        ]
        dxl_addparam_result = groupSyncWrite.addParam(dxl_id, param_goal_position)
        if not dxl_addparam_result:
            print(f"[ID:{dxl_id:03d}] groupSyncWrite addparam failed")
            exit()
 
    dxl_comm_result = groupSyncWrite.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Error during SyncWrite: {packetHandler.getTxRxResult(dxl_comm_result)}")
 
    groupSyncWrite.clearParam()
 
    while True:
        dxl_comm_result = groupSyncRead.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print(f"Error during SyncRead: {packetHandler.getTxRxResult(dxl_comm_result)}")
 
        all_reached = True
        for dxl_id in ids_positions.keys():
            dxl_present_position = groupSyncRead.getData(dxl_id, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
            if dxl_present_position is None:
                print(f"Error reading position for Dynamixel {dxl_id}")
                all_reached = False
                break
            if dxl_id in LIFT_SERVOS:
                goal_position = lift_positions[dxl_id][ids_positions[dxl_id]]
            elif dxl_id in ROTATE_SERVOS:
                goal_position = rotate_positions[dxl_id][ids_positions[dxl_id]]
            else:
                continue
 
            if abs(goal_position - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
                all_reached = False
                break
 
        if all_reached:
            break
 
def detect_color(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
 
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])
 
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
 
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
    red_detected = any(cv2.contourArea(contour) > 1000 for contour in contours_red)
    green_detected = any(cv2.contourArea(contour) > 1000 for contour in contours_green)
 
    return red_detected, green_detected
 
def camera_thread_function():
    global red_detected_flag, green_detected_flag, camera_active
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Utiliser l'index approprié pour votre caméra et V4L2 backend
 
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la caméra.")
        camera_active = False
        return
 
    camera_active = True
 
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erreur: Impossible de capturer l'image.")
                break
 
            red_detected, green_detected = detect_color(frame)
 
            if red_detected:
                print("Forme rouge détectée!")
                red_detected_flag = True
                time.sleep(3) 
            if green_detected:
                print("Forme verte détectée!")
                green_detected_flag = True
                time.sleep(3) 
 
            time.sleep(1)  # Attendre 1 seconde avant de capturer la prochaine image
 
    finally:
        cap.release()
        cv2.destroyAllWindows()
 
# Initialiser les flags de contrôle du robot
red_detected_flag = False
green_detected_flag = False
camera_active = True
 
# Démarrer le thread de la caméra
camera_thread = threading.Thread(target=camera_thread_function)
camera_thread.start()
 
try:
    while True:
        if red_detected_flag:
            
            for _ in range(3):
                move_to_position({1: 1, 7: 0, 9: 1})
                move_to_position({2: 0, 8: 0, 10: 0})
                move_to_position({4: 1, 6: 1, 12: 1})
                move_to_position({1: 0, 7: 1, 9: 0})
                move_to_position({3: 0, 5: 1, 11: 0})
                move_to_position({4: 0, 6: 0, 12: 0})
                move_to_position({2: 1, 8: 1, 10: 1})
                move_to_position({3: 0, 5: 1, 11: 0})
            red_detected_flag = False
        if green_detected_flag:
            
            for _ in range(3):
                move_to_position({1: 0, 7: 1, 9: 0})
                move_to_position({2: 0, 8: 0, 10: 0})
                move_to_position({4: 1, 6: 1, 12: 1})
                move_to_position({1: 1, 7: 0, 9: 1})
                move_to_position({3: 1, 5: 0, 11: 1})
                move_to_position({4: 0, 6: 0, 12: 0})
                move_to_position({2: 1, 8: 1, 10: 1})
                move_to_position({3: 0, 5: 1, 11: 0})
            green_detected_flag = False
        if not red_detected_flag and not green_detected_flag:
                move_to_position({1: 1, 7: 1, 9: 1})

                move_to_position({2: 0, 8: 0, 10: 0})
                #le monte pour facilité la rotation
                move_to_position({4: 1, 6: 1, 12: 1})

                move_to_position({1: 0, 7: 0, 9: 0})



                # Move group 2 to max position

                move_to_position({3: 1, 5: 1, 11: 1})



                # Move group 2 to min position

                move_to_position({4: 0, 6: 0, 12: 0})
                move_to_position({2: 1, 8: 1, 10: 1})

                move_to_position({3: 0, 5: 0, 11: 0})
 
finally:
    camera_thread.join()
    # Disable Dynamixel Torque
    for dxl_id in LIFT_SERVOS + ROTATE_SERVOS:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print(f"Error disabling torque for Dynamixel {dxl_id}: {packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            print(f"Error disabling torque for Dynamixel {dxl_id}: {packetHandler.getRxPacketError(dxl_error)}")
 
    # Close port
    portHandler.closePort()