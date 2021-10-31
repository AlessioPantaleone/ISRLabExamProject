"""
This is the world simulator for environments and agents
"""
from typing import List

from AgentModel import Environment
from AgentModel import Agent


class WorldSimulator:

    def __init__(self):
        self._my_environments = [Environment]
        self._my_agents = [Agent]

    def step(self, time):
        """
        makes the simulator step ahead for a fixed time interval
        :param time  : TODO ???
        """

    def external_event(self):
        """
        TODO ???
        """
