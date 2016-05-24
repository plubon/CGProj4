
class Edge:

    def __init__(self, x1, y1, x2, y2):
        self.p1 = (x1, y1)
        self.p2 = (x2, y2)
        self.ymin = min(y1, y2)
        self.x = None
        if y1 < y2:
            self.x = x2
        else:
            self.x = x1
        self.m = (x2 - x1)/float(abs(y2 - y1))