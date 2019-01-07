from copy import deepcopy

#sCla = 'p cnf 3 3 -1 0 2 0 3 0'
#sCla = 'p cnf 16 18 1 2  0 -2   -4  0  3    4  0 -4   -5  0  5   -6  0  6   -7  0  6    7  0  7  -16  0  8   -9  0 -8  -14  0  9   10  0  9  -10  0 -10  -11  0 10   12  0 11   12  0 13   14  0 14  -15  0 15   16'
nVar = 0 # Number of variables
nCla = 0 # Number of clauses
dVarSat = None

def initSat(sCla):
    global lCla
    global nVar
    global nCla
    lCla = [[]]
    lSat = sCla.split() #split clauses into list
    if lSat[1].lower() != 'cnf':
        #return -1
        pass
    nVar = int(lSat[2])
    nCla = int(lSat[3])
    lSat = list(map(int,lSat[4:-1])) #-1, assuming there's always a '0' at the end. Otherwise, nothing.
    #dVar = dict( [ (i, 0) for i in range(-nVar,nVar+1) ] )
    dVar = dict({0:0}) #initialize dict of variables
    #0 is unassigned, -1 is false, 1 is true
    
    j = 0
    for lit in lSat:
        if lit != 0:
            lCla[j].append(lit)
        else:
            lCla.append([])
            j += 1
    return dVar
    #lCla will remain a global variable to be accessed from other functions

def satClause(cla, dVar):
    sum = 0
    for lit in cla:
        if lit in dVar:
            if dVar[lit] == 1:
                return 1
            sum += dVar[lit]
    if sum == -len(cla): #Check if all literals are false
        return -1
    return 0
    
def checkSat(dVar):
    sum = 0
    for cla in lCla:
        check = satClause(cla, dVar)
        if check == -1:
            return -1
        sum += check
    if sum == nCla:
        return 1
    return 0


def setUnit(dVar):
    flag = 0
    for cla in lCla:
        nUnVar = 0 # Number of unassigned variables
        for lit in cla:
            if lit in dVar:
                if dVar[lit] == 1:
                    break
            else:
                nUnVar += 1 #Increments for every non-assigned literal
                unitLit = lit
        else:
            if nUnVar == 1: #If there is only one unassigned literal, assign it
                assignLit(unitLit, 1, dVar)
                flag = 1
    return flag
                
def setPure(dVar):
    flag = 0
    nOccVar = dict( [ (i, 0) for i in range(-nVar,nVar+1) ] ) #Dict for number of occurrences of a variable
    for cla in lCla:
        for lit in cla:
            if lit in dVar:
                if dVar[lit] == 1:
                    break # Do not add occurrences if clause is already true
        else: # for exhausted = clause not yet true
            for lit in cla:
                if lit not in dVar: #add for each non-occurrence
                    nOccVar[lit] += 1

    for lit in range(-nVar, nVar+1):
        if nOccVar[-lit] != 0:
            continue
        if nOccVar[lit]:
            assignLit(lit, 1, dVar)
            flag = 1
            
    return flag

def assignLit(lit, val, dVar):
    dVar[lit]  =  val
    dVar[-lit] = -val

def linearAssign(dVar, val):
    for i in range(nVar+1):
        if i not in dVar:
            assignLit(i, val, dVar)
            return #i

def DPLL(dVar):
    global dVarSat
    check = checkSat(dVar)
    if check != 0:
        if check == 1:
            dVarSat = dVar
        return check
    while(setPure(dVar)):
        pass
    while(setUnit(dVar)):
        pass

    dVar1 = deepcopy(dVar)
    dVar2 = deepcopy(dVar)
    linearAssign(dVar1,  1)
    linearAssign(dVar2, -1)
    return (DPLL(dVar1) == 1) | (DPLL(dVar2) == 1)
#
#def printSat():
#    for i in range(nVar):
#        if i+1 in dVarSat:
#            print((i+1)*dVarSat[i+1])
#        else:
#            print((i+1)*-1, 'unAss')
    
        
def printSat():
    lVarSat = []
    for i in range(nVar):
        if i+1 in dVarSat:
            #print((i+1)*dVarSat[i+1])
            lVarSat.append((i+1)*dVarSat[i+1])
        else:
            #print((i+1)*-1, 'unAss')
            lVarSat.append((i+1)*-1)
    return ' '.join(map(str,lVarSat))