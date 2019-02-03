#import numpy as np
#import random
#from node import Graph
#import math
#
#longitudes = [43.664356, 43.664932, 43.665730, 43.666264, 43.667071, 43.668180, 43.660837, 43.661403, 43.661898, 43.662422, 43.663183, 43.664295, 43.658455, 43.659094, 43.659910, 43.660467, 43.661243, 43.662322, 43.655775, 43.656292, 43.656518, 43.657050, 43.658301, 43.659381, 43.651870, 43.652448, 43.653161, 43.653713, 43.654510, 43.655605]
#latitudes = [-79.387163, -79.384514, -79.380942, -79.378328, -79.374680, -79.369546, -79.385846, -79.383101, -79.379297, -79.376687, -79.373071, -79.367982, -79.384852, -79.382114, -79.378477, -79.375801, -79.372213, -79.367185, -79.383666, -79.380896, -79.377131, -79.374553, -79.370947, -79.365975, -79.381810, -79.379307, -79.375726, -79.373216, -79.369440, -79.364435]

from keras.models import Sequential, load_model
from keras.layers import Activation, Dense, Dropout
from keras.optimizers import Adagrad

class Simulator:
    def __init__(self, graph):
        self.graph = graph
        self.model = Sequential()
        self.initModel(graph.edges*4, graph.getVertices())
    
    def initModel(self, inputNum, outputNum):
        self.model.add(Dense(64, activation='relu', input_dim=inputNum))
        self.model.add(Dense(32, activation='sigmoid'))
        self.model.add(Dense(32, activation='sigmoid'))
        self.model.add(Dense(outputNum, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer=Adagrad(0.05),
              metrics=['accuracy'])        
    
    def trainStep(self):
        xData = []
        yData = []
        
        #Gather input data
        for q in self.graph.queues:
            xData.append(np.array([len(q)]))
            yData.append(np.array([0]))
        
        self.model.fit(xData, yData, 4)
        
    def update(self):
        
                
