from enum import Enum, auto

class VerticalState(Enum):
    
    JUMPING=auto()
    FALLING=auto()
    BOUNCING=auto()
    GROUNDED=auto()
    DOUBLE_JUMP = auto()

state = VerticalState

print(state(1))