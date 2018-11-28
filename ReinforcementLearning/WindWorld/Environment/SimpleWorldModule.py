'''
Created on 15 Nov 2018

@author: hoanglong
'''
from Environment import IWorldModule
import Environment.IWorldMapModule 
import Environment.SimpleWorldMap
from LearningAgent import AgentModule as am

import numpy as np

class SimpleWorld(IWorldModule.IWorld):
    '''
    Handle game physics
    '''


    def __init__(self, _map):
        '''
        Constructor
        '''
        self.MAX_VEL = 1
        self.MAX_ACC = 1
        self.map = _map
        self.mapWidth, self.mapHeight = self.map.getMapSize()
        self.windmap = np.random.randint(-1, 2, (self.mapWidth, self.mapHeight))
    
    def getMap(self):
        return self.map
        
    def resetAgent(self, agent):
        agent.setStates((0, 0, 0, 0, 0, 0 ))
        
    def getLimitOfStates(self):
        return ((0, self.mapWidth), (0, self.mapHeight), (-self.MAX_VEL, self.MAX_VEL),\
                (-self.MAX_VEL, self.MAX_VEL), (-self.MAX_ACC, self.MAX_ACC), (-self.MAX_ACC, self.MAX_ACC))
    
    def act(self, agent):
        x, y, vx, vy, ax, ay = agent.getStates()
        action_x, action_y = agent.getActions()
        prev_vx = vx
        prev_vy = vy
        ax = vx - prev_vx
        ay = vy - prev_vy
        vx = vx + action_x
        vy = vy + action_y
        vx = min(max(vx, -self.MAX_VEL), self.MAX_VEL)
        vy = min(max(vy, -self.MAX_VEL), self.MAX_VEL)
        finalX = x
        finalY = y
        finalVx = vx
        finalVy = vy
        goalReached = False
        if vy != 0:
            cot = vx * 1.0 / vy
            for i in range(int(abs(vy) / vy), int(vy + abs(vy) / vy), int(abs(vy) / vy)):
                finalX_prev = finalX
                finalY_prev = finalY
                finalX = int(round(x + i * cot))
                finalY = y + i
                #Either it is goal, path or obstacle
                if self.map.isGoal(finalX, finalY):
                    goalReached = True
                    break
                elif not self.map.isPath(finalX, finalY):
                    finalX = finalX_prev
                    finalY = finalY_prev
                    finalVx = 0
                    finalVy = 0
                    break
                    
        elif vx != 0:
            tan = vy * 1.0 / vx
            for i in range(int(abs(vx) / vx), int(vx + abs(vx) / vx), int(abs(vx) / vx)):
                finalX_prev = finalX
                finalY_prev = finalY
                finalX = x + i
                finalY = int(round(y + i * tan))
                if self.map.isGoal(finalX, finalY):
                    goalReached = True
                    break
                elif not self.map.isPath(finalX, finalY):
                    finalX = finalX_prev
                    finalY = finalY_prev
                    finalVx = 0
                    finalVy = 0
                    break
        else:
            finalX = x
            finalY = y 
            
        #sanitary check
        finalX = min(max(finalX, 0), self.mapWidth)
        finalY = min(max(finalY, 0), self.mapHeight)
        
        agent.setStates((finalX, finalY, finalVx, finalVy, ax, ay))
        
        if goalReached == True:
            agent.notifyGoalReached()
        pass 
                    
    def setGoal(self, agent):
        goals = []
        for i in range(self.mapWidth):
            for j in range(self.mapHeight):
                if self.map.isGoal(i, j):
                    goals.append((i, j))
        agent.setGoal(goals)
            