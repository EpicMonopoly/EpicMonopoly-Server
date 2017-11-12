class a:
    def __init__(self, a1):
        self.a1 = a1

class b(a):
    def __init__(self, b1):
        super().__init__(b1)

c = b(12)
print(c.a1)
