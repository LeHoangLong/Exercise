'''
Created on 25 Nov 2018

@author: hoanglong
'''
from abc import ABC, abstractmethod
import pickle

class IAgent(ABC):
    '''
    Interface for agents
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    @abstractmethod
    def act(self):
        '''
        perform 1 action and then invoke a reaction from world
        '''
        pass
    
    @abstractmethod
    def getStates(self):
        '''
        return a tuple of current states of the agent
        '''
        pass
    
    @abstractmethod
    def setStates(self, states):
        '''
        set the next state of the agent (for World module to use)
        '''
        pass
    
    @abstractmethod
    def setGoal(self, goal):
        '''
        set the goal of the agent. Can take in multiple goals
        '''
        pass
    
    def _protected_save(self, filename, obj):
        '''
        save the value of obj of the agent into filename file
        '''
        dst = open(filename, "wb")
        pickle.dump(obj, dst)
        pass
    
    def _protected_load(self, filename, dst):
        '''
        load the previously saved value of obj into dst from filename file
        throws IOError if file not found
        '''
        try:
            src = open(filename, "rb")
            dst = pickle.load(src)
        except (IOError):
            raise IOError
        