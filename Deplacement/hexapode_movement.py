from dynamixel_sdk import *  # Import the Dynamixel SDK

# Constants for control table addresses and motor configuration
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132
ADDR_PROFILE_VELOCITY = 112
ADDR_PROFILE_ACCELERATION = 108

TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
DXL_MOVING_STATUS_THRESHOLD = 75
PROFILE_VELOCITY = 70
PROFILE_ACCELERATION = 30

# Movement positions (set these appropriately for your specific hexapod)
# Here, example positions are used for lifting and rotating
lift_positions = {...}  # As defined earlier
rotate_positions = {...}

class HexapodMovement:
    def __init__(self, port, baudrate=1000000):
        # Initialize the PortHandler and PacketHandler
        self.portHandler = PortHandler(port)
        self.packetHandler = PacketHandler(2.0)
        self.groupSyncWrite = GroupSyncWrite(self.portHandler, self.packetHandler, ADDR_GOAL_POSITION, 4)
        self.groupSyncRead = GroupSyncRead(self.portHandler, self.packetHandler, ADDR_PRESENT_POSITION, 4)
        
        if not self.portHandler.openPort():
            raise Exception("Failed to open the port")
        if not self.portHandler.setBaudRate(baudrate):
            raise Exception("Failed to set baudrate")

        # Enable all Dynamixel motors
        self.servos = {
            'lift': [2, 4, 6, 8, 10, 12],
            'rotate': [1, 3, 5, 7, 9, 11]
        }
        self._enable_all_motors()

    def _enable_all_motors(self):
        """Enable torque on all motors."""
        for servo_id in self.servos['lift'] + self.servos['rotate']:
            self.packetHandler.write1ByteTxRx(self.portHandler, servo_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
            self.packetHandler.write4ByteTxRx(self.portHandler, servo_id, ADDR_PROFILE_VELOCITY, PROFILE_VELOCITY)
            self.packetHandler.write4ByteTxRx(self.portHandler, servo_id, ADDR_PROFILE_ACCELERATION, PROFILE_ACCELERATION)

    def _move_to_position(self, ids_positions):
        """Move motors to target positions."""
        for dxl_id, position in ids_positions.items():
            if dxl_id in self.servos['lift']:
                goal_position = lift_positions[dxl_id][position]
            elif dxl_id in self.servos['rotate']:
                goal_position = rotate_positions[dxl_id][position]
            
            param_goal_position = [
                DXL_LOBYTE(DXL_LOWORD(goal_position)),
                DXL_HIBYTE(DXL_LOWORD(goal_position)),
                DXL_LOBYTE(DXL_HIWORD(goal_position)),
                DXL_HIBYTE(DXL_HIWORD(goal_position)),
            ]
            self.groupSyncWrite.addParam(dxl_id, param_goal_position)
        
        # Syncwrite the goal positions
        self.groupSyncWrite.txPacket()
        self.groupSyncWrite.clearParam()

    def forward(self):
        """Move hexapod forward."""
        self._move_to_position({1: 1, 7: 1, 9: 1, 3: 0, 5: 0, 11: 0})

    def backward(self):
        """Move hexapod backward."""
        self._move_to_position({1: 0, 7: 0, 9: 0, 3: 1, 5: 1, 11: 1})

    def left(self):
        """Move hexapod left."""
        self._move_to_position({2: 1, 4: 1, 6: 1, 8: 0, 10: 0, 12: 0})

    def right(self):
        """Move hexapod right."""
        self._move_to_position({2: 0, 4: 0, 6: 0, 8: 1, 10: 1, 12: 1})

    def rotate(self, direction):
        """Rotate hexapod in place. direction: 'left' or 'right'."""
        if direction == 'left':
            self._move_to_position({1: 0, 3: 0, 5: 0, 7: 1, 9: 1, 11: 1})
        elif direction == 'right':
            self._move_to_position({1: 1, 3: 1, 5: 1, 7: 0, 9: 0, 11: 0})

    def stop(self):
        """Stop the hexapod by disabling torque."""
        for servo_id in self.servos['lift'] + self.servos['rotate']:
            self.packetHandler.write1ByteTxRx(self.portHandler, servo_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)

    def close(self):
        """Close the port when finished."""
        self.portHandler.closePort()
