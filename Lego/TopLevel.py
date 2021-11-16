"""
This is a generic agent level
"""
from typing import Dict


def __init__(self, sensors, actuators):
    self._sensors = sensors
    self._actuators = actuators

def act(self):
    """
    ??? TODO
    """

def get_perceptions(self) -> Dict:
    """
    Produces perceptions built from sensors
    """
    out = {}
    ...  # Build perceptions
    return out