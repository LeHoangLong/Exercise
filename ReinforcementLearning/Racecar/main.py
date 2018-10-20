import Track as tr
import numpy as np


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

gamma = 0.9


Q = np.random.randint(-8000, -5000, shape) / 1000.0
C = np.zeros(shape)


number_of_actions = np.size(Q, -1) * np.size(Q, -2)

trajectory = []

        
epsilon = 1.0
threshold = 20
count = 0
for episodes in range(5000):
    trajectory = []
    print("epsiode: " + str(episodes))
    track.initializePosition()
    count = 0
    while (track.move() == False):
        dice = np.random.rand()
        velocity = track.getVelocity()
        pos = track.getPosition()
        if counter[pos[0], pos[1], velocity[0], velocity[1]] >= threshold:
            epsilon = 0.05
        else:
            epsilon = 1.0
        if dice > epsilon:
            action = tuple((pi[pos[0], pos[1], velocity[0], velocity[1]][0], pi[pos[0], pos[1], velocity[0], velocity[1]][1]))
        else:
            action = tuple((np.random.randint(-1, 2), np.random.randint(-1, 2)))
        #-- action = tuple((np.random.randint(-1, 2), np.random.randint(-1, 2)))
        trajectory.append(((track.getPosition()[0], track.getPosition()[1], velocity[0], velocity[1]), action))
        count += 1
        track.increaseVelocity(action)
        
    G = 0
    W = 1
    for i, t in enumerate(reversed(trajectory)):
        G = gamma * G - 1
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
        Q[int(t[0][0]), int(t[0][1]), int(t[0][2]), int(t[0][3]), int(t[1][0]) + 1, int(t[1][1]) + 1] = tempQ
        
        temp1 = Q[int(t[0][0]), int(t[0][1]), int(t[0][2]), int(t[0][3])]
        next_action = np.argmax(temp1)
        pi[t[0][0], t[0][1], t[0][2], t[0][3]][0] = next_action % 3 - 1
        pi[t[0][0], t[0][1], t[0][2], t[0][3]][1] = next_action / 3 - 1
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
        if (c != a) or (d != b):
            break
    
    if episodes % 100 == 0 and episodes > 0 or episodes == 100:
        track.initializePosition()
        count = 0
        while (track.move() == False and count < 30):
            velocity = track.getVelocity()
            position = track.getPosition()
            action = pi[position[0], position[1], velocity[0], velocity[1]]
            track.increaseVelocity(action)
            track.printCurrentPos() 
            count += 1
    
while (track.move() == False):
    velocity = track.getVelocity()
    position = track.getPosition()
    action = pi[position[0], position[1], velocity[0], velocity[1]]
    track.increaseVelocity(action)
    track.printCurrentPos()       