from enum import Enum, auto

class HorizontalState(Enum):
    IDLE = auto()
    MOVING_LEFT = auto()
    MOVING_RIGHT = auto()

class VerticalState(Enum):
    JUMPING=auto()
    FALLING=auto()
    BOUNCING=auto()
    GROUNDED=auto()

class DoubleJumpState(Enum):
    YES = auto()
    NO = auto()

class BounceState(Enum):
    BOUNCED= auto()
    DID_NOT_BOUNCE= auto()

class RotateState(Enum):
    IDLE = auto()
    ROTATING= auto()
