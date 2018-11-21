'''
Created on 15 Nov 2018

@author: hoanglong
'''

import Tkinter as tk
import numpy as np
import copy
import threading
import time
class MainWindow(object):
    '''
    main window to display wind world game
    '''


    def __init__(self, map, width = 500, height = 500):
        '''
        Constructor
        '''
        self.top = tk.Tk()
        self.cv = tk.Canvas(self.top, bg="black")
        self.cv.config(width=width, height=height)
        self.prev_mark = 0
        self.prev_markedX = 0
        self.prev_markedY = 0
        self.lock = threading.Lock()
        mapWidth, mapHeight = np.shape(map)
        
        boxWidth = width / mapWidth
        boxHeight = height / mapHeight
        
        for j in range(mapHeight):
            for i in range(mapWidth):
                if map[i,j] == 0:
                    fill = "white"
                elif map[i,j] == 1:
                    fill = "gray"
                elif map[i,j] == 2:
                    fill = "orange"
                else:
                    fill = "black"
                self.cv.create_rectangle(i * boxWidth, j * boxHeight, (i + 1) * boxWidth, (j + 1) * boxHeight, fill=fill)
                
        self.cv.pack()
        self.boxWidth = boxWidth
        self.boxHeight = boxHeight
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.map = map
        self.event = threading.Event()
    
    def getUpdateEvent(self):
        return self.event
        
    def markPosition(self, x, y):
        self.lock.acquire()
        self.map[self.prev_markedX, self.prev_markedY] = self.prev_mark
        self.prev_mark = self.map[x, y]
        self.prev_markedX = x
        self.prev_markedY = y
        self.map[x, y] = 3
        self.lock.release()
        
    def updateMap(self):
        self.lock.acquire()
        for i in range(self.mapWidth):
            for j in range(self.mapHeight):
                if self.map[i, j] == 3:
                    self.cv.create_oval(i * self.boxWidth, j * self.boxHeight, (i + 1) * self.boxWidth, (j + 1) * self.boxHeight, fill="black")
                else:
                    if self.map[i,j] == 0:
                        fill = "white"
                    elif self.map[i,j] == 1:
                        fill = "gray"
                    elif self.map[i,j] == 2:
                        fill = "orange"
                    else:
                        fill = "black"
                    self.cv.create_rectangle(i * self.boxWidth, j * self.boxHeight, (i + 1) * self.boxWidth, (j + 1) * self.boxHeight, fill=fill)
         
        self.lock.release()       
       
    def getMap(self):
        return copy.deepcopy(self.map)
     
    def start(self):
        '''
        run the gui
        '''
        self.stopProg = False
        self.pauseProg = False
        
        while (self.stopProg == False):
            while (self.pauseProg == False and self.stopProg == False):   
                self.updateMap()
                self.top.update_idletasks()
                self.top.update()
                self.event.set()
            if (self.pauseProg == True):
                time.sleep(1)
        
    def pause(self):
        self.pauseProg = True
        
    def resume(self):
        self.pauseProg = False
        
    def stop(self):
        self.stopProg = True