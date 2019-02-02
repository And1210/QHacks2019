import numpy as np
from video_recog import VideoRecognize
from traffic_controller import TrafficController
import mapbox_helper as mb
from flask import Flask
from flask_cors import CORS
import random

#Setting up video recognizer
video = "rushhour.mp4"
graph = "frozen_inference_graph.pb"
videoGrab = VideoRecognize(video, graph)

#Setting up traffic controller
controller = [TrafficController([2*i%2, 2*((i+1)%2), 2*i%2, 2*((i+1)%2)]) for i in range(16)]

#Setting up count arrays
vehicleCounts = np.zeros(4)
peopleCounts = np.zeros(4)

#Hardcoded intersections in Toronto
longitudes = [43.659815, 43.660839, 43.661441, 43.659120, 43.651295, 43.652879, 43.657591, 43.658499, 43.647258, 43.648748, 43.650812, 43.650812, 43.646308, 43.648885, 43.649910, 43.650469]
latitudes = [-79.390429, -79.385869, -79.383075, -79.382163, -79.405618, -79.397979, -79.389331, -79.384834, -79.404031, -79.396349, -79.386606, -79.386606, -79.391091, -79.385684, -79.380792, -79.378517]

#Returns the GEOJSON for one feature
def getFeature(title, state, lon, lat):
    out = '{"type": "Feature", "properties": { "title": "' + str(title) + '", "description": "' + str(state) + '"}, "geometry": { "coordinates": [' + str(lat) + ', ' + str(lon) + '], "type": "Point" }}'
    return out

#Returns 
def getFeatures():
    out = '{"features":['
    for i in range(len(longitudes)):
        lon = longitudes[i]
        lat = latitudes[i]
        title = 'Feature' + str(i)
        state = int(controller[i].getLights()[0]/2)
        if (i < len(longitudes) - 1):
            out = out + getFeature(title, state, lon, lat) + ', '
        else:
            out = out + getFeature(title, state, lon, lat)
    out = out + '], "type": "FeatureCollection"}'
    return out

print(getFeatures())

app = Flask(__name__)
CORS(app)

@app.route("/")
def main():
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