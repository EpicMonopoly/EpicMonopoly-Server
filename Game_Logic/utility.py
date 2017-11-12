from property import Property

class Utility(Property):
    """
    Class Utility
    """
    def __init__(self):
        '''
        Call superclass construct method
        '''
        super().__init__()

    def getPayment(self, utility_num, dice_result):
        if utility_num == 1:
            return dice_result * 4
        elif utility_num == 2:
            return  dice_result * 10
        else:
            # Should not be here
            return 0

    def display(self):
        pass
