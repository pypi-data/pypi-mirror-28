import threading
import time
from blinker import signal
import logging


class BaseObstacleSensor(threading.Thread):
    """
    Lowest level sensor object
    """
    threshold = 0
    constant = False
    output = 0

    _reading = True
    delay = 0

    def __init__(self, gpio, position, **kwargs):
        super(BaseObstacleSensor, self).__init__()
        self.position = position
        self.input_pin = kwargs.pop('input_pin', None)
        self.output_pin = kwargs.pop('output_pin', None)
        self.gpio = gpio
        self.gpio_setup()

    def gpio_setup(self):
        """
        sets up the GPIO pins prior to use
        """
        self.gpio.setup(self.output_pin, self.gpio.OUT)
        self.gpio.setup(self.input_pin, self.gpio.IN)
        self.gpio.output(self.output_pin, False)

    def test(self):
        """
        Must be implemented by subclasses and return a number (e.g. 0 for obstruction, 1 for clear)
        """
        raise NotImplementedError()

    @property
    def clear(self):
        return self.output > self.threshold

    def read(self):
        output = self.test()
        if output < self.threshold:
            signal('ON_OBSTACLE_%s' % self.position).send()
        return output

    def run(self):
        while True:
            self.output = self.read()
            time.sleep(self.delay)
            if not self._reading:
                break

    def stop(self):
        self._reading = False
        self.join()


class InfraredSensor(BaseObstacleSensor):
    """
    Infra red sensor
    """
    threshold = 0.1  # self.test() will return 0 if not clear or 1 if clear

    def test(self):
        return self.gpio.input(self.input_pin) == 0


class UltrasoundSensor(BaseObstacleSensor):
    """
    Ultrasound sensor
    """
    threshold = 30  # when self.test() returns less than this value, self.clear will return False
    delay = 0.1

    def test(self):
        """
        Takes a reading from the ultrasound sensor and returns the distance in cm
        """
        pulse_end, pulse_start = 0, 0
        self.gpio.output(self.output_pin, True)
        time.sleep(0.00001)
        self.gpio.output(self.output_pin, False)

        while self.gpio.input(self.input_pin) == 0:
            pulse_start = time.time()

        while self.gpio.input(self.input_pin) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = round(pulse_duration * 17150, 2)
        logging.info('Ultrasound sensor at position %s returned a reading of %s cm' % (self.position, distance))
        return distance
