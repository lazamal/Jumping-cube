from utils import lerp


class Animation():
    def __init__(self, state_enum):
        self.start = 0
        self.end = 0
        self.t = 0
        self.state = state_enum
        self.current_state = state_enum(1)
        self.direction = 0
        self.duration = 0
        self.final = 0


    def start_movement(self, new_start, target, direction, duration):
        if self.current_state == self.state(1):
            if len(self.state) > 2:
                self.current_state = (
                self.state(2) if direction > 0 else self.state(3)
            )
            else:
                self.current_state = self.state(2)

            self.start = new_start
            self.ending_movement = self.start + target * direction
            self.movement_t = 0
            self.movement_duration = duration

    def update_movement(self,dt):
        if self.current_state != self.state(1):
            self.t += dt / self.duration
            if self.t >= 1:
                self.t=1
                self.final = self.ending_movement
                self.current_state = self.state(1)
            else:
                
                self.final = lerp(self.start, self.end, self.t)
                return self.final, self.current_state
