import numpy as np
import tensorflow as tf
import cv2


#Analyzes given video footage (could be live streamed) to determine number of vehicles and pedestrians
class VideoRecognize:
    #videoName - the path of the video file (use 0 for computer camera)
    #graphName - the path to the .pd file containing the byte samples of feature
    def __init__(self, videoName, graphName):
        self.running = False
        #setup
        self.cap = cv2.VideoCapture(videoName)
        # Read the graph.
        with tf.gfile.FastGFile(graphName, 'rb') as f:
            self.graph_def = tf.GraphDef()
            self.graph_def.ParseFromString(f.read())

    def getInfo(self, index):
        if (index == 1):
            return 'person'
        elif (index == 3):
            return 'car'
        elif (index == 8):
            return 'truck'
    
    #Starts the session (must be called before analyzeFrame)
    def startSess(self):
        self.running = True
        try:
            self.sess = tf.Session()
            # Restore session
            self.sess.graph.as_default()
            tf.import_graph_def(self.graph_def, name='')
        except:
            self.running = False
            print("Error starting session")
    
    def analyzeFrame(self):
        if (self.running):
            # Read and preprocess an image.
            ret, img = self.cap.read()
            if (ret == False):
                return (-1, -1)
            rows = img.shape[0]
            cols = img.shape[1]
            inp = img
            inp = cv2.resize(img, (300, 300))
            inp = inp[:, :, [2, 1, 0]]  # BGR2RGB
        
            # Run the model
            out = self.sess.run([self.sess.graph.get_tensor_by_name('num_detections:0'),
                            self.sess.graph.get_tensor_by_name('detection_scores:0'),
                            self.sess.graph.get_tensor_by_name('detection_boxes:0'),
                            self.sess.graph.get_tensor_by_name('detection_classes:0')],
                           feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})
        
            # Visualize detected bounding boxes.
            num_detections = int(out[0][0])
            for i in range(num_detections):
                classId = int(out[3][0][i])
                score = float(out[1][0][i])
                bbox = [float(v) for v in out[2][0][i]]
                if score > 0.3:
                    x = bbox[1] * cols
                    y = bbox[0] * rows
                    right = bbox[3] * cols
                    bottom = bbox[2] * rows
                    cv2.rectangle(img, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)
            cv2.imshow('video', img)
            
            #getting the counts of different objects
            personCount = 0
            bikeCount = 0
            carCount = 0
            motorcycleCount = 0
            busCount = 0
            truckCount = 0
            trafficCount = 0
            
            objCount = int(out[0][0])
            objList = out[3][0][:objCount]
            print(objList)
            for i in range(objCount):
                if objList[i] == 1:
                    personCount = personCount + 1
                elif objList[i] == 2:
                    bikeCount = bikeCount + 1
                elif objList[i] == 3:
                    carCount = carCount + 1
                elif objList[i] == 4:
                    motorcycleCount = motorcycleCount + 1
                elif objList[i] == 6:
                    busCount = busCount + 1
                elif objList[i] == 8:
                    truckCount = truckCount + 1
            trafficCount = carCount + motorcycleCount + busCount + truckCount
            cv2.waitKey(50)
            return (trafficCount, personCount)
        else:
            return (-1, -1)
    
    #Stops the session from running
    def stopSess(self):
        cv2.destroyAllWindows() 
        del self.sess
                    
                    