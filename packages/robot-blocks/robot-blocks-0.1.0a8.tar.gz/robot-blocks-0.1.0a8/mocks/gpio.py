import random

class Pwm:
    @staticmethod
    def start(_int: int):
        return

    @staticmethod
    def ChangeDutyCycle(duty_cycle):
        return

class GPIO:
    BCM = 1
    OUT = True
    IN = True

    @staticmethod
    def PWM(forwards_pin, frequency):
        return Pwm

    @staticmethod
    def setup(pin, mode):
        return

    @staticmethod
    def setmode(mode):
        return

    @staticmethod
    def setwarnings(mode: bool):
        return

    @staticmethod
    def input(pin):
        return random.randint(0, 1)

    @staticmethod
    def output(pin, bool):
        return