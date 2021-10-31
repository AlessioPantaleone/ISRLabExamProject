"""
This is the agent
"""
from AgentModel import Body
from AgentModel import Controller

from typing import Dict, List


class Agent:

    def __init__(self):
        self._my_body = Body
        self._my_controller = Controller
        self._up_time = 0

    def set_current_goal(self, goal):
        """
        ???
        :param goal : current goal to be set for the agent
        """