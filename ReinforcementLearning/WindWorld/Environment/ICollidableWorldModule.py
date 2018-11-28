'''
Created on 25 Nov 2018

@author: hoanglong
'''

from abc import ABCMeta, abstractmethod

class ICollidableWorld(object):
    '''
    Just an interface used for ensuring that the agent can know whether a collision has occured
    '''


    def __init__(self, params):
        '''
        Constructor
        '''