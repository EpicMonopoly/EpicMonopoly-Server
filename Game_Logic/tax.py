import block
import operation


class Tax(block.Block):
    """Class Tax

    Parameters
    ----------
    block.Block: superclass 

    """
    def __init__(self, name, block_id, position, description, rate):
        """constructor

        Parameters
        ----------
        self: class itself
        name: name of tax
        block_id: block id of tax
        position: position of tax
        description: description of tax
        rate: rate

        """
        super().__init__(name, block_id, position)
        self._description = description
        self._rate = rate

    @property
    def rate(self):
        """rate

        Parameters
        ----------
        self: class itself

        Returns
        -------
        rate: rate
        """
        return self._rate

    @rate.setter
    def rate(self, rate):
        """rate setter

        Parameters
        ----------
        self: class itself
        rate: new rate

        Returns
        -------
        rate: newly set rate
        """
        self._rate = rate

    def display(self, gamer, data, dice_result):
        pass

    def change_value(self, new_rate):
        self._rate = int(self._rate * (1 + new_rate))

    def getJSON(self):
        """
        get data in json format
        """
        json_data = {
            "name": self._name,
            "block_id": self._block_id,
            "position": self._position,
            "rete": self._rate
        }
        return json_data


class Income_Tax(Tax):
    """Class Income_Tax

    Parameters
    ----------
    Tax: superclass

    """
    def __init__(self, name, block_id, position, description, rate):
        """constructor

        Parameters
        ----------
        self: class itself
        name: name of tax
        block_id: block id of tax
        position: position of tax
        description: description of tax
        rate: rate

        """
        super().__init__(name, block_id, position, description, rate)

    def display(self, gamer, data, dice_result):
        """display message

        Parameters
        ----------
        self: class itself
        gamer: gamer who invloved in
        data: data dict
        dice_result: result of dice

        """
        bank = data['epic_bank']
        payment = gamer.cash * self.rate
        operation.pay(gamer, bank, payment, data)
        data["msg"].push2all(operation.gen_record_json("%s pay %d for tax" % (gamer.name, payment)))


class Super_Tax(Tax):
    """Class Super_Tax

    Parameters
    ----------
    Tax: superclass

    """
    def __init__(self, name, block_id, position, description, rate):
        """constructor

        Parameters
        ----------
        self: class itself
        name: name of tax
        block_id: block id of tax
        position: position of tax
        description: description of tax
        rate: rate

        """
        super().__init__(name, block_id, position, description, rate)

    def display(self, gamer, data, dice_result):
        """display message

        Parameters
        ----------
        self: class itself
        gamer: gamer who invloved in
        data: data dict
        dice_result: result of dice

        """
        bank = data['epic_bank']
        payment = gamer.calculate_asset_value() * self.rate
        operation.pay(gamer, bank, payment, data)
        data["msg"].push2all(operation.gen_record_json("%s pay %d for tax" % (gamer.name, payment)))
