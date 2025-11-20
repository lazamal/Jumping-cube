from dataclasses import dataclass, fields
from states import *

@dataclass
class PlayerState():
    horizontal : HorizontalState
    vertical : VerticalState
    bounce: BounceState
    double_jump : DoubleJumpState
    rotate : RotateState
    shape: ShapeState

    def __iter__(self):
        for state in fields(self):
            yield state.name, state.type, getattr(self, state.name)


PLAYER_STATE = PlayerState(
    horizontal=HorizontalState.IDLE,
    vertical=VerticalState.GROUNDED,
    bounce=BounceState.BOUNCED,
    double_jump=DoubleJumpState.NO,
    rotate=RotateState.IDLE,
    shape = ShapeState.IDLE_SQUARE )
