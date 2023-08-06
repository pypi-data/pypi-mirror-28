from robotblocks.hardware import BaseObstacleSensor


class BlockedMockSensor(BaseObstacleSensor):
    @property
    def clear(self):
        return False


class ClearMockedSensor(BaseObstacleSensor):
    @property
    def clear(self):
        return True



