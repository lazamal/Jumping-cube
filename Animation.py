from PlayerState import PLAYER_STATE
from states import *


class Animation():
    def __init__(self, state_to_change, new_state_value):
        self.start: float = 0
        self.end: float = 0
        self.t: float = 0
        self.duration: float = 1
        self.direction: int = 0
        self.last_direction: int = self.direction
        self.state_to_change: str = state_to_change
        self.new_state_value : Enum = new_state_value
        self.lerp_value : int = 0


    def start_animation(self, direction, duration, target) -> None:
        setattr(PLAYER_STATE, self.state_to_change, self.new_state_value)
        self.start = self.lerp_value
        self.end = self.start + target * direction
        self.t = 0
        self.duration = duration
