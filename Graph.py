import sys

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
    def addEdge(self, v1, v2, w):
        if v1 == v2:
            print("Same vertex %d and %d" % (v1, v2))
        self.adjMatrix[v1][v2] = w
        self.adjMatrix[v2][v1] = w
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
    
    # a aux function to check if there is a path linking last visited vertex to v and v was not visited yet
    def checkVertex(self, v, pos): 
        # check if there is a path linking last visited vertex to v
        if self.adjMatrix[ self.path[pos-1] ][v] == 0: 
            return False
  
        # check if v was not visited yet
        for vertex in self.path: 
            if vertex == v: 
                return False
  
        return True
  
    #  recursive aux function to find hamiltonian cycle path 
    def hamCycleAux(self, pos): 
  
        # base case: all vertices are included in the path 
        if pos == self.size: 
            # must have a path from the first vertex to last one 
            if self.adjMatrix[ self.path[pos-1] ][ self.path[0] ] > 0: 
                # update result matrix
                self.result[ self.path[pos-1] ][ self.path[0] ] = self.adjMatrix[ self.path[pos-1] ][ self.path[0] ]
                self.result[ self.path[0] ][ self.path[pos-1] ] = self.adjMatrix[ self.path[0] ][ self.path[pos-1] ]
                return True
            else: 
                return False
  
        # try each vertex as a candidate for next visit
        for v in range(1,self.size): 
  
            # check if there is a path linking last visited vertex to v and v was not visited yet
            if self.checkVertex(v, pos) == True: 
                
                # add v to path as a candidate
                self.path[pos] = v 
  
                # if v lead to a solution, add the edge to result matrix
                if self.hamCycleAux(pos+1) == True: 
                    self.result[ self.path[pos-1] ][ v ] = self.adjMatrix[ self.path[pos-1] ][ v ]
                    self.result[ v ][ self.path[pos-1] ] = self.adjMatrix[ v ][ self.path[pos-1] ]
                    return True
  
                # else remove v at the path
                self.path[pos] = -1
                # self.result[ self.path[pos-1] ][ v ] = 0
                # self.result[ v ][ self.path[pos-1] ] = 0
        return False

    def dfs(self, v):
        visited =[False]*(self.size)
        self.path = []

        # initialize matrix of result path
        self.result = [[0 for j in range(self.size)] for i in range(self.size)]

        self.__dfsAux(v, visited)

        return self.path
    
    def isEulerian(self): 
        # initialize matrix of result path
        self.path = []
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

    def hamCycle(self): 
        self.result = [[0 for j in range(self.size)] for i in range(self.size)]
        self.path = [-1] * self.size

        #add initial vertex to path array
        self.path[0] = 0
  
        if self.hamCycleAux(1) == False: 
            print("false")
            return False
  
        self.toString() 
        return True

    # aux function to find the vertex with minimum distance value,
    def minDistance(self, distance, mstSet): 
  
        # initilaize min value as inf
        min = sys.maxsize
  
        for v in range(self.size): 
            if distance[v] < min and mstSet[v] == False: 
                min = distance[v] 
                min_index = v 
  
        return min_index 
  
    def primMST(self): 
        # initialize matrix of result path
        self.result = [[0 for j in range(self.size)] for i in range(self.size)]
        # values used to pick minimum weight edge in cut 
        distance = [sys.maxsize] * self.size
        # array to store constructed MST  
        self.path = [None] * self.size 
        # make key 0 so that this vertex is picked as first vertex 
        distance[0] = 0 
        mstSet = [False] * self.size
  
        self.path[0] = -1
  
        for i in range(self.size): 
  
            # pick the minimum distance vertex from vertices not processed yet
            u = self.minDistance(distance, mstSet) 
  
            # mark the minimum distance vertex as visited
            mstSet[u] = True

            # update dist value of the adjacent vertices  
            # of the picked vertex only if the current  
            # distance is greater than new distance and 
            # the vertex in not in the shotest path tree 
            for v in range(self.size): 
                # graph[u][v] is non zero only for adjacent vertices of m 
                # mstSet[v] is false for vertices not yet included in MST 
                # Update the key only if graph[u][v] is smaller than key[v] 
                if self.adjMatrix[u][v] > 0 and mstSet[v] == False and distance[v] > self.adjMatrix[u][v]: 
                        distance[v] = self.adjMatrix[u][v] 
                        self.path[v] = u 
        for u in range(len(self.path)):
            self.result[ u ][ self.path[u] ] = self.adjMatrix[ u ][ self.path[u] ]
            self.result[ self.path[u] ][ u ] = self.adjMatrix[ self.path[u] ][ u ]

        print(self.path)
g = Graph(0)
g.addVertex()
g.addVertex()
g.addVertex()
g.addVertex()
# g.addVertex()
g.addEdge(0,1, 9)
g.addEdge(0,2, 1)
g.addEdge(1,2, 3)
g.addEdge(2,3, 2)
g.primMST()
# g.addEdge(1,4, 1)
# g.addEdge(2,4, 1)
# g.addEdge(3,4, 1)
# g.hamCycle()
# print()
# g.toString()
# print(g.isEulerian())
# g.toString()
# print(g.isEulerian())
# print(g.dfs(0))
g.toString()

