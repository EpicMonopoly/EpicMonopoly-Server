# economy factor
import random


class EF:
    """
    Economy factor
    """

    def ___init___(self, variation):
        """
        Constructor
        """
        self._variation = variation
        self._ef_history = []

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
        pass

    def generate_ef(self):
        """
        Generate a new ef number
        """
        new_ef = random.random * 2 * self._variation
        new_ef = new_ef - self._variation
        self._ef_history.append(new_ef)
