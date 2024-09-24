# Dynamixel IDs for lift and rotate
LIFT_SERVOS = [2, 4, 6, 8, 10, 12]
ROTATE_SERVOS = [id - 1 for id in LIFT_SERVOS]


class MockDynamixel:
    def __init__(self, id):
        self.id = id
        self.position = 0
    
    def set_goal_position(self, position):
        print(f"Motor {self.id}: Moving to position {position}")
        self.position = position
        return True  # Simulate success

    def get_present_position(self):
        return self.position  # Simulate motor reaching the position

# Replace LIFT_SERVOS and ROTATE_SERVOS with mock objects
lift_servos = {id: MockDynamixel(id) for id in LIFT_SERVOS}
rotate_servos = {id: MockDynamixel(id) for id in ROTATE_SERVOS}

def move_to_position(ids_positions):
    for dxl_id, position in ids_positions.items():
        if dxl_id in lift_servos:
            lift_servos[dxl_id].set_goal_position(position)
        elif dxl_id in rotate_servos:
            rotate_servos[dxl_id].set_goal_position(position)
