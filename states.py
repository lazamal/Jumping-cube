from enum import StrEnum, auto

class HorizontalState(StrEnum):
    IDLE =  auto()
    MOVING_LEFT = auto()
    MOVING_RIGHT = auto()

class VerticalState(StrEnum):
    JUMPING=auto()
    FALLING=auto()
    BOUNCING=auto()
    GROUNDED=auto()

class DoubleJumpState(StrEnum):
    YES = auto()
    NO = auto()

class BounceState(StrEnum):
    BOUNCED= auto()
    DID_NOT_BOUNCE= auto()

class RotateState(StrEnum):
    IDLE = auto()
    ROTATING= auto()

class ShapeState(StrEnum):
    IDLE_SQUARE = auto()
    IDLE_CIRCLE = auto()
    MORPH_TO_SQUARE = auto()
    MORPH_TO_CIRCLE =auto()
