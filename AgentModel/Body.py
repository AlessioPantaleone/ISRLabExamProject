"""
This is the body of the agent
"""
from typing import Dict, List


class Body:

    def __init__(self):
        self._sensors = []
        self._actuators = []

    def get_perceptions(self) -> Dict:
        """
        Produces perceptions built from sensors
        """
        out = {}
        ...  # Build perceptions
        return out

    def set_stimuli(self, stimuli: List):
        """
        Set stimuli
        :param stimuli : array of values from world or simulator
        """
        self._sensors = stimuli

    def calibrate(self, sensor, data):
        """
        calibrate one sensor
        :param sensor : key or index of the sensor
        :param data : calibration data
        """
        ...  # Calibrate sensor

    def calibrate(self, actuator, data):
        """
        calibrate one actuator
        :param actuator : key or index of the actuator
        :param data : calibration data
        """
        ...  # Calibrate actuator
