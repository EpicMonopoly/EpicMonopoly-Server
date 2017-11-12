from property import Property

class Station(Property):
    '''
    Class Station
    '''

    def __init__(self):
        '''
        Call for superclass construct
        '''
        super().__init__()

    def getPayment(self, station_num, dice_result):
        '''
        Return the payment if a player enter this block
        :param station_num:
        :param dice_result:
        :return:
        '''
        value = self.value
        if station_num == 1:
            return (1/8) * value
        elif station_num == 2:
            return  (1/4) * value
        elif station_num == 3:
            return  (1/2) * value
        elif station_num == 4:
            return  value
        else:
            # Should not be here
            return 0

    def display(self):
        pass