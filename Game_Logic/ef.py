# economy factor
import random


class EF:
    """
    Economy factor
    """

    def __init__(self, variation):
        """
        Constructor
        """
        self._variation = variation
        self._ef_history = []
        self._cur_rate = 0
        self._random_rate_range = 0.025

    @property
    def ef_value(self):
        """
        Return current ef
        """
        return self._ef_history[-1]

    @property
    def variation(self):
        """
        Return the variation of this game
        """
        return self._variation

    def random_rate(self):
        """
        Generate a increase rate based on current economic factor
        """
        return random.random() * 2 * self._random_rate_range - self._random_rate_range + self._cur_rate

    def generate_ef(self):
        """
        Generate a new ef number
        """
        new_ef = random.random() * 2 * self._variation
        new_ef = new_ef - self._variation
        self._cur_rate = new_ef
        self._ef_history.append(new_ef)

    def getJSON(self):
        json_data = {
            "variation": self._variation,
            "cur_rate": self._cur_rate
        }
        return json_data
