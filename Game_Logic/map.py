import random

class Map(object):

    def __init__(self, street_list, two_block_street, three_block_street):
        self._street_list = street_list
        self._two_block_street = two_block_street
        self._three_block_street = three_block_street
        self._chest = CardPile.__init__()
        self._oppertunity = CardPile.__init__()

    def new_map(self):
        pass

    def change_street_order(self):
        num_three_block_street = len(self._three_block_street)
        random_num = random.random()
        if(random_num < 0.5):
            street_a = self._two_block_street[0]
            street_b = self._two_block_street[1]
            for index in range(2):
                block = street_a[index]
                temp = block.position
                block.position(street_b[index].position)
                street_b[index].position(temp)
            street_a.resort()
            street_b.resott()
        for i in range(3):
            int_a = random.randint(num_three_block_street)
            int_b = random.randint(num_three_block_street)
            while(int_a == int_b):
                int_b = random.randint(num_three_block_street)
            street_a = self._three_block_street[int_a]
            street_b = self._three_block_street[int_b]
            self._change_two_street(street_a, street_b)
            street_a.resort()
            street_b.resort()

    def _change_two_street(self, street_a, street_b):
        for index in range(3):
            block = street_a[index]
            temp = block.position
            block.position(street_b[index].position)
            street_b[index].position(temp)







