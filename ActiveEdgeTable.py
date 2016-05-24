from Edge import Edge


class ActiveEdgeTable:

    def __init__(self):
        self.edges = []

    def add(self, x1, y1, x2, y2):
        self.edges.append(Edge(x1, y1, x2, y2))

    def update(self):
        for item in self.edges:
            item.x = item.x + item.m

    def removeEdge(self, x1, y1, x2, y2):
        self.edges[:] = [tup for tup in self.edges if tup.p1 != (x1, y1) or tup.p2 != (x2, y2)]
        self.edges[:] = [tup for tup in self.edges if tup.p2 != (x1, y1) or tup.p1 != (x2, y2)]

    def sort(self):
        self.edges.sort(key= lambda tup:tup.x)

    def remove(self, y):
        self.edges[:] = [tup for tup in self.edges if tup.ymin != y]