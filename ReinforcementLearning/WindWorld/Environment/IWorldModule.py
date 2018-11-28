'''
Created on 24 Nov 2018

@author: hoanglong
'''

from abc import ABC, abstractmethod

class IWorld(ABC):
    '''
    World interface
    handle game physics
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    @abstractmethod
    def act(self, agent):
        '''
        react to the agent based on its current states and actions
        '''
        pass
    
        
    @abstractmethod
    def setGoal(self, agent):
        '''
        set goal for the agent for simpler learning. We don't want to get invovled in path finding algorithm.
        Of course, if desired, the agent can simple ignore whatever the environment sets here
        '''
        pass