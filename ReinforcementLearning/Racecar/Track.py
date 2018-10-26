import numpy as np
import sys
from operator import pos

class Track:
    def __init__(self):
        self.map = np.zeros((10, 30))
        self.x = 0
        self.y = 0
        self.finishLine_x = 0
        self.allowMove = False
        if self.loadMap() == False:
            self.generateMap()
            
            
    def loadMap(self):
        try:
            mapFile = open("map", "r")
            for j in reversed(range(np.shape(self.map )[1])):
                l = mapFile.readline().split()
                for i, w in enumerate(l):
                    if w == "1":
                        self.map[i, j] = 1
                        if j == np.shape(self.map )[1] - 1:
                            self.finishLine_x = i
                    else:
                        self.map[i, j] = 0
            return True
        except:
            return False
            
        
    def generateMap(self):
        prev_start = 0
        prev_end = 0
        
        mapFile = open("map", "w")
        
        for i in range(np.shape(self.map)[1]):
            if i == 0:
                start = 0
                end = 2
            elif i < np.shape(self.map)[1] - 5:
                start = prev_start + np.random.randint(-1, 2)
                end = prev_end + np.random.randint(-1, 2)
                if start < 0:
                    start = 0
                if end > 9:
                    end = 9
                if end - start < 1:
                    if start + 1 >= np.shape(self.map)[0]:
                        start = start - 2
                    else:
                        end = end + 2
            else:
                #finish line
                start = prev_start + np.random.randint(-1, 2)
                if start < 0:
                    start = 0
                if end - start < 3:
                    end = start + 3
                self.finishLine_x = end
            for j in range(np.shape(self.map)[0]):
                if j >= start and j <= end:
                    self.map[j, i] = 1
                else:
                    self.map[j, i] = 0
            prev_start = start
            prev_end = end
            
        for j in reversed(range(np.shape(self.map)[1])):
            for i in range(np.shape(self.map)[0]):
                if self.map[i, j] == 1:
                    mapFile.write("1 ")
                else:
                    mapFile.write("0 ")
            mapFile.write("\n")
            
    def initializePosition(self):
        self.y = 0
        self.x = np.random.randint(0, 3)
        self.velocity = np.zeros(2)
    
    def getPosition(self):
        return (self.x, self.y)
    
    def setPositionAndVelocity(self, pos, vel):
        self.x = pos[0]
        self.y = pos[1]
        self.velocity[0] = vel[0]
        self.velocity[1] = vel[1]
        
    def getVelocity(self):
        return np.copy(self.velocity)
    
    def getTrackShape(self):
        return np.shape(self.map)
    
    def increaseVelocity(self, deltaV):
        if not ((self.velocity[0] <= -3 and deltaV[0] < 0) or (self.velocity[0] >= 3 and deltaV[0] > 0)):
            self.velocity[0] += deltaV[0]
        if not ((self.velocity[1] <= -3 and deltaV[1] < 0) or (self.velocity[1] >= 3 and deltaV[1] > 0)):
            self.velocity[1] += deltaV[1]
        
    def enableMove(self):
        self.allowMove = True
    
    def disableMove(self):
        self.allowMove = False
        
    def move(self):
        if self.allowMove == False:
            return 0
        self.x = self.x + self.velocity[0]
        self.y = self.y + self.velocity[1]
        max_width, max_height = np.shape(self.map)
        if self.x < 0 or self.x >= max_width or self.y < 0 or self.y >= max_height or self.map[int(self.x), int(self.y)] == 0: #run out of track
            self.y = 0
            self.x = np.random.randint(0, 3)
            self.velocity[0] = 0
            self.velocity[1] = 0
            return 1
        else:
            if self.y >= np.shape(self.map)[1] - 5 and self.x >= self.finishLine_x:
                return 2 #reached finish line
        return 0
            
    def printCurrentPos(self):
        for j in reversed(range(np.shape(self.map)[1])):
            for i in range(np.shape(self.map)[0]):
                if self.x == i and self.y == j:
                    sys.stdout.write("x ")
                else:
                    if self.map[i, j] == 1:
                        sys.stdout.write("1 ")
                    else:
                        sys.stdout.write("0 ")
            sys.stdout.write("\n")
        print(self.velocity)