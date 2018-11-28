'''
Created on 22 Nov 2018

@author: hoanglong
'''

from abc import ABC, abstractmethod

class IWorldMap(ABC):
    '''
    WorldMap interface, used to abstract map implementation from WorldModule
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    @abstractmethod
    def generateMap(self, height=30, width=30):
        pass
    
    @abstractmethod
    def isObstacle(self, x, y):
        pass

    @abstractmethod
    def isGoal(self):
        pass

    @abstractmethod
    def isPath(self, x, y):
        '''
        return True if agent can move to position x, y
        '''
        pass
    
    @abstractmethod
    def getMapSize(self):
        pass
    
    @abstractmethod
    def markPositionTemporarily(self, x, y, val): 
        '''
        mark position with val
        The marked value is not persistent
        '''
        pass   
    
    @abstractmethod
    def unmark(self, x, y):
        '''
        return map to the original value
        '''
        pass
    
    @abstractmethod
    def isMark(self, x, y, val):
        '''
        return true if position x, y was marked with val
        '''
        pass