from abc import abstractmethod
import block


class Asset(block.Block):
    """Class Asset

    Parameters
    ----------
    block.Block: superclass 

    Returns
    -------

    """

    def __init__(self, name, block_id, position, uid, estate_value, status, mortgage_rate=0.5):
        """constructor

        Parameters
        ----------
        self: class itself
        name: asset name 
        block_id: block id of asset
        position: position of asset
        uid: owner id of asset
        estate_value: estate value of asset
        status: status of asset
        mortgage_rate: mortgage rate, 0.5 by default 

        """
        super().__init__(name, block_id, position)
        self._uid = uid
        self._estate_value = estate_value
        self._status = status
        self.mortgage_rate = mortgage_rate
        self.enter_log = {}

    @property
    def owner(self):
        """owner

        Parameters
        ----------
        self: class itself

        Returns
        -------
        uid: user id
        """
        return self._uid

    def clear_log(self):
        """
        Clear entering log
        """
        self.enter_log = {}

    @owner.setter
    def owner(self, uid):
        """setter of owner id

        Parameters
        ----------
        self: class itself
        uid: owner id

        """
        self._uid = uid

    @property
    def value(self):
        """estate value

        Parameters
        ----------
        self: class itself

        Returns
        -------
        estate_value: estate value
        """
        return self._estate_value

    @property
    def status(self):
        """status

        Parameters
        ----------
        self: class itself

        Returns
        -------
        status: status of asset
        """
        return self._status

    @status.setter
    def status(self, status):
        """

        Parameters
        ----------
        self: class itself
        status: changed status

        """
        self._status = status

    @property
    def mortgage_value(self):
        """mortagage value of asset

        Parameters
        ----------
        self: class itself

        Returns
        -------
        mortgage_value: mortgage value of asset
        """
        return self._estate_value * self.mortgage_rate

    @abstractmethod
    def change_value(self, rate):
        pass

    @property
    def block_id(self):
        return self._block_id

    def payment(self):
        """payment

        Parameters
        ----------
        self: class itself

        Returns
        -------
        estate_value: estate value for buying

        """
        return self._estate_value

    @abstractmethod
    def display(self, gamer, data_dict, dice_result):
        pass

    @abstractmethod
    def getJSON(self):
        pass
        # json_data = {
        #     "name": self._name,
        #     "block_id": self._block_id,
        #     "position": self._position,
        #     "uid": self._uid,
        #     "estate_value": self._estate_value,
        #     "status": self._status
        # }
        # return json_data
