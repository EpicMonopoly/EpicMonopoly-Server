import property


class Utility(property.Property):
    """
    Class Utility
    """
    def __init__(self, name, position, uid, estate_value, status, street_id):
        """
        Call superclass construct method
        """
        super().__init__(name, position)
        super()._uid = uid
        super()._estate_value = estate_value
        super()._status = status
        super()._street_id = street_id

    def payment(self, utility_num, dice_result):
        if utility_num == 1:
            return dice_result * 4
        elif utility_num == 2:
            return dice_result * 10
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
