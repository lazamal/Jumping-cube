from enum import Enum, auto
from utils import lerp

class HorizontalState(Enum):
    IDLE = auto()
    MOVING_LEFT = auto()
    MOVING_RIGHT = auto()

class Animation():
    def __init__(self, start, end, t, state, direction, duration, final):
        self.start = start
        self.end = end
        self.t = t
        self.state = state
        self.direction = direction
        self.duration = duration   
        self.final = final

    def start_movement(self, new_start, target, direction, duration):
        if self.state == HorizontalState.IDLE:
            self.state = (
            HorizontalState.MOVING_RIGHT if direction > 0 else HorizontalState.MOVING_LEFT
        )
            self.start = new_start
            self.ending_movement = self.start + target * direction
            self.movement_t = 0
            self.movement_duration = duration

    def update_movement(self,dt):
        if self.state != HorizontalState.IDLE:
            self.t += dt / self.duration
            if self.t >= 1:
                self.t=1
                self.final = self.ending_movement
                self.state = HorizontalState.IDLE
            else:
                
                self.final = lerp(self.starting_movement, self.ending_movement, self.movement_t)
                return self.final
