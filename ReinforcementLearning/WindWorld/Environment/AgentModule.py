'''
Created on 15 Nov 2018

@author: hoanglong
'''

import numpy as np
import WorldModule as wm
import pickle

class Agent(object):
    '''
    classdocs
    '''


    def __init__(self,  mapSize, maxVel, maxWind, regenerateQ=False, maxAction = 2, x0 = 0, y0 = 0):
        '''
        Constructor
        '''
        self.x = x0
        self.y = y0
        self.vx = 0
        self.vy = 0
        self.windx = 0
        self.windy = 0
        self.maxVx = maxVel[0]
        self.maxVy = maxVel[1]
        #self.Q1 = np.zeros((mapSize[0], mapSize[1], maxVel[0] * 2 + 1, maxVel[1] * 2 + 1))
        #self.Q2 = np.zeros((4 * maxVel[0] + 1, 4 * maxVel[1] + 1, maxWind[0], maxWind[1], 2 * maxAction + 1, 2 * maxAction + 1))
        #remove wind effect for now
        if regenerateQ == False:
            try:
                src = open("Agen_Q1", "r")
                self.Q1 = pickle.load(src)
            except (IOError):
                self.Q1 = np.zeros((mapSize[0], mapSize[1], maxVel[0] * 2 + 1, maxVel[1] * 2 + 1, 2 * maxAction + 1, 2 * maxAction + 1))
        else:
            self.Q1 = np.zeros((mapSize[0], mapSize[1], maxVel[0] * 2 + 1, maxVel[1] * 2 + 1, 2 * maxAction + 1, 2 * maxAction + 1))
       
        self.testTime = False
        self.maxAction = 2 * maxAction + 1
        self.gamma = 1
        self.alpha = 0.1
        self.goalReached = False
        
    def getPosition(self):
        return (self.x, self.y)
    
    def setPosition(self, x, y):
        self.x = x 
        self.y = y 
        
    def getVelocity(self):
        return (self.vx, self.vy)
    
    def setVelocity(self, vx, vy):
        self.vx = vx
        self.vy = vy
    
    def setWind(self, wx, wy):
        self.windx = wx
        self.windy = wy
    
    def attachWorld(self, world):
        self.world = world
        
    def setAfterVeloctiy(self, vx, vy):
        self.afterVx = vx #use these for learning
        self.afterVy = vy 
        
    
    def setTargetPosition(self, x, y):
        self.target_x = x
        self.target_y = y
        
    def act(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_vx = self.vx
        self.prev_vy = self.vy
        #=======================================================================
        # if self.testTime == False:
        #     epsilon = np.random.rand()
        # if epsilon < 0.5:
        #     target_v = np.argmax(self.Q1[self.x, self.y])
        # else:
        #     target_v = np.random.randint(0, self.maxVx * 2 + 1) * self.maxVy + np.random.randint(0, self.maxVy * 2 + 1) 
        #           
        # target_vx = target_v / self.maxVy - self.maxVx
        # target_vy = target_v % self.maxVy - self.maxVy
        #      
        # self.target_ax = target_vx - self.vx
        # self.target_ay = target_vy - self.vy
        #        
        # epsilon = np.random.rand()
        #        
        # if epsilon < 0.5:
        #     action = np.argmax(self.Q2[self.target_ax, self.target_ay, self.windx, self.windy])
        # else:
        #     action = np.random.randint(0, self.maxAction) * self.maxAction + np.random.randint(0, self.maxAction) 
        #            
        # action_x = action / self.maxAction - ((self.maxAction - 1) / 2)
        # action_y = action % self.maxAction - ((self.maxAction - 1) / 2)
        # self.vx = self.vx + action_x
        # self.vy = self.vy + action_y
        #=======================================================================
            
        #=======================================================================
        # remove wind effect for now
        #=======================================================================
        if self.testTime == False:
            epsilon = np.random.rand()
            
            if epsilon < 0.95:
                action = np.argmax(self.Q1[self.x, self.y, self.vx, self.vy])
            else:
                action = np.random.randint(0, self.maxAction) * self.maxAction + np.random.randint(0, self.maxAction) 
                
            temp = self.Q1[self.x, self.y, self.vx, self.vy]
            self.action_x = action / self.maxAction
            self.action_y = action % self.maxAction
            self.vx = self.vx + self.action_x - ((self.maxAction - 1) / 2)
            self.vy = self.vy + self.action_y - ((self.maxAction - 1) / 2)
    
    def reset(self, x0 = 0, y0 = 0):
        self.goalReached = False
        self.x = x0
        self.y = y0
        self.vx = 0
        self.vy = 0
        
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
            
        #=======================================================================
        # prev_vx = self.x - self.prev_x
        # prev_vy = self.y - self.prev_y
        # 
        # self.Q1[self.prev_x, self.prev_y, prev_vx, prev_vy] += self.alpha * (ret + self.gamma * np.max(self.Q1[self.x, self.y]) - self.Q1[self.prev_x, self.prev_y, prev_vx, prev_vy])
        # 
        # ret = -self.afterVx - self.afterVy
        # self.Q2[self.target_ax, self.target_ay, self.windx, self.windy] += self.alpha * (ret + self.gamma * np.max(self.Q1[self.x, self.y]) - self.Q1[self.prev_x, self.prev_y, prev_vx, prev_vy])
        #=======================================================================
        temp1 = self.Q1[self.prev_x, self.prev_y, self.prev_vx, self.prev_vy]
        temp2 = self.Q1[self.x, self.y, self.vx, self.vy]
        self.Q1[self.prev_x, self.prev_y, self.prev_vx, self.prev_vy, self.action_x, self.action_y] += self.alpha * (ret + self.gamma * np.max(self.Q1[self.x, self.y, self.vx, self.vy]) - self.Q1[self.prev_x, self.prev_y, self.prev_vx, self.prev_vy, self.action_x, self.action_y])
        temp3 = self.Q1[self.prev_x, self.prev_y, self.prev_vx, self.prev_vy]
        
        temp3 = self.Q1[self.prev_x, self.prev_y, self.prev_vx, self.prev_vy]
            
            
    def saveQ(self):
        dest = open("Agen_Q1", "w")
        pickle.dump(self.Q1, dest)
        
