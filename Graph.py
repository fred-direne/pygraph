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
        for row in self.result:
            print(row),
            print

    def __dfsAux(self,v,visited): 
        visited[v]= True
        if len(self.path) > 0:
            v_from = self.path[-1]
            self.result[v_from][v] = self.adjMatrix[v_from][v]
            self.result[v][v_from] = self.adjMatrix[v][v_from]
        self.path.append(v)

        for i in range(self.size): 
            if visited[i]==False and self.adjMatrix[v][i] > 0: 
                self.__dfsAux(i,visited)

    def __isConnected(self): 
   
        visited =[False]*(self.size)

        for i in range(self.size): 
            if sum(self.adjMatrix[i]) > 1: 
                break
  
        if i == self.size-1: 
            return True
  
        self.__dfsAux(0,visited) 

        for i in range(self.size): 
            if visited[i]==False and sum(self.adjMatrix[i]) > 0: 
                return False
          
        return True

    def dfs(self, v):
        visited =[False]*(self.size)
        self.path = []

        # initialize matrix of result path
        self.result = [[0 for j in range(self.size)] for i in range(self.size)]

        self.__dfsAux(v, visited)

        return self.path
    
    def isEulerian(self): 
        # initialize matrix of result path
        self.result = [[0 for j in range(self.size)] for i in range(self.size)]

        if self.__isConnected() == False: 
            return 0
        else: 
            odd = 0
            for i in range(self.size): 
                aux = self.size - self.adjMatrix[i].count(0)
                if (aux % 2) != 0: 
                    odd +=1
                    
            if odd == 0: 
                return 2
            elif odd == 2: 
                return 1
            elif odd > 2: 
                return 0


# g = Graph(0)
# g.addVertex()
# g.addVertex()
# g.addVertex()
# g.addEdge(0,1)
# # g.addEdge(1,2)
# # g.addEdge(2,0)
# # g.toString()
# # print(g.isEulerian())
# g.addVertex()
# g.addEdge(2,3)
# # g.toString()
# # print(g.isEulerian())
# g.addVertex()
# g.addEdge(1,4)
# g.addEdge(2,4)
# print()
# print(g.dfs(0))
# g.toString()

