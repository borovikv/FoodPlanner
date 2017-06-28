

class r:
    def __init__(self, start):
        self.start = start

    def to(self, i, step=1):
        return range(self.start, i + 1, step)


print(list(r(1).to(5)))