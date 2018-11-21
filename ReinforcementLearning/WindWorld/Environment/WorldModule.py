'''
Created on 15 Nov 2018

@author: hoanglong
'''
import AgentModule as am
import numpy as np

class World(object):
    '''
    Handle game physics
    '''


    def __init__(self, map):
        '''
        Constructor
        '''
        self.map = map
        self.windmap = np.random.randint(-1, 2, (np.shape(map)[0], np.shape(map)[1], 2))
        self.spawnAgent()
        self.mapWidth = np.shape(map)[0]
        self.mapHeight = np.shape(map)[1]
        for i in range(np.shape(map)[0]):
            for j in range(np.shape(map)[1]):
                if map[i, j] == 2:
                    self.agent.setTargetPosition(i, j)
                    break
            
        
    def getAgent(self):
        return self.agent
    
        
    def spawnAgent(self):
        self.agent = am.Agent(np.shape(self.map), (7, 7), (3, 3), False)
        self.agent.attachWorld(self)
        
    def timeStep(self):
        x, y = self.agent.getPosition()
        self.agent.setWind(self.windmap[x, y][0], self.windmap[x, y][1])
        self.agent.act()
        vx, vy = self.agent.getVelocity()
        #vx = min(max(vx + int(round(np.random.normal(self.windmap[x, y][0], 1))), -1), 1)
        #vy = min(max(vy + int(round(np.random.normal(self.windmap[x, y][1], 1))), -1), 1)
        #remove wind effect for now
        vx = min(max(vx, -1), 1)
        vy = min(max(vy, -1), 1)
        
        self.agent.setAfterVeloctiy(vx, vy)
        finalX = x
        finalY = y
        finalVx = vx
        finalVy = vy
        goalReached = False
        if vy != 0:
            tan = vx * 1.0 / vy
            for i in range(0, vy + abs(vy) / vy, abs(vy) / vy):
                finalX_prev = finalX
                finalY_prev = finalY
                finalX = int(round(x + i * tan))
                finalY = y + i
                if finalX < 0 or finalY < 0 or finalX >= self.mapWidth or finalY >= self.mapHeight or self.map[finalX, finalY] == 1:
                    finalX = finalX_prev
                    finalY = finalY_prev
                    finalVx = 0
                    finalVy = 0
                    break
                elif self.map[finalX, finalY] == 2:
                    goalReached = True
                    break
        elif vx != 0:
            cot = vy * 1.0 / vx
            for i in range(0, vx + abs(vx) / vx, abs(vx) / vx):
                finalX_prev = finalX
                finalY_prev = finalY
                finalX = x + i
                finalY = int(round(y + i * cot))
                if finalX < 0 or finalY < 0 or finalX >= self.mapWidth or finalY >= self.mapHeight or self.map[finalX, finalY] == 1:
                    finalX = finalX_prev
                    finalY = finalY_prev
                    finalVx = 0
                    finalVy = 0
                    break
                elif self.map[finalX, finalY] == 2:
                    goalReached = True
                    break
        else:
            finalX = x
            finalY = y 
                    
        finalX = min(max(finalX, 0), np.shape(self.map)[0])
        finalY = min(max(finalY, 0), np.shape(self.map)[1])
        
        self.agent.setPosition(finalX, finalY)
        self.agent.setVelocity(finalVx, finalVy)
        
        if goalReached == True:
            self.agent.notifyGoalReached()
            
        self.agent.learn()
        
        if goalReached == True:
            self.agent.reset(0, 0)

                    
            