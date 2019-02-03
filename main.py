import numpy as np
from video_recog import VideoRecognize
from traffic_controller import TrafficController
import mapbox_helper as mb
from flask import Flask
from flask_cors import CORS

#Setting up video recognizer
video = "rushhour.mp4"
graph = "frozen_inference_graph.pb"
videoGrab = VideoRecognize(video, graph)

#Setting up traffic controller
controllers = [TrafficController([0, 2, 0, 2]) for i in range(30)]

#Setting up count arrays
vehicleCounts = np.zeros(4)
peopleCounts = np.zeros(4)

#Hardcoded intersections in Toronto
longitudes = [43.664356, 43.664932, 43.665730, 43.666264, 43.667071, 43.668180, 43.660837, 43.661403, 43.661898, 43.662422, 43.663183, 43.664295, 43.658455, 43.659094, 43.659910, 43.660467, 43.661243, 43.662322, 43.655775, 43.656292, 43.656518, 43.657050, 43.658301, 43.659381, 43.651870, 43.652448, 43.653161, 43.653713, 43.654510, 43.655605]
latitudes = [-79.387163, -79.384514, -79.380942, -79.378328, -79.374680, -79.369546, -79.385846, -79.383101, -79.379297, -79.376687, -79.373071, -79.367982, -79.384852, -79.382114, -79.378477, -79.375801, -79.372213, -79.367185, -79.383666, -79.380896, -79.377131, -79.374553, -79.370947, -79.365975, -79.381810, -79.379307, -79.375726, -79.373216, -79.369440, -79.364435]

#Returns the GEOJSON for one feature
def getFeature(title, state, lon, lat):
    out = '{"type": "Feature", "properties": { "title": "' + str(title) + '", "description": "' + str(state) + '"}, "geometry": { "coordinates": [' + str(lat) + ', ' + str(lon) + '], "type": "Point" }}'
    return out

#Returns 
def getFeatures():
    d0 = 0.0003
    d1 = 0.0002
    
    out = '{"features":['
    for i in range(len(longitudes)):
        lon = longitudes[i]
        lat = latitudes[i]
        title = 'Feature' + str(i)
        states = controllers[i].getLights()
        out = out + getFeature(title + chr(65), states[0], lon+d1, lat) + ', '
        out = out + getFeature(title + chr(66), states[1], lon, lat+d0) + ', '
        out = out + getFeature(title + chr(67), states[2], lon-d1, lat) + ', '
        out = out + getFeature(title + chr(68), states[3], lon, lat-d0) + ', '
        if (i < len(longitudes) - 1):
            out = out + getFeature(title, 3, lon, lat) + ', '
        else:
            out = out + getFeature(title, 3, lon, lat)
    out = out + '], "type": "FeatureCollection"}'
    return out

#print(getFeatures())

#Start server
app = Flask(__name__)
CORS(app)

@app.route("/")
def main():
    (vehicleCounts[0], peopleCounts[0]) = videoGrab.analyzeFrame()
    controllers[0].updateCount(vehicleCounts, peopleCounts)
    controllers[0].tick()
    data = getFeatures()
    return data
#
if __name__ == "__main__":
    app.run(host="192.168.137.1", port=80)

#out = mb.create('Test', '2', 44.6788, 43.8757).json()
#out = mb.update('City Hall', '0')

#videoGrab.startSess()
#while (True):
#    (vehicleCounts[0], peopleCounts[0]) = videoGrab.analyzeFrame()
#    controller.updateCount(vehicleCounts, peopleCounts)
#    controller.tick()
#    print(controller.getLights())
#videoGrab.stopSess()