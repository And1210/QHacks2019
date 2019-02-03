#longitudes = [43.664356, 43.664932, 43.665730, 43.666264, 43.667071, 43.668180, 43.660837, 43.661403, 43.661898, 43.662422, 43.663183, 43.664295, 43.658455, 43.659094, 43.659910, 43.660467, 43.661243, 43.662322, 43.655775, 43.656292, 43.656518, 43.657050, 43.658301, 43.659381, 43.651870, 43.652448, 43.653161, 43.653713, 43.654510, 43.655605]
#latitudes = [-79.387163, -79.384514, -79.380942, -79.378328, -79.374680, -79.369546, -79.385846, -79.383101, -79.379297, -79.376687, -79.373071, -79.367982, -79.384852, -79.382114, -79.378477, -79.375801, -79.372213, -79.367185, -79.383666, -79.380896, -79.377131, -79.374553, -79.370947, -79.365975, -79.381810, -79.379307, -79.375726, -79.373216, -79.369440, -79.364435]
import numpy as np
from flask import Flask
from flask_cors import CORS

from sklearn.cluster import KMeans
#from ClusteringLayer import ClusteringLayer

from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adagrad

from node import setupField

class Simulator:
    def __init__(self):
        self.graph = setupField()
        self.model = Sequential()
        self.initSupervisedModel(self.graph.edges*4, self.graph.numVertices())
    
    def initSupervisedModel(self, inputNum, outputNum):
        self.model.add(Dense(64, activation='relu', input_dim=inputNum))
        self.model.add(Dense(32, activation='sigmoid'))
        self.model.add(Dense(32, activation='sigmoid'))
        self.model.add(Dense(outputNum, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer=Adagrad(0.05),
              metrics=['accuracy'])        
    def trainSupervisedStep(self, xData, yData):
        return self.model.fit(xData, yData, 4)
    def feedForwardSupervised(self, data):
        return self.model.predict(data)
        
    def initKMeans(self, outputNum):
        self.n_clusters = outputNum
        self.model = KMeans(n_clusters=self.n_clusters, n_init=10, n_jobs=4)
    def predictKMeans(self, data):
        return self.model.fit_predict(data)
    
#    def clusterSampleInit(self, outputNum):
#        self.model.add(ClusteringLayer(n_clusters=outputNum))    
#    def clusterSampleTrain(self, data):
#        pass
        
    def update(self):
        self.trainSupervisedStep()
      
sim = Simulator()


#Returns the GEOJSON for one feature
def getFeature(title, state, lon, lat):
    out = '{"type": "Feature", "properties": { "title": "' + str(title) + '", "description": "' + str(state) + '"}, "geometry": { "coordinates": [' + str(lat) + ', ' + str(lon) + '], "type": "Point" }}'
    return out
def getFeatures():
    out = '{"features":['
    for i in range(len(sim.graph.cars)):
        (lon, lat) = sim.graph.cars[i].getCoords()
        title = 'Car' + str(i)
        if (i < len(sim.graph.cars) - 1):
            out = out + getFeature(title, 1, lon, lat) + ', '
        else:
            out = out + getFeature(title, 1, lon, lat)
    out = out + '], "type": "FeatureCollection"}'
    return out
        
#Start server
app = Flask(__name__)
CORS(app)

@app.route("/")
def main():
    data = getFeatures()
    sim.graph.update(10)
    return data
#
if __name__ == "__main__":
    app.run()
