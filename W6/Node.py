class Node:
    def __init__(self, min, max, mean, var, sd, count):
        self.father = None
        self.min = min
        self.max = max
        self.mean = mean
        self.var = var
        self.sd = sd
        self.count = count
        self.children = []