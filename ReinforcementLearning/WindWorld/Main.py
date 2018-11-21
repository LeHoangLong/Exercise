'''
Created on 15 Nov 2018

@author: hoanglong
'''

import Environment.MapModule as MapModule
import Environment.AgentModule as AgenModule
import GUI.MainWindowModule as MainWindowModule
import threading
import numpy as np
import Environment.WorldModule as WorldModule
import  os
import time


def console():
    global rec
    global wd
    global step
    global agent
    while (True):
        a = raw_input("s: step record, p: pause, c: continuous record")
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
    agent = w.getAgent()
    wd.markPosition(agent.getPosition()[0], agent.getPosition()[1])
    event = wd.getUpdateEvent()
    stepCount = 0
    while(True):
        if step == True:
            raw_input("Press enter to continue\n")
        w.timeStep()
        wd.markPosition(agent.getPosition()[0], agent.getPosition()[1])
        if rec == True:
            event.wait()
            event.clear()
        print("step: " + str(stepCount) + "\n")
        stepCount += 1

if __name__ == '__main__':
    rec = True
    step = False
    sem0 = threading.Semaphore(0)
    sem1 = threading.Semaphore(1)
    m = MapModule.Map()
    wd = MainWindowModule.MainWindow(m.getMap(), height = 600, width = 600)
    wdMap = wd.getMap()
    w = WorldModule.World(m.getMap())
    agent = w.getAgent()
    gameThread = threading.Thread(target=game)
    console = threading.Thread(target=console)
    console.start()
    gameThread.start()
    
    wd.start()
    
