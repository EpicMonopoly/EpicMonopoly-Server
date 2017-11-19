import property


class Station(property.Property):
    """
    Class Station
    """

    def __init__(self, name, position, uid, estate_value, status, street_id):
        """
        Call for superclass construct
        """
        super().__init__()
        super()._name = name
        super()._position = position
        super()._uid = uid
        super()._estate_value = estate_value
        super()._status = status
        super()._street_id = street_id

    def payment(self, station_num, dice_result):
        """
        Return the payment if a player enter this block
        :param station_num: number of station
        :param dice_result: dice result
        :return: amount of payment

        """
        value = self._estate_value
        if station_num == 1:
            return (1/8) * value
        elif station_num == 2:
            return (1/4) * value
        elif station_num == 3:
            return (1/2) * value
        elif station_num == 4:
            return value
        else:
            # Should not be here
            return 0

    # TODO: implement display
    def display(self):
        """
        Display description
        :return:
        """
        pass
