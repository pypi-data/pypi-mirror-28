from .sensors import ClearMockedSensor
from .gpio import GPIO


class Robot(object):
    sensors = [ClearMockedSensor(GPIO, position='FRONT')]

    def __init__(self, *args, **kwargs):
        """"""

    def add_callback(self, hook, callback):
        """"""

    def brake(self):
        """"""