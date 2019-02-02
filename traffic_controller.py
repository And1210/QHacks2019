import numpy as np
import time

class trafficLight:
    #The state is what light it is on
    #0 = green, 1 = yellow, 2 = red
    def __init__(self, state):
        self.state = state
        self.lastUpdated = 0
        self.timeThresh = 2.0
    
    def setState(self, state):
        self.state = state
    def getState(self):
        return self.state
    
    def trigger(self):
        if (self.state == 0):
            self.lastUpdated = time.time()
            self.state = 1
        else:
            self.state = 0
    
    def update(self):
        if (time.time() - self.timeThresh > 0 and self.state == 1):
            self.state = 2


class trafficController:
    def __init__(self):
        #Counts obtained from video recognition
        #0 - North
        #1 - East
        #2 - South
        #3 - West
        self.humanCount = np.zeros(4)
        self.vehicleCount = np.zeros(4)
    
        #What state the light is in 
        self.lights = [trafficLight(2*(i%2)) for i in range(4)]
        
        self.carThresh = 15
        self.timeThresh = 30.0
        self.lastTrigger = -self.timeThresh
    
    def resetLights(self, states):
        self.lights = [trafficLight(states[i]) for i in range(4)]
        
    def updateCount(self, humanCount, vehicleCount):
        self.humanCount = humanCount
        self.vehicleCount = vehicleCount
        
    def getDir(self):
        if (self.lights[0].getState() == 0 or self.lights[0].getState() == 1):
            return 0
        else:
            return 1
    
    def tick(self):
        d = self.getDir()
        waitHumanCount = self.humanCount[d] + self.humanCount[d+2]
        waitVehicleCount = self.vehicleCount[d] + self.vehicleCount[d+2]
        if (waitVehicleCount > 0):
            if (time.time() - self.lastTrigger > self.timeThresh):
                self.lastTrigger = time.time()
                for l in self.lights:
                    l.trigger()
        if (waitVehicleCount > self.carThresh):
            if (time.time() - self.lastTrigger > self.timeThresh/2):
                self.lastTrigger = time.time()
                for l in self.lights:
                    l.trigger()
        if (waitHumanCount > 0):
            if (time.time() - self.lastTrigger > self.timeThresh):
                self.lastTrigger = time.time()
                for l in self.lights:
                    l.trigger()
            
            