class Graph(object):
    def __init__(self, size):
        self.adjMatrix = []
        # for i in range(size):
        #     self.adjMatrix.append([0 for i in range(size)])
        self.size = size
    def addVertex(self):
        for v in self.adjMatrix:
            v.append(0)
        self.size += 1
        self.adjMatrix.append([0 for i in range(self.size)])
    def removeVertex(self, v):
        self.adjMatrix.pop(v)
        for row in self.adjMatrix:
            row.pop(v)
        self.size -= 1
    def addEdge(self, v1, v2):
        if v1 == v2:
            print("Same vertex %d and %d" % (v1, v2))
        self.adjMatrix[v1][v2] = 1
        self.adjMatrix[v2][v1] = 1
    def removeEdge(self, v1, v2):
        if self.adjMatrix[v1][v2] == 0:
            print("No edge between %d and %d" % (v1, v2))
            return
        self.adjMatrix[v1][v2] = 0
        self.adjMatrix[v2][v1] = 0
    def containsEdge(self, v1, v2):
        return True if self.adjMatrix[v1][v2] > 0 else False
    def __len__(self):
        return self.size
        
    def toString(self):
        for row in self.adjMatrix:
            print(row),
            print

g = Graph(0)
g.addVertex()
g.addVertex()
g.addVertex()
g.addVertex()
g.addEdge(0,1)
g.addEdge(1,1)
g.addEdge(2,1)
g.addEdge(3,1)
g.toString()
g.removeVertex(1)
print()

g.toString()