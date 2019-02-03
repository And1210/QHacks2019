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
longitudes = [43.666356, 43.664932, 43.665730, 43.666264, 43.667071, 43.668180, 43.660837, 43.661403, 43.661898, 43.662422, 43.663183, 43.664295, 43.658455, 43.659094, 43.659910, 43.660467, 43.661243, 43.662322, 43.655775, 43.656292, 43.656518, 43.657050, 43.658301, 43.659381, 43.651870, 43.652448, 43.653161, 43.653713, 43.654510, 43.655605]
latitudes = [-79.387163, -79.384514, -79.380942, -79.378328, -79.374680, -79.369546, -79.385846, -79.383101, -79.379297, -79.376687, -79.373071, -79.367982, -79.384852, -79.382114, -79.378477, -79.375801, -79.372213, -79.367185, -79.383666, -79.380896, -79.377131, -79.374553, -79.370947, -79.365975, -79.381810, -79.379307, -79.375726, -79.373216, -79.369440, -79.364435]
edges = ['43.668180, -79.369546',
'43.664295, -79.367982',
'43.662322, -79.367185',
'43.659381, -79.365975',
'43.655605, -79.364435',
'43.664356, -79.387163',
'43.660837, -79.385846',
'43.658455, -79.384852',
'43.655775, -79.383666',
'43.651870, -79.381810',
'43.664932, -79.384514',
'43.665730, -79.380942',
'43.666264, -79.378328',
'43.667071, -79.374680',
'43.652448, -79.379307',
'43.653161, -79.375726',
'43.653713, -79.373216',
'43.654510, -79.369440'];


# _____________________________________ Classes _________________________________

letters = "ABCDEF"
    
# creates a graph to allow linking between the different classes
class Graph():
    def __init__(self):
        self.size = 0
        self.vertices = {}
        self.neighbours = 0
        self.cars = []
        self.edges = 0

    def initCar(self, strNode):
        node = self.findNode(strNode)
        if node != None:
            self.cars.append(Car(node))

    def numVertices(self):
        return self.size

    def getVertices(self):
        return self.vertices

    def addVertex(self, n0, n1):
        # prevents duplication from user
        name = str(n0)+', '+str(n1)
        if name not in self.vertices:
            # creates a dict value
            self.vertices[name] = Node(n0, n1, self.size)
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
            time = (((dist.get('rows'))[0].get('elements'))[0].get('duration')).get('value')
            # determines the direction that the node is linked
            dir = math.atan2(objA.y-objB.y, objA.x-objB.x)
            if (math.pi/4 > abs(dir)): dir = 1
            elif (3*math.pi/4 < abs(dir)): dir = 3
            elif dir > 0: dir = 0
            else:
                dir = 2

            self.edges += 1
            # this portion adds the neighbours to each other, since it is unidirectional
            print("linking:", strA+',', strB)
            self.vertices[strA].addNeighbour(objB,(dir+2)%4, distance, time)
            self.vertices[strB].addNeighbour(objA, dir, distance, time)
            # return if successful
            return True
        return False

    def removeNeighbour(self, objA, objB):
        if objA in self.vertices and objB in self.vertices:
            # this portion removes he neighbours from each other, since it is unidirectional
            # returns if the operation succeeded
            self.edges += 1
            return self.vertices[objA].removeNeighbour(objB) and self.vertices[objB].removeNeighbour(objA)
        return False


    def update(self, time):
        loss = 0
        traffic = np.zeros((self.numVertices(), self.numVertices()))
        waiting = np.zeros((self.numVertices(), self.numVertices()))
        for i in range(len(self.cars)-1,-1,-1):
            if (not self.cars[i].active):
                loss += self.cars[i].tTime/self.cars[i].tDist
                del(self.cars[i])
                self.initCar(wb2["Sheet2"]["{}{}".format(letters[0], randint(1,18))].value)
            else:
                if self.cars[i].direction%2 == self.cars[i].nextNode.getDirection() and self.cars[i].distance <= 20:
                    waiting[self.cars[i].currentNode.num][self.cars[i].nextNode.num] += 1
                    
                elif (self.cars[i].distance <= 5):
                    # TODO make this part exponential?
                    self.cars[i].passInter()
                    if self.cars[i].nextNode != None:
                        print(self.cars[i].currentNode.getCoord(), "->",self.cars[i].nextNode.getCoord())
                else:
                    self.cars[i].distance -= self.cars[i].velocity * time
                    traffic[self.cars[i].currentNode.num][self.cars[i].nextNode.num] += 1
        return [traffic, waiting, loss]



# acts as the node to display the country or team etc
class Node():
    def __init__(self, n0, n1, num):
        # a value holding the location of the place
        # if a user owns all nodes of a continent then they gain more troops
        self.num = num
        self.direction = True
        # how many troops they have
        # the position to display on the screen
        self.y = n0
        self.x = n1
        # when the data is reset
        self.neighbours = [None for i in range(4)]
        self.wait = Queue()
        self.act = Queue()
        self.distances = [0 for i in range(4)]
        self.traffic = [0 for i in range(4)]
        self.time = [0 for i in range(4)]

    def addNeighbour(self, obj, dirc, distance, time):
        # adds a new neighbour to the vertex with a given distance
        if self.neighbours[dirc] == None:
            self.neighbours[dirc] = obj
            self.distances[dirc] = distance
            self.time[dirc] = time
            return True
        return False

    def removeNeighbour(self, dirc):
        # deletes a neighbour from the vertex
        if dirc in self.neighbours:
            del self.neighbours[dirc]
            del self.cars[dirc]
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
        print(obj)
        for i in range(4):
            if self.currentNode.getNeighbours()[i] == None:
                options.append((i+2)%4)
        self.direction = options[randint(0,len(options)-1)]
        self.nextNode = self.currentNode.getNeighbours()[self.direction]
        self.tTime = 0
        self.tDist = 1
        self.active = True
        self.distance = self.currentNode.distances[self.direction]
        self.tDist += self.currentNode.distances[self.direction]
        self.time = self.currentNode.time[self.direction]
        self.tTime += self.currentNode.time[self.direction]
        self.velocity = self.distance/self.time
        print(self.currentNode.getCoord(), self.direction, self.nextNode.getCoord(),self.distance,self.time)
        
    def getCoords(self):
        if (self.nextNode != None):
            y1,x1 = self.nextNode.getCoord()
            y2,x2 = self.currentNode.getCoord()
            percent = float(self.currentNode.distances[self.direction] - self.distance) / self.currentNode.distances[self.direction]
            gapY = y1 - y2
            gapX = x1 - x2
            x = x2 + gapX*percent
            y = y2 + gapY*percent
            return (y, x)
        else:
            self.active = False
            return (0, 0)
        
    def dump(self):
        print("Direction: ", self.direction, " Distance: ", self.distance, " Velocity: ", self.velocity, " Cur Node: ", self.currentNode.getCoord(), " Next Node: ", self.nextNode.getCoord())

    def passInter(self):
        self.currentNode = self.nextNode
        self.detNext()


    def detNext(self):
        if self.active:
            choice = randint(0,100)
            # turn car right
            if choice < 12:
                self.direction = (self.direction + 1) % 4
            # turn car left
            elif choice < 24:
                self.direction = (self.direction - 1) % 4
            self.nextNode = self.nextNode.getNeighbours()[self.direction]
            if self.nextNode == None:
                self.active = False
            else:
                self.distance = self.currentNode.distances[self.direction]
                self.tDist += self.currentNode.distances[self.direction]
                self.time = self.currentNode.time[self.direction]
                self.tTime += self.currentNode.distances[self.direction]
                self.velocity = self.distance/self.time

def setupField():
    # Create and link the graph
    toronto = Graph()
    
    
    for i in range(0,30):
            toronto.addVertex(longitudes[i], latitudes[i])
    
    for i in range (0,5):
        for n in range(0,6):
            index = i*6+n
            index0 = (i+1)*6+n
            index1 = i*6+n+1
            if i < 4:
                toronto.addNeighbour(str(longitudes[index]) + ', ' + str(latitudes[index]),
                                     str(longitudes[index0]) + ', ' + str(latitudes[index0]))
            if n < 5:
                toronto.addNeighbour(str(longitudes[index]) + ', ' + str(latitudes[index]),
                                     str(longitudes[index1]) + ', ' + str(latitudes[index1]))
    #TODO, save into a pickle for faster startup
    for i in range(100):
        temp = randint(0,17)
        toronto.initCar(edges[temp])
#        toronto.update(4)
    return toronto


