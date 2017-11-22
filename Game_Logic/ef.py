# economy factor 
import random
import datetime


class EF:
    """
    Economy factor
    """
    def ___init___(self):
        """
        Constructor
        """
        seed = datetime.datetime.now()
        random.seed(seed)
        self._seed = random.randint(0, 999999)
    
    @property
    def ef_value(self):
        pass

    
    
