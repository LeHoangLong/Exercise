import Track as tr
import numpy as np
from threading import Thread

printPos = False


def toPrint():
    while (1):
        global printPos
        a = raw_input("input: ")
        if a == "y":
            printPos = True
        elif a == "n":
            printPos = False

thread = Thread(target = toPrint)
thread.start()

track = tr.Track()
shape = list(track.getTrackShape())
shape.append(7)
shape.append(7)
counter = np.zeros(shape)
shape.append(2)
pi = np.random.randint(-1, 2, shape)

shape = list(track.getTrackShape())
shape.append(7)
shape.append(7)
shape.append(3)
shape.append(3)

gamma = 1


Q = np.random.randint(-8000, -5000, shape) / 1000.0
C = np.zeros(shape)


number_of_actions = np.size(Q, -1) * np.size(Q, -2)

trajectory = []

        
epsilon = 0.5
threshold = 20
count = 0
counter00 = 0
episodes = 0

while True:
    episodes += 1
    reset = False
    print("epsiode: " + str(episodes))
    if len(trajectory) == 0 or len(trajectory) > 200000:
        track.initializePosition()
        trajectory = []
    else:
        lastPos = (trajectory[-1][0][0], trajectory[-1][0][1])
        lastVel = (trajectory[-1][0][2], trajectory[-1][0][3])
        track.setPositionAndVelocity(lastPos, lastVel)
        track.disableMove()
        
    #--------------------------------------------- if counter[0, 0, 0, 0] >= 10:
        #------------------------------------------------------- trajectory = []
        #---------------------------------------------------------- pos = [0, 0]
        #---------------------------------------------------------- vel = [0, 0]
        #-------------------------------- track.setPositionAndVelocity(pos, vel)
        #--------------------------------------------------- track.disableMove()
        #------------------------------------------------------- printPos = True
    
    count = 0
    ret = 0
    lose = 0
    while (ret != 2):
        if ret == 1:
            lose = 1
            break
        track.enableMove()
        dice = np.random.rand()
        velocity = track.getVelocity()
        pos = track.getPosition()
        a = pi[pos[0], pos[1], velocity[0], velocity[1]][0]
        b = pi[pos[0], pos[1], velocity[0], velocity[1]][1]
        c = Q[pos[0], pos[1], velocity[0], velocity[1], a, b]
        if counter[pos[0], pos[1], velocity[0], velocity[1]] >= threshold:
            epsilon = 0.05
        else:
            epsilon = 1.0
        if dice > epsilon:
            action = tuple((a, b))
        else:
            action = tuple((np.random.randint(-1, 2), np.random.randint(-1, 2)))
        #-- action = tuple((np.random.randint(-1, 2), np.random.randint(-1, 2)))
        trajectory.append(((track.getPosition()[0], track.getPosition()[1], velocity[0], velocity[1]), action))
        count += 1
        track.increaseVelocity(action)
        #-------------------------------------------------- if printPos == True:
            #------------------------------------------- track.printCurrentPos()
        ret = track.move()
        
    G = 0
    W = 1
    reset = True
    for i, t in enumerate(reversed(trajectory)):
        counter00 = 0
        if i == 0:
            lastPos = (trajectory[-1][0][0], trajectory[-1][0][1])
            lastVel = (trajectory[-1][0][2], trajectory[-1][0][3])
            lastAction = (trajectory[-1][1][0], trajectory[-1][1][1])
            if lose == 1:
                G = -10
            else:
                G = 1000
        else:
            G = gamma * G - 5
        prev_optimal_action = pi[t[0][0], t[0][1], t[0][2], t[0][3]]
        
        
        if counter[t[0][0], t[0][1], t[0][2], t[0][3]] >= threshold:
            epsilon = 0.05
        else:
            epsilon = 1.0
            
        temp = epsilon / number_of_actions
    
        if t[1][0] == prev_optimal_action[0] and t[1][1] == prev_optimal_action[1]:
            W = W / (1 - epsilon + temp)
        else:
            W = W / temp
        #---------------------------------------------------------- W = W / temp
        tempQ = Q[int(t[0][0]), int(t[0][1]), int(t[0][2]), int(t[0][3]), int(t[1][0]) + 1, int(t[1][1]) + 1]
        tempC = C[int(t[0][0]), int(t[0][1]), int(t[0][2]), int(t[0][3]), int(t[1][0]) + 1, int(t[1][1]) + 1]
        
        tempC += W
        tempQ += W / tempC * (G - tempQ)
        C[int(t[0][0]), int(t[0][1]), int(t[0][2]), int(t[0][3]), int(t[1][0]) + 1, int(t[1][1]) + 1] = tempC
        Q[int(t[0][0]), int(t[0][1]), int(t[0][2]), int(t[0][3]), int(t[1][0]) + 1, int(t[1][1]) + 1] = tempQ
        
        temp1 = Q[int(t[0][0]), int(t[0][1]), int(t[0][2]), int(t[0][3])]
        next_action = np.argmax(temp1)
        pi[t[0][0], t[0][1], t[0][2], t[0][3]][0] = (next_action ) / 3 - 1
        pi[t[0][0], t[0][1], t[0][2], t[0][3]][1] = (next_action ) % 3 - 1
        a = t[1][0]
        b = t[1][1]
        c = pi[t[0][0], t[0][1], t[0][2], t[0][3]][0]
        d = pi[t[0][0], t[0][1], t[0][2], t[0][3]][1]
        
        counter[t[0][0], t[0][1], t[0][2], t[0][3]] += 1
        
        
        posX = t[0][0]
        posY = t[0][1]
        velX = t[0][2]
        velY = t[0][3]
        co = counter[t[0][0], t[0][1], t[0][2], t[0][3]]
        
        if t[0][0] == 0 and t[0][1] == 0 and t[0][2] == 0 and t[0][3] == 0:
            if reset == True:
                counter00 = 0
                reset = False
            else:
                counter00 += 1
        trajectory.pop()
        if (c != a) or (d != b):
            break
    
    if printPos == True:
        track.initializePosition()
        count = 0
        
        while (track.move() != 2 and count < 50):
            velocity = track.getVelocity()
            position = track.getPosition()
            action = pi[position[0], position[1], velocity[0], velocity[1]]
            track.increaseVelocity(action)
            track.printCurrentPos()
            count += 1
            
            
#------------------------------------------------------------------------------ 
    #------------------------------------------------------ if printPos == True:
        #--------------------------------------------------------- while (True):
            #---------------------------------------- track.initializePosition()
            #---------------------------------------- while (track.move() != 2):
                #-------------------------------- velocity = track.getVelocity()
                #-------------------------------- position = track.getPosition()
                # action = pi[position[0], position[1], velocity[0], velocity[1]]
                #-------------------------------- track.increaseVelocity(action)
                #--------------------------------------- track.printCurrentPos()
    