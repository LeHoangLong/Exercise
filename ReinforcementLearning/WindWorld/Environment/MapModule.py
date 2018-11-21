'''
Created on 14 Nov 2018


@author: hoanglong
'''

import numpy as np
import copy

class Map(object):
    '''
    generate map
    '''


    def __init__(self):
        '''
        Constructor
        '''
        if self.loadMap() == False:
            self.generateMap()
        
    def generateMap(self, height = 30, width = 30, numOfObstacles = 15, obstacleSize = 10):
        self.map = np.zeros((height, width), np.int32)
        for i in range(numOfObstacles):
            x1 = np.random.randint(0, width)
            y1 = np.random.randint(0, height)
            x2 = min(max(x1 + np.random.randint(-obstacleSize, obstacleSize + 1), 0), width - 1)
            y2 = min(max(y1 + np.random.randint(-obstacleSize, obstacleSize + 1), 0), height -1)
            if y2 != y1:
                tan = (x2 - x1) * 1.0 / (y2 - y1)
                for j in range(y2 - y1 + 1):
                    self.map[np.round(x1 + j * tan), y1 + j] = 1
                    temp = np.round(x1 + j * tan)
                    temp2 = y1 + j
            elif x2 !=  x1:
                cot = (y2 - y1) * 1.0 / (x2 - x1) 
                for j in range(x2 - x1 + 1):
                    self.map[x1 + j, np.round(y1 + j * cot)] = 1
            else:
                self.map[x1, y1] = 1
        
        self.map[width - 1, np.random.randint(0, height)] = 2
                
        f = open("map", "w")
        
        f.write(str(width) + " " + str(height) + "\n")
        
        for j in range(height):
            for i in range(width):
                f.write(str(self.map[i, j]) + " ")
            f.write("\n")
        f.close()
    
    def loadMap(self):
        try:
            f = open("map", "r")
            j = 0
            
            firstLine = f.readline()
            lst = firstLine.split()
            self.map = np.zeros((int(lst[0]), int(lst[1])), np.int32)
            
            for j, line in enumerate(f):
                lst = line.split()
                for i in range(len(lst)):
                    self.map[i, j] = int(lst[i])
            return True
        except:
            return False
                
    def getMap(self):
        return self.map
        