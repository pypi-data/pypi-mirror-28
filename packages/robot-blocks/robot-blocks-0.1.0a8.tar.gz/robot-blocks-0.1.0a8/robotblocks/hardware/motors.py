class BaseMotor(object):
    """
    Lowest level motor class
    """
    frequency = 0  # PWM frequency
    duty_cycle = 0  # PWM duty cycle

    def __init__(self, gpio, position):
        self.position = position
        self.gpio = gpio


class DcMotor(BaseMotor):
    """
    DC motor
    """
    frequency = 40
    duty_cycle = 40

    def __init__(self, gpio, position, **kwargs):
        super(DcMotor, self).__init__(gpio, position)

        forward_pin = kwargs.pop('forward_pin')
        backward_pin = kwargs.pop('backward_pin')

        self.gpio.setup(forward_pin, gpio.OUT)
        self.gpio.setup(backward_pin, gpio.OUT)

        self.forwards = self.gpio.PWM(forward_pin, self.frequency)
        self.backwards = self.gpio.PWM(forward_pin, self.frequency)

        self.forwards.start(0)
        self.backwards.start(0)

    def move_backwards(self):
        self.forwards.ChangeDutyCycle(0)
        self.backwards.ChangeDutyCycle(self.duty_cycle)

    def move_forwards(self):
        self.forwards.ChangeDutyCycle(self.duty_cycle)
        self.backwards.ChangeDutyCycle(0)

    def stop(self):
        self.forwards.ChangeDutyCycle(0)
        self.backwards.ChangeDutyCycle(0)


class Servomotor(BaseMotor):
    """
    Servomotor
    """
