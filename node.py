"""
QHacks 2019 project, simulating traffic with nodes to train AI
"""

# _____________________________________ Imports _________________________________

import distance_matrix
import googlemaps
import math
from openpyxl import workbook, load_workbook
# _____________________________________ Google API ______________________________

client = googlemaps.Client(key='AIzaSyCgY2Z9_bBdriMaGe_2hPLBjUEZacnEHfQ')

# Time between points
# (((dist.get('rows'))[0].get('elements'))[0].get('duration')).get('value')

# _____________________________________ XLS _____________________________________

wb2 = load_workbook('nodes.xlsx')


# _____________________________________ Classes _________________________________


# creates a graph to allow linking between the different classes
class Graph():
    def __init__(self):
        self.size = 0
        self.vertices = {}
        self.neighbours = 0

    def numVertices(self):
        return self.size

    def getVertices(self):
        return self.vertices

    def addVertex(self, name):
        # prevents duplication from user
        if name not in self.vertices:
            # creates a dict value
            self.vertices[name] = Node(name)
            self.size += 1
            return True
        return False

    def findNode(self, name):
        # looks in the dict if the value exists
        if name in self.vertices:
            # returns the class to the caller
            return self.vertices[name]
        return None

    def addNeighbour(self, strA, strB):
        objA = self.findNode(strA)
        objB = self.findNode(strB)
        # error check to make sure the data can be accessed
        if strA in self.vertices and strB in self.vertices:
            dist = distance_matrix.distance_matrix(client, (objA.x, objA.y), (objB.x, objB.y), mode="driving")
            distance = (((dist.get('rows'))[0].get('elements'))[0].get('distance')).get('value')
            # direction is fine
            dir = math.atan2(objA.x-objB.x,objA.y-objB.y)
            if (math.pi/4 > abs(dir)): dir = 1
            elif (3*math.pi/4 < abs(dir)): dir = 3
            elif dir > 0: dir = 0
            else: dir = 2
            # this portion adds the neighbours to each other, since it is unidirectional
            self.vertices[strA].addNeighbour(objB,(dir+2)%4, distance)
            self.vertices[strB].addNeighbour(objA,dir,distance)
            # return if successful
            return True
        return False

    def removeNeighbour(self, objA, objB):
        if objA in self.vertices and objB in self.vertices:
            # this portion removes he neighbours from each other, since it is unidirectional
            # returns if the operation succeeded
            return self.vertices[objA].removeNeighbour(objB) and self.vertices[objB].removeNeighbour(objA)
        return False


# acts as the node to display the country or team etc
class Node():
    def __init__(self, name):
        # a value holding the location of the place
        # if a user owns all nodes of a continent then they gain more troops
        self.direction = True
        # how many troops they have
        # the position to display on the screen
        self.x, self.y = [float(i) for i in name.strip().split(',')]
        # when the data is reset
        self.neighbours = {}
        self.cars = {}
        self.num = 0

    def addNeighbour(self, obj, dir, distance):
        # adds a new neigbour to the vertex with a given distance
        if dir not in self.neighbours:
            self.neighbours[dir] = [obj, distance]
            self.cars[dir] = 0
            self.num += 1
            return True
        return False

    def removeNeighbour(self, dir):
        # deletes a neighbour from the vertex
        if dir in self.neighbours:
            del self.neighbours[dir]
            del self.cars[dir]
            self.num -= 1
            return True
        return False

    def getNeighbours(self):
        return self.neighbours

    def getCoord(self):
        return [self.x,self.y]

    def getDirection(self):
        return self.direction

    def changeDirection(self):
        self.direction = not self.direction


toronto = Graph()


letters = "ABCD"
for i in range(0,4):
    for n in range(1,5):
        print(i,n)
        print("{}{}".format(str(letters[i]),n), wb2["Sheet1"]["{}{}".format(str(letters[i]), n)].value)
        toronto.addVertex(wb2["Sheet1"]["{}{}".format(str(letters[i]),n)].value)

for i in range (0,4):
    for n in range(1,5):
        if i > 1:
            print(wb2["Sheet1"]["{}{}".format(letters[i], n)].value)
            toronto.addNeighbour(wb2["Sheet1"]["{}{}".format(letters[i], n)].value,
                                 wb2["Sheet1"]["{}{}".format(letters[i - 1], n)].value)
        if i < 4:
            print(wb2["Sheet1"]["{}{}".format(letters[i], n)].value)
            toronto.addNeighbour(wb2["Sheet1"]["{}{}".format(letters[i], n)].value,
                                 wb2["Sheet1"]["{}{}".format(letters[i + 1], n)].value)
        if n > 1:
            print(wb2["Sheet1"]["{}{}".format(letters[i], n)].value)
            toronto.addNeighbour(wb2["Sheet1"]["{}{}".format(letters[i], n)].value,
                                 wb2["Sheet1"]["{}{}".format(letters[i], n - 1)].value)
        if n < 4:
            print(wb2["Sheet1"]["{}{}".format(letters[i], n)].value)
            toronto.addNeighbour(wb2["Sheet1"]["{}{}".format(letters[i], n)].value,
                                 wb2["Sheet1"]["{}{}".format(letters[i], n - 1)].value)

print(toronto.numVertices())
print(toronto.getVertices())