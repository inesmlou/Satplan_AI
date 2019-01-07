import random

MaxFlips = 50
MaxRestarts = 10
prob = 0.5

def initSat(sCla):
    global nVar
    global nCla
    lCla = [[]]
    vec = []
    lSat = sCla.split() #split clauses into list
    if lSat[1].lower() != 'cnf':
        #return -1
        pass
    nVar = int(lSat[2])
    nCla = int(lSat[3])
    lSat = list(map(int,lSat[4:-1])) #-1, assuming there's always a '0' at the end. Otherwise, nothing.
#    dVar = dict( [ (i, 0) for i in range(-nVar,nVar+1) ] )
    dVar = dict({0:0})    
    for i in range(nVar+1):
        randbool = 2*random.randrange(0,2)-1
        dVar[i]  =  randbool
        dVar[-i] = -randbool
    #0 is unassigned, -1 is false, 1 is true
    
    j = 0
    for lit in lSat:
        if lit != 0:
            lCla[j].append(lit)
        else:
            lCla.append([])
            j += 1
    return lCla, dVar
    
def satClause(cla, dVar):
    for lit in cla:
        if dVar[lit] == 1:
            return 1
    return -1

def checkSat(lCla, dVar):
    sum = 0
    for cla in lCla:
        check = satClause(cla, dVar)
        if check == -1:
            return -1
        sum += check
    if sum == nCla:
        return 1
    return 0

def randomAssign(lCla, dVar):
    for cla in lCla:
        if satClause(cla, dVar) == -1:
            rand = random.randrange(len(cla))
            return flipAssign(dVar, cla[rand])

# This function counts the occurrences of each variable in unsatisfied clauses, as a choosing heuristic
def greedyAssign(lCla, dVar):
    max = 0
    nOccVar = dict( [ (i, 0) for i in range(-nVar,nVar+1) ] ) #Dict for number of occurrences of a variable
    for cla in lCla:
        if satClause(cla, dVar) == -1:
            for lit in cla:
                nOccVar[lit] += 1

    for lit in range(-nVar,nVar+1):
        if nOccVar[lit] > max:
            max = lit
    return flipAssign(dVar, lit)
    
def flipAssign(dVar, lit):
    dVar[lit]  = -dVar[lit]
    dVar[-lit] = -dVar[-lit]
    return dVar

def restart():
    dVar = dict({0:0})
    for i in range(nVar+1):
        randbool = 2*random.randrange(0,2)-1
        dVar[i]  =  randbool
        dVar[-i] = -randbool
    return dVar

def walkSAT(lCla, dVar):
    global dVarSat
    count  = 0
    count2 = 0
    while checkSat(lCla, dVar) != 1:
        if random.random() < prob:
            dVar = randomAssign(lCla, dVar)
        else:
            dVar = greedyAssign(lCla, dVar)
        count += 1
        if count >= MaxFlips:
            dVar = restart()
            count2 += 1
            count = 0
        if count2 >= MaxRestarts:
            return -1
    dVarSat = dVar
    print(lCla, dVar)
    return 1


def printSat():
    lVarSat = []
    for i in range(nVar):
        if i+1 in dVarSat:
            lVarSat.append((i+1)*dVarSat[i+1])
        else:
            lVarSat.append((i+1))
    return ' '.join(map(str,lVarSat))