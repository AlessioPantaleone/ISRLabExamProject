"""
This is the environment simulated from the world simulator
"""
from typing import List


class Environment:

    def __init__(self):
        self._map = ...  # TODO
        self._state = ...  # TODO

    def set_state(self, state):
        """
        Set current state for the environment
        :param state  : TODO ???
        """

    def events_memory(self, time, state):
        """
        ???
        :param time  : TODO ???
        :param state : TODO ???
        """

    def get_action(self, agent, action):
        """
        ???
        :param  : TODO ???
        :param  : TODO ???
        """

    def give_stimuli(self, agent, stimuli):
        """
        ???
        :param  : TODO ???
        :param  : TODO ???
        """

    def give_reward(self, agent, reward):
        """
        ???
        :param  : TODO ???
        :param  : TODO ???
        """

