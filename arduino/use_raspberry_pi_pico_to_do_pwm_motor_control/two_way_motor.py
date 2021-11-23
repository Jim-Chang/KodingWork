from machine import PWM, Pin

_FULL_DUTY = 65535

FORWARD = 0
BACKWARD = 1

class TwoWayMotor:

    def __init__(self, pin_forward: int, pin_backward: int):
        self.pwm_f = PWM(Pin(pin_forward))
        self.pwm_b = PWM(Pin(pin_backward))
        self.pwm_f.duty_u16(0)
        self.pwm_b.duty_u16(0)

    # speed: 0 ~ 100
    def set_speed(self, speed: int, direction: int):
        if direction == FORWARD:
            self.pwm_f.duty_u16(int(_FULL_DUTY * (speed / 100)))
            self.pwm_b.duty_u16(0)

        else:
            self.pwm_f.duty_u16(0)