'''
Created on 24 Nov 2018

@author: hoanglong
'''

from Environment import IWorldMapModule
import Environment.MapGeneratorModule as gm
import numpy as np
import copy 

class SimpleWorldMap(IWorldMapModule.IWorldMap):
    '''
    WorldMap object, used to abstract map implementation from WorldModule
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.PATH_VAL = 0
        self.OBSTACLE_VAL = 1
        self.GOAL_VAL = 2
        self.mapGenerator = gm.MapGenerator()
        if self.mapGenerator.checkBlankMap():
            self.generateMap()
        self.map = copy.deepcopy(self.mapGenerator.getMap())
        self.width = np.shape(self.map)[0]
        self.height = np.shape(self.map)[1]
        self.originalMap = self.mapGenerator.getMap()
    
    def generateMap(self, height=30, width=30, numOfObstacles=10, obstacleSize=10):
        self.mapGenerator.generateBlankMap()
        obstacleList = []
        for i in range(numOfObstacles):
            x1 = np.random.randint(1, width)
            y1 = np.random.randint(1, height)
            x2 = max(min(x1 + np.random.randint(-obstacleSize / 2 + 1, obstacleSize / 2), 0), width)
            y2 = max(min(y1 + np.random.randint(-obstacleSize / 2 + 1, obstacleSize / 2), 0), height)
            if x2 == 0 and y2 == 0:
                x2 = 1
            obstacleList.append((x1, y1, x2, y2))
            
        self.mapGenerator.addStraightBlocks(obstacleList, self.OBSTACLE_VAL)
        #add goal
        x_goal = width - 1
        y_goal = np.random.randint(0, height)
        self.mapGenerator.addObject([(x_goal, y_goal)], self.GOAL_VAL)
        
        self.map = self.mapGenerator.getMap()
        
    def isObstacle(self, x, y):
        if (x >= 0) and (x < self.width) and (y >= 0) and (y < self.height) and self.map[x, y] == self.OBSTACLE_VAL:
            return True
        else:
            return False
        
    def isGoal(self, x, y):
        if (x >= 0) and (x < self.width) and (y >= 0) and (y < self.height) and self.map[x, y] == self.GOAL_VAL:
            return True
        else:
            return False
    
    def isPath(self, x, y):
        if (x >= 0) and (x < self.width) and (y >= 0) and (y < self.height) and (self.map[x, y] == self.PATH_VAL):
            return True
        else:
            return False
            
    def getMapSize(self):
        return self.width, self.height
    
    def markPositionTemporarily(self, x, y, val):
        if (x >= 0) and (x < self.width) and (y >= 0) and (y < self.height):
            self.map[x, y] = val + self.GOAL_VAL  + 1
            pass
        
    def unmark(self, x, y):
        if (x >= 0) and (x < self.width) and (y >= 0) and (y < self.height):
            self.map[x, y] = self.originalMap[x, y]
        
    def isMark(self, x, y, val):
        if (x >= 0) and (x < self.width) and (y >= 0) and (y < self.height) and (val == self.map[x, y] - self.GOAL_VAL - 1):
            return True
        else:
            return False
            pass
    