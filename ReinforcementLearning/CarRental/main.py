import numpy as np;

numberOfStates = 11


def possion(lamd, n):
    return np.power(lamd, n) * np.exp(-lamd) / np.math.factorial(n)

def pNextState(s, a, lambd):
    #compute the poisson probabilty of cars rented out
    c1, c2 = s
    c1 = c1 - a
    c2 = c2 + a
    p1_rented = 0
    lambd1_rent, lambd1_return, labmd2_rent, lambd2_return = lambd
    pNext = np.zeros((c1 + c2 + 1, numberOfStates, numberOfStates))
    cum1 = 0
    cum2 = 0
    for i in range(c1+1):
        p1_rented = possion(lambd1_rent, i)
        cum1 = 0
        for j in range(numberOfStates - 1 - c1 + i + 1):
            if j == (numberOfStates - 1 - c1 + i):
                p1_returned = 1 - cum1
            else: 
                p1_returned = possion(lambd1_return, j)
                cum1 = cum1 + p1_returned
            for m in range(c2+1):
                p2_rented = possion(labmd2_rent, m)
                cum2 = 0
                for n in range(numberOfStates - 1 - c2 + m):
                    if n == (numberOfStates - 1 - c2 + m):
                        p2_returned = 1 - cum2
                    else:    
                        p2_returned = possion(lambd2_return, n)
                        cum2 = cum2 + p2_returned
                    c1_next = c1 - i + j
                    c2_next = c2 - m + n
                    pNext[i+m, c1_next, c2_next] += p1_rented * p1_returned * p2_rented * p2_returned
    return pNext

def getActionValue(p, state_value, discount):
    value = 0
    for reward in range(np.size(p, 0)):
        for i in range(np.size(p, 1)):
            for j in range(np.size(p, 2)):
                value += p[reward, i, j] * ( reward  + discount * state_value[i, j] ) 
    return value


#initialization
value = np.full((numberOfStates, numberOfStates), 0)
policy = np.zeros(((numberOfStates, numberOfStates)))
policy = policy / np.size(policy, 0)
action_value = np.zeros((11, numberOfStates, numberOfStates))

lambd = [3, 3, 4, 2]

stable = False

print("Start")
iteration = 0
while (stable == False):
    print("iteration: " + str(iteration) + "\n")
    iteration += 1
    #evaluation
    delta = np.full(np.shape(value), 10)
    while (np.max(np.abs(delta)) > 0.1):
        value_prev = value
        value = np.zeros(np.shape(value_prev))
        for i in range(np.size(value, 0)):
            for j in range(np.size(value, 1)):
                for k in range(np.size(action_value, 0)):
                    a = k - np.size(policy, 0) / 2
                    s = [i, j]
                    action_value[k, i, j] = getActionValue(pNextState(s, a, lambd), value_prev, 0.9)    
                pi_a = policy[i, j]
                value[i, j] = action_value[pi_a, i, j]
        delta = value - value_prev
        
    #improvement
    stable = True
    for i in range(np.size(value, 0)):
        for j in range(np.size(value, 1)):
            action_value_prev = action_value[i, j]
            policy[i, j] =  np.argmax(action_value[:, i, j])
            action_value_now = action_value[policy[i, j], i, j]
            if (max(np.abs(action_value_prev - action_value_now)) > 0.1):
                stable = False

print("done")
input(a)        
                
            
            
            
            
            
        
        


                
                
                