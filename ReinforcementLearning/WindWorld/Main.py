'''
Created on 15 Nov 2018

@author: hoanglong
'''

import Environment.MapGeneratorModule as MapModule
import LearningAgent.AgentModule as am
import GUI.MainWindowModule as MainWindowModule
import threading
import numpy as np
import Environment.SimpleWorldModule as WorldModule
import Environment.SimpleWorldMap as WorldMapModule
import  os
import time


def console():
    global rec
    global wd
    global step
    global agent
    while (True):
        a = input("s: step record, p: pause, c: continuous record ")
        if a == "p":
            rec = False
            wd.pause()
        elif a == "c":
            rec = True
            step = False
            wd.resume()
        elif a == "step":
            rec = True
            step = True
            wd.resume()
        elif a == "save":
            agent.saveQ()
            
        
def game():
    global w
    global step
    global wd
    global rec
    global agent
    x = agent.getStates()[0]
    y = agent.getStates()[1]
    
    wd.markPosition(x, y)
    event = wd.getUpdateEvent()
    stepCount = 0
    while(True):
        if step == True:
            input("Press enter to continue\n")
        agent.act()
        x = agent.getStates()[0]
        y = agent.getStates()[1]
    
        wd.markPosition(x, y)
        if rec == True:
            event.wait()
            event.clear()
        print("step: " + str(stepCount) + "\n")
        stepCount += 1
        agent.learn()

if __name__ == '__main__':
    rec = True
    step = False
    sem0 = threading.Semaphore(0)
    sem1 = threading.Semaphore(1)
    m = WorldMapModule.SimpleWorldMap()
    wd = MainWindowModule.MainWindow(m, height = 600, width = 600)
    w = WorldModule.SimpleWorld(m)
    maxStates = w.getLimitOfStates()
    agent = am.SimpleAgent(w)
    gameThread = threading.Thread(target=game)
    console = threading.Thread(target=console)
    console.start()
    gameThread.start()
    
    wd.start()
    
