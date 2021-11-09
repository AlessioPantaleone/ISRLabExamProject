"""
This is pioneer agent
"""
import Body
import Controller
import Abstraction_Level

from typing import Dict, List


class Agent:

    def __init__(self, B: Body, C=Controller):
        self._up_time = 0
        self._my_physical_body = B
        self._my_controller = C
        self._my_levels = [Abstraction_Level]
        self._my_abstraction_levels = 2

    def set_current_goal(self, goal):
        """
        ???
        :param goal : current goal to be set for the agent
        """
