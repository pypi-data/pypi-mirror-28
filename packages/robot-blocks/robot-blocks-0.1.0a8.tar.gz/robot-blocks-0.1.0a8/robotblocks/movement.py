import threading
import time
import random


class Obstruction(Exception):
    pass


class RobotMovement(threading.Thread):
    """
    Lowest level robot movement object
    """
    def __init__(self, robot, *args, **kwargs):
        self.robot = robot
        super(RobotMovement, self).__init__(*args, **kwargs)


class ObstacleAvoidance(RobotMovement):
    """
    Movement class for an autonomous, obstacle avoidance robot
    """
    _running = True
    max_evasion_time = 5

    def __init__(self, robot, *args, **kwargs):
        """
        Updates the class to tell the robot to brake on receiving an ON_OBSTACLE_[[position]] signal
        """
        super(ObstacleAvoidance, self).__init__(robot, *args, **kwargs)

        for sensor in self.robot.sensors:
            if 'FRONT' in sensor.position:
                self.robot.add_callback('ON_OBSTACLE_%s' % sensor.position, self.robot.brake)

    @property
    def clear_ahead(self):
        return self.robot.clear_ahead

    @property
    def clear_left(self):
        return self.robot.clear_left

    @property
    def clear_right(self):
        return self.robot.clear_right

    def pick_direction(self):
        """
        Checks obstacle sensors to see if there is a clear path on either side to turn to. If Robot cannot establish
        that one side is clearer than the other, a direction is picked at random

        :return: `self.robot.turn_left` or `self.robot.turn_right`
        """
        if self.clear_left == self.clear_right:
            turn = self.pick_random_direction()

        elif self.clear_left > self.clear_right:
            turn = self.robot.turn_left

        else:
            turn = self.robot.turn_right

        return turn

    def pick_random_direction(self):
        """
        Chooses a random direction in which to turn while evading if robot cannot establish a preferable direction in
        which to turn
        """
        return random.choice([self.robot.turn_left, self.robot.turn_right])

    def evade(self):
        """
        This method is called if an obstacle is detected - attempts to move the robot away from the obstacle
        """
        self.robot.brake()

        turn = self.pick_direction()

        timer = 0

        while not self.clear_ahead:
            turn()
            time.sleep(0.1)
            timer += 0.1

            if timer > self.max_evasion_time:
                raise Obstruction('Unable to find a clear path to proceed')

    def run(self):
        while self._running:
            if self.robot.clear_ahead:
                self.robot.move_forwards()

            self.evade()

    def stop(self):
        self._running = False
        self.robot.brake()
        self.join()
