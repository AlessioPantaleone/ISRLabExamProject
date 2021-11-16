from typing import Dict


def __init__(self, sensors, actuators):
    self._sensors = sensors
    self._actuators = actuators


def honk(honkLength):
    ...
    # Command to honk for given time length


def get_perceptions(self) -> Dict:
    """
    Produces perceptions built from sensors
    """
    out = {}
    ...  # Build perceptions
    ...  # Send perceptions to redis custom list
    return out
