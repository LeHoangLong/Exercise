'''
Created on 14 Nov 2018


@author: hoanglong
'''

import numpy as np
import copy

class MapGenerator(object):
    '''
    generate map
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.isBlank = False
        if self.loadMap() == False:
            self.generateBlankMap()
        
    def addObject(self, pos, val):
        '''
        Take in a list of tuples (x, y) and assign val to the corresponding coordinate
        '''
        for i in range(len(pos)):
            x, y = pos[i]
            if x >= 0 and x < self.width and y >= 0 and y < self.height:
                self.map[x, y] = val
        self.saveMap()
        
    def addStraightBlocks(self, coordinates, val):
        '''
        Take a list of 4-element tuple (x1, y1, x2, y2) and create a straight block from (x1, y1) to (x2, y2) with value of val
        '''
        for i in range(len(coordinates)):
            x1, y1, x2, y2 = coordinates[i]
            if x1 >= 0 and x1 < self.width and y1 >= 0 and y1 < self.height and \
                x2 >= 0 and x2 < self.width and y2 >= 0 and y2 < self.height:
                    if y2 != y1:
                        tan = (x2 - x1) * 1.0 / (y2 - y1) #oops
                        for j in range(y2 - y1 + 1):
                            self.map[np.round(x1 + j * tan), y1 + j] = val
                    elif x2 !=  x1:
                        cot = (y2 - y1) * 1.0 / (x2 - x1) #oops
                        for j in range(x2 - x1 + 1):
                            self.map[x1 + j, np.round(y1 + j * cot)] = val
                    else:
                        self.map[x1, y1] = val
        self.saveMap()
            
        
    def generateBlankMap(self, width = 30, height = 30):
        '''
        generate map with no objects
        '''
        self.map = np.zeros((height, width), np.int32)
        self.width = width
        self.height = height
        self.saveMap()
        self.isBlank = True
       
    def checkBlankMap(self):
        return self.isBlank         
        
    
    def saveMap(self):
        '''
        persist map into a map file
        '''
        
        f = open("map", "w")
        
        f.write(str(self.width) + " " + str(self.height) + "\n")
        
        for j in range(self.height):
            for i in range(self.width):
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
            
            self.width, self.height = np.shape(self.map)
            return True
        except (IOError):
            return False
                
    def getMap(self):
        return self.map
        