import numpy as np
import time

#Stores the info on one traffic light, 4 will be used to represent all directions
class TrafficLight:
    #The state is what light it is on
    #0 = green, 1 = yellow, 2 = red
    def __init__(self, state):
        self.state = state
        self.lastUpdated = time.time()
        self.timeThresh = 3.0
    
    def setState(self, state):
        self.state = state
    def getState(self):
        return self.state
    
    #Toggles light b/w green and red (and vice versa) with yellow delay
    def trigger(self):
        if (self.state == 0):
            self.lastUpdated = time.time()
            self.state = 1
        else:
            self.state = 0
    
    #Needed for yellow delay
    def update(self):
        if (time.time() - self.timeThresh > 0 and self.state == 1):
            self.state = 2

#The class doing the controlling, changes lights with certain logic
class TrafficController:
    #initLightStates - a list or array of 4 representing the starting config of the lights
    def __init__(self, initLightStates):
        #Counts obtained from video recognition
        #0 - North
        #1 - East
        #2 - South
        #3 - West
        self.humanCount = np.zeros(4)
        self.vehicleCount = np.zeros(4)
    
        #What state the light is in 
        self.lights = [TrafficLight(initLightStates[i]) for i in range(4)]
        
        self.carThresh = 15
        self.timeThresh = 30.0
        self.lastTrigger = time.time()
    
    #resets lights to given values
    #states - list or array of starting config of lights
    def resetLights(self, states):
        self.lights = [TrafficLight(states[i]) for i in range(4)]
    
    #gets lights as list of 4
    def getLights(self):
        return [l.getState() for l in self.lights]
        
    #updates the number of humans and vehicles in view (is a list, one index for each dir)
    def updateCount(self, vehicleCount, humanCount):
        self.humanCount = humanCount
        self.vehicleCount = vehicleCount
        
    #gets which way traffic is currently moving
    #0 - north south, 1 - east west
    def getDir(self):
        if (self.lights[0].getState() == 0 or self.lights[0].getState() == 1):
            return 1
        else:
            return 0
    
    #checks the logic for every frame of live stream
    #will change lights if needed
    def tick(self):
        #update all lights to see if they are yellow and need to be red
        for l in self.lights:
            l.update()
            
        #get the direction so we know which count to gather
        d = self.getDir()
        #get the counts of the waiting patrons
        waitHumanCount = self.humanCount[d] + self.humanCount[d+2]
        waitVehicleCount = self.vehicleCount[d] + self.vehicleCount[d+2]
        
        #Logic 0: if there is at least one car waiting, change lights after a time threshold
        if (waitVehicleCount > 0):
            if (time.time() - self.lastTrigger > self.timeThresh):
                print("Time from more than 0 cars")
                self.lastTrigger = time.time()
                for l in self.lights:
                    l.trigger()
        #Logic 1: if there are enough cars waiting, change immediately
        if (waitVehicleCount > self.carThresh):
            if (time.time() - self.lastTrigger > self.timeThresh/2):
                print("Excess limit of cars")
                if humanbool == 1:
                    time.sleep(7)
                self.lastTrigger = time.time()
                for l in self.lights:
                    l.trigger()
        #Logic 2: if there is at least one human waiting, change lights after a time threshold
        if (waitHumanCount > 0):
            if (time.time() - self.lastTrigger > self.timeThresh):
                print("Human waiting")
                self.lastTrigger = time.time()
                for l in self.lights:
                    l.trigger()

    def humanCheck(self, out):
        humanbool = 0
        objCount = int(out[0][0])
        objList = out[3][0][:objCount]
        for i in range(objCount):
            if objList[i] == 1:
                left = bbox[0]
                right = bbox[2]
                if right < 0.77:
                    print("Human crossing, change after timer")
                    humanbool = 1
                    return humanbool
                elif left > 0.12:
                    print("Human crossing, change after timer")
                    humanbool = 1
                    return humanbool
            