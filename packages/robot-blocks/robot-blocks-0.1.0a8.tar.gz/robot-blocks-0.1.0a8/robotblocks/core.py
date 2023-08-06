try:
    from RPi import GPIO
except ImportError:
    from mocks.gpio import GPIO

from blinker import signal
from .hardware import DcMotor
from .movement import ObstacleAvoidance
import importlib

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class RobotException(Exception):
    pass


class Robot(object):
    """
    Base robot object
    """
    # TODO: Implement methods for checking whether a GPIO pin is appropriate for its provided use
    # TODO: create remove_motor() method
    # TODO: remove controller_types property

    hooks = [
        'ON_REVERSE_START',
        'ON_FORWARDS_START',
        'ON_LEFT_START',
        'ON_RIGHT_START',
        'ON_BRAKE',
        'ON_REVERSE_END',
        'ON_FORWARDS_END',
        'ON_LEFT_END',
        'ON_RIGHT_END',
    ]

    positions = [
        'FRONT_LEFT', 'FRONT', 'FRONT_RIGHT',
        'LEFT', 'RIGHT',
        'REAR_LEFT', 'REAR', 'REAR_RIGHT'
    ]

    sensor_types = ['Ultrasound', 'Infrared']
    sensor_module = '.hardware'

    for position in positions:
        hooks.append('ON_OBSTACLE_%s' % position)

    motor_sides = ['LEFT', 'RIGHT']
    controller_types = ['DRIVE', 'AUXILIARY']

    def __init__(self, movement_mode=ObstacleAvoidance):
        """
        Creates a new Robot instance

        :param movement_mode: the controlling logic. Defaults to ObstacleAvoidance
        """
        self.sensors = []
        self.motors = []
        self.used_gpio_pins = []
        self.callbacks = {}
        self._hooks = {}
        self.movement = None
        for hook in self.hooks:
            self._hooks[hook] = signal(hook)

        self.movement_mode = movement_mode(self)

    def add_motor(self, position: str, forward_pin: int, backward_pin: int, motor_type=DcMotor) -> None:
        """
        Register a motor for the robot. Raises and error if either the input_pin or output_pin is already in use
        elsewhere on the robot

        :param str position: must be LEFT or RIGHT
        :param int forward_pin: GPIO IN
        :param int backward_pin: GPIO OUT
        :param motor_type: the motor type (e.g DC, servo)
        :type motor_type: hardware.motors.BaseMotor
        """
        assert position in self.motor_sides

        try:
            assert forward_pin not in self.used_gpio_pins
            assert backward_pin not in self.used_gpio_pins
        except AssertionError:
            raise RobotException('One of the pins you have provided (%i and %i) is already in use' % (forward_pin,
                                                                                                      backward_pin))

        motor = motor_type(gpio=GPIO, position=position, forward_pin=forward_pin, backward_pin=backward_pin)

        self.used_gpio_pins.append(forward_pin)
        self.used_gpio_pins.append(backward_pin)

        self.motors.append(motor)

    def remove_sensors(self, position):
        """
        De-registers a sensor

        :param position: the position from which to remove a sensor
        """
        # TODO: consider updating this function to remove a specific sensor, instead of all sensors at a position
        sensors = self.get_sensors(position)
        pins = [s.input_pin for s in sensors] + [s.output_pin for s in sensors]

        [self.used_gpio_pins.remove(i) for i in pins]
        [self.sensors.remove(i) for i in self.sensors if i.position == position]

    def add_sensor(self, sensor_type: str, position: str, input_pin: [int, None]=None,
                   output_pin: [int, None]=None, replace: bool=False) -> None:
        """
        Register a sensor for the robot

        :param sensor_type: the type of sensor -  Ultrasound or Infrared
        :param str position: the sensor position
        :param int input_pin: GPIO IN
        :param int output_pin: GPIO OUT
        :param bool replace: replace existing sensor(s) at this position
        """

        assert position in self.positions
        assert sensor_type in self.sensor_types

        try:
            assert input_pin not in self.used_gpio_pins
            assert output_pin not in self.used_gpio_pins
        except AssertionError:
            if not replace:
                raise RobotException('One of the pins you have provided (%i and %i) is already in use' % (input_pin,
                                                                                                          output_pin))

        if replace:
            existing = self.get_sensors(position)

            if not existing:
                raise RobotException('Cannot replace sensors, as there are no existing sensors at this position (%s)' %
                                     position)

            self.remove_sensors(position)

        self.used_gpio_pins.append(input_pin)
        self.used_gpio_pins.append(output_pin)

        sensor_module = importlib.import_module(self.sensor_module)
        _sensor_type = getattr(sensor_module, sensor_type)
        sensor = _sensor_type(gpio=GPIO, position=position, input_pin=input_pin, output_pin=output_pin)

        self.sensors.append(sensor)

    @property
    def turnable(self):
        return all([self.left_motors] + [self.right_motors])

    @property
    def movable(self):
        return any(self.motors)

    @property
    def left_motors(self):
        return [motor for motor in self.motors if motor.position == 'LEFT']

    @property
    def right_motors(self):
        return [motor for motor in self.motors if motor.position == 'RIGHT']

    def add_callback(self, hook, action):
        """
        Binds a function to a callback

        :param function action: the function to call on a specific hook
        :param str hook: the hook to attach the callback to
        """
        _hook = self._hooks[hook]
        _hook.connect(action)

    def __reverse(self):
        assert self.movable

        for motor in self.motors:
            motor.move_backwards()

    def __move_forwards(self):
        assert self.movable

        for motor in self.motors:
            motor.move_forwards()

    def __turn_left(self):
        assert self.turnable

        for motor in self.left_motors:
            motor.move_backwards()

        for motor in self.right_motors:
            motor.move_forwards()

    def __turn_right(self):
        assert self.turnable

        for motor in self.left_motors:
            motor.move_forwards()

        for motor in self.right_motors:
            motor.move_backwards()

    def __brake(self):
        for motor in self.motors:
            motor.stop()

    def reverse(self):
        """
        Handles callbacks then calls private __reverse() method
        """
        self._movement_change()
        _signal = self._hooks['ON_REVERSE_START']
        _signal.send()
        self.__reverse()
        self.movement = 'REVERSE'

    def move_forwards(self):
        """
        Handles callbacks then calls private __move_forwards() method
        """
        self._movement_change()
        _signal = self._hooks['ON_FORWARDS_START']
        _signal.send()
        self.__move_forwards()
        self.movement = 'FORWARDS'

    def turn_left(self):
        """
        Handles callbacks then calls private __turn_left() method
        """
        self._movement_change()
        _signal = self._hooks['ON_LEFT_START']
        _signal.send()
        self.__turn_left()
        self.movement = 'LEFT'

    def turn_right(self):
        """
        Handles callbacks then calls private __turn_right() method
        """
        self._movement_change()
        _signal = self._hooks['ON_RIGHT_START']
        _signal.send()
        self.__turn_right()
        self.movement = 'RIGHT'

    def brake(self):
        """
        Handles callbacks then calls private __brake() method
        """
        self._movement_change()
        _signal = self._hooks['ON_BRAKE']
        _signal.send()
        self.__brake()
        self.movement = None

    def get_sensors(self, position: str):
        """
        Returns a list of sensors at the given position

        :param position: the position on the robot to check - one of self.positions
        :rtype: list
        """
        assert position in self.positions
        return [s for s in self.sensors if s.position == position]

    @property
    def clear_ahead(self):
        """
        Tests whether the clear property of all sensors in the FRONT position is True

        :rtype: bool
        """
        sensors = self.get_sensors('FRONT')
        return all([s.clear for s in sensors])

    @property
    def clear_left(self):
        """
        Tests whether the clear property of all sensors in the LEFT or FRONT_LEFT positions is True
        Returns a numeric value instead of a boolean, giving a higher precedence to LEFT instead of FRONT_LEFT.
        This helps a robot to decide which path to take while evading obstacles

        :rtype: number
        """
        diagonal = self.get_sensors('FRONT_LEFT')
        side = self.get_sensors('LEFT')

        return (sum([s.clear for s in diagonal]) / 2) + sum([s.clear for s in side])

    @property
    def clear_right(self):
        """
        Tests whether the clear property of all sensors in the RIGHT or FRONT_RIGHT positions is True
        Returns a numeric value instead of a boolean, giving a higher precedence to RIGHT instead of FRONT_RIGHT.
        This helps a robot to decide which path to take while evading obstacles

        :rtype: number
        """
        diagonal = self.get_sensors('FRONT_RIGHT')
        side = self.get_sensors('RIGHT')

        return (sum([s.clear for s in diagonal]) / 2) + sum([s.clear for s in side])

    def _movement_change(self):
        """
        Called by all movement methods, e.g. move_forwards(), turn_right(), etc. In order to send ON_[[movement]]_END
        signal
        """
        if self.movement:
            _hook = self._hooks['ON_%s_END' % self.movement]
            _hook.send()
            self.movement = None

    def start(self):
        """
        Starts the robot moving by calling the start() method of self.movement_class (a threaded object)
        """
        if not self.motors:
            raise RobotException('Unable to start robot because no driving motors have been configured')

        self.movement_mode.start()

    def stop(self):
        """
        Stops the robot by calling the stop() method of self.movement_class
        """
        self.movement_mode.stop()
