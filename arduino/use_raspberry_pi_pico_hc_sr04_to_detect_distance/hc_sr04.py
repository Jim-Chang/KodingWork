from machine import Pin, time_pulse_us
import time

class HCSR04:

    def __init__(self, trig_pin: int, echo_pin: int):
        self.trig_pin = Pin(trig_pin, Pin.OUT)
        self.echo_pin = Pin(echo_pin, Pin.IN)

        self.trig_pin.low()

    def get_distance_in_cm(self):
        self._send_trig()
        echo_t = self._receive_echo()

        if echo_t >= 0:
            return (echo_t / 2.0) / 29  # 1 / 29 = 0.034
       
        # if timeout, return -1
        return -1

    def _send_trig(self):
        # send trig high
        self.trig_pin.high()
        time.sleep_us(10)

        # complete trig
        self.trig_pin.low()

    def _receive_echo(self):
        echo_t = time_pulse_us(self.echo_pin, 1, 58000)
        if echo_t == -2:
            print('timeout to wait echo to be high.')
        if echo_t == -1:
            print('timeout to measure echo pulse width')
        return echo_t