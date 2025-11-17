from dataclasses import dataclass
from states import *

@dataclass
class PlayerState():
    horizontal : HorizontalState
    vertical : VerticalState
    bounce: BounceState
    double_jump : DoubleJumpState
    rotate : RotateState

    def __iter__(self):
        yield self.horizontal
        yield self.vertical
        yield self.double_jump
        yield self.bounce
        yield self.rotate

player_state = PlayerState(
    horizontal=HorizontalState.IDLE,
    vertical=VerticalState.GROUNDED,
    bounced=BounceState.BOUNCED,
    double_jumps=DoubleJumpState.NO,
    rotating=RotateState.IDLE )
