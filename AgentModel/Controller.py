"""
This is the controller of the agent
"""
from typing import List


class Controller:

    def __init__(self):
        self._internal_state = ...  # TODO internal state
        self._world_map = ...  # TODO world map

    def act(self):
        """
        ??? TODO
        """

    def save_history(self, action, stimuli: List):
        """
        Save history of the agent up to current time
        :param action : TODO
        :param stimuli : array of values from the body
        """

    def load_prior_knowledge(self, file):
        """
        load knowledge into the agent
        :param file : file that contains prior knowledge for the agent
        """
        ...  # Calibrate sensor

    def load_history(self, time, action, file):
        """
        calibrate one sensor
        :param time : TODO
        :param action : TODO
        :param file : history data
        """

    def load_abilities(self, file):
        """
        load agent's abilities
        :param file : file that contains agent's abilities
        """