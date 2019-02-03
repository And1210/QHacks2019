"""
QHacks 2019 project, simulating traffic with nodes to train AI
"""

# _____________________________________ Imports _________________________________

import distance_matrix
import googlemaps
import math
from openpyxl import workbook, load_workbook
from dat import Queue
from random import randint
import numpy as np
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
        self.cars = []

    def initCar(self, strNode):
        node = self.findNode(strNode)
        self.cars.append(Car(node))

    def numVertices(self):
        return self.size

    def getVertices(self):
        return self.vertices

    def addVertex(self, name):
        # prevents duplication from user
        if name not in self.vertices:
            # creates a dict value
            self.vertices[name] = Node(name, self.size)
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
            # Det distance between the nodes
            dist = distance_matrix.distance_matrix(client, (objA.y, objA.x), (objB.y, objB.x), mode="driving")
            distance = (((dist.get('rows'))[0].get('elements'))[0].get('distance')).get('value')

            # determines the direction that the node is linked
            dir = math.atan2(objA.y-objB.y, objA.x-objB.x)
            if (math.pi/4 > abs(dir)): dir = 1
            elif (3*math.pi/4 < abs(dir)): dir = 3
            elif dir > 0: dir = 0
            else:
                dir = 2

            # this portion adds the neighbours to each other, since it is unidirectional
            print("linking:", strA+',', strB)
            self.vertices[strA].addNeighbour(objB,(dir+2)%4, distance)
            self.vertices[strB].addNeighbour(objA, dir, distance)
            # return if successful
            return True
        return False

    def removeNeighbour(self, objA, objB):
        if objA in self.vertices and objB in self.vertices:
            # this portion removes he neighbours from each other, since it is unidirectional
            # returns if the operation succeeded
            return self.vertices[objA].removeNeighbour(objB) and self.vertices[objB].removeNeighbour(objA)
        return False


    def update(self, time, intensity):
        loss = 0
        traffic = np.zeros((self.getVertices(), self.getVertices()))
        waiting = np.zeros((self.getVertices(), self.getVertices()))
        for i in range(len(self.cars),0,-1):
            if (not self.cars[i].active):
                loss += self.cars[i].tTime/self.cars[i].tDist
                del(self.cars[i])
            else:
                if (self.cars[i].distance <= 0):
                    # TODO make this part exponential?
                    if self.cars[i].direction == self.cars[i].nextNode.getDirection():
                        self.cars[i].detNext()
                    else:
                        waiting[self.cars[i].currentNode.num][self.cars[i].nextNode.num] += 1
                        self.cars[i].distance = 0
                else:
                    self.cars[i].distance -= self.cars[i].velocity * self.cars[i].nextNodes.traffic[self.cars[i].direction]
                    traffic[self.cars[i].currentNode.num][self.cars[i].nextNode.num] += 1
        return [traffic, waiting, loss]





# acts as the node to display the country or team etc
class Node():
    def __init__(self, name, num):
        # a value holding the location of the place
        # if a user owns all nodes of a continent then they gain more troops
        self.nodeNum = num
        self.direction = True
        # how many troops they have
        # the position to display on the screen
        self.y, self.x = [float(i) for i in name.strip().split(',')]
        # when the data is reset
        self.neighbours = [None for i in range(4)]
        self.wait = Queue()
        self.act = Queue()
        self.distances = [0 for i in range(4)]
        self.traffic = [0 for i in range(4)]

    def addNeighbour(self, obj, dir, distance):
        # adds a new neighbour to the vertex with a given distance
        if self.neighbours[dir] == None:
            self.neighbours[dir] = obj
            self.distances[dir] = distance
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
        return [self.y,self.x]

    def getDirection(self):
        return self.direction

    def changeDirection(self):
        self.direction = not self.direction

class Car():
    def __init__(self, obj):
        self.currentNode = obj
        options = []
        for i in range(4):
            if self.currentNode.getNeighbours()[i] == None:
                options.append((i+2)%4)
        self.direction = options[randint(0,len(options))-1]
        self.nextNode = self.currentNode.getNeighbours()[self.direction]
        self.time = 0
        self.distance = 0
        self.velocity = 0
        self.tTime = 0
        self.tDist = 0
        self.active = True
        self.waiting = False

    def detNext(self):
        choice = randint(0,100)
        # turn car right
        if choice < 12:
            self.direction = (self.direction + 1) % 4
        # turn car left
        if choice < 24:
            self.direction = (self.direction - 1) % 4
        self.nextNode = self.nextNode.getNeighbours[self.direction]
        if nextNode == None:
            self.active = False
        else:
            self.distance = self.currentNode.distances[self.direction]
            self.tDist += self.currentNode.distances[self.direction]
            self.time= self.currentNode.distances[self.direction]
            self.tTime = self.currentNode.distances[self.direction]





# Create and link the graph
toronto = Graph()


letters = "ABCDEF"
for i in range(0,6):
    for n in range(1,6):
        print("{}{}".format(str(letters[i]),n), wb2["Sheet1"]["{}{}".format(str(letters[i]), n)].value)
        toronto.addVertex(wb2["Sheet1"]["{}{}".format(str(letters[i]),n)].value)

for i in range (0,6):
    for n in range(1,6):
        if i < 5:
            toronto.addNeighbour(wb2["Sheet1"]["{}{}".format(letters[i], n)].value,
                                 wb2["Sheet1"]["{}{}".format(letters[i + 1], n)].value)
        if n < 5:
            toronto.addNeighbour(wb2["Sheet1"]["{}{}".format(letters[i], n)].value,
                                 wb2["Sheet1"]["{}{}".format(letters[i], n + 1)].value)

#TODO, save into a pickle for faster startup

toronto.initCar(wb2["Sheet1"]["{}{}".format(letters[0], 1)].value)

