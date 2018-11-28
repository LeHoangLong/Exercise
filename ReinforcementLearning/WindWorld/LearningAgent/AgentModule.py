'''
Created on 15 Nov 2018

@author: hoanglong
'''

import numpy as np
import Environment.SimpleWorldModule as wm
import Environment.ICollidableWorldModule as cwm
from LearningAgent import IAgentModule

class SimpleAgent(IAgentModule.IAgent):
    '''
    classdocs
    '''


    def __init__(self,  world, regenerateQ=False, maxAction = 2, x0 = 0, y0 = 0):
        '''
        Constructor
        '''
        self.x = x0
        self.y = y0
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.target_x = 0
        self.target_y = 0 
        self.goalReached = False
        self.world = world 
        self.world.setGoal(self)
        maxStates = world.getLimitOfStates()
        mapSize = world.getMap().getMapSize()
        self.maxVx = maxStates[2][1]
        self.maxVy = maxStates[3][1]
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_vx = self.vx
        self.prev_vy = self.vy
        #self.Q1 = np.zeros((mapSize[0], mapSize[1], maxVel[0] * 2 + 1, maxVel[1] * 2 + 1))
        #self.Q2 = np.zeros((4 * maxVel[0] + 1, 4 * maxVel[1] + 1, maxWind[0], maxWind[1], 2 * maxAction + 1, 2 * maxAction + 1))
        #remove wind effect for now
        self.Q1 = 0
        if regenerateQ == False:
            try:
                super()._protected_load("Agent_Q1", self.Q1)
            except (Exception):
                self.Q1 = np.zeros((mapSize[0], mapSize[1], self.maxVx * 2 + 1, self.maxVx * 2 + 1, 2 * maxAction + 1, 2 * maxAction + 1))
        else:
            self.Q1 = np.zeros((mapSize[0], mapSize[1], self.maxVx * 2 + 1, self.maxVx * 2 + 1, 2 * maxAction + 1, 2 * maxAction + 1))
       
        self.testTime = False
        self.maxAction = 2 * maxAction + 1
        self.gamma = 1
        self.alpha = 0.1
        self.goalReached = False
    
    def getStates(self):
        '''
        '''
        return (self.x, self.y, self.vx, self.vy, self.ax, self.ay)
        pass
    
    def setStates(self, states):
        self.x, self.y, self.vx, self.vy, self.ax, self.ay = states
        pass
    
    def getActions(self):
        return self.action_x, self.action_y
        pass
    
    def setGoal(self, goal):
        self.target_x = goal[0][0]
        self.target_y = goal[0][1]
        
    def act(self):
        #=======================================================================
        # remove wind effect for now
        #=======================================================================
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_vx = self.vx
        self.prev_vy = self.vy
        if self.testTime == False:
            epsilon = np.random.rand()
            
            if epsilon < 0.95:
                action = np.argmax(self.Q1[self.x, self.y, self.vx, self.vy])
            else:
                action = np.random.randint(0, self.maxAction) * self.maxAction + np.random.randint(0, self.maxAction) 
                
            self.action_x_index = action // self.maxAction
            self.action_y_index = action % self.maxAction
            self.action_x =  self.action_x_index - ((self.maxAction - 1) / 2)
            self.action_y =  self.action_y_index - ((self.maxAction - 1) / 2)
        self.world.act(self)
        self.learn()
        
    def notifyGoalReached(self):
        self.goalReached = True
        #self.saveQ()
        
    def learn(self):
        if self.goalReached == True:
            ret = 1000
        else:
            if self.prev_x == self.x and self.prev_y == self.y:
                ret = -5 - abs((self.target_x - self.x)) - abs((self.target_y - self.y))
            else:
                ret = -1 - abs((self.target_x - self.x)) - abs((self.target_y - self.y))
            
        self.Q1[self.prev_x, self.prev_y, self.prev_vx, self.prev_vy, self.action_x_index, self.action_y_index] += self.alpha * (ret + self.gamma * np.max(self.Q1[self.x, self.y, self.vx, self.vy]) - self.Q1[self.prev_x, self.prev_y, self.prev_vx, self.prev_vy, self.action_x_index, self.action_y_index])
            
            
    def saveQ(self):
        super()._protected_save("Agent_Q1", self.Q1)
        
    
