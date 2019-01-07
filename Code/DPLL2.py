from copy import deepcopy

def initSat(sCla):
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
    dVar = dict({0:0}) #initialize dict of variables
    #0 is unassigned, -1 is false, 1 is true
    
    j = 0
    for lit in lSat:
        if lit != 0:
            lCla[j].append(lit)
        else:
            lCla.append([])
            j += 1
    return lCla, dVar

def setUnit(lCla, dVar):
    flag = 0
    for ind, cla in enumerate(lCla):
        if len(cla) == 1:
            assignLit(cla[0], lCla, dVar, 1)
            flag = 1
    return flag
            
def setPure(lCla, dVar):
    flag = 0
    nOccVar = dict( [ (i, 0) for i in range(-nVar,nVar+1) ] ) #Dict for number of occurrences of a variable
    for cla in lCla:
        for lit in cla:
            nOccVar[lit] += 1

    for lit in range(-nVar, nVar+1):
        if nOccVar[-lit] != 0:
            continue
        if nOccVar[lit]:
            assignLit(lit, lCla, dVar, 1)
            flag = 1

    return flag

def assignLit(lit_set, lCla, dVar, val):
    dVar[lit_set]  =  val
    dVar[-lit_set] = -val
    fl = 1
    while fl:
        fl = 0
        aux1 = 0
        for ind1, cla in enumerate(lCla[aux1:]):
            if fl:
                break
            for ind2, lit in enumerate(cla):
                if lit == lit_set:
                    fl = 1
                    if val == -1: #If variable is false, only remove it from clause
                        cla.pop(ind2)
                        aux1 = ind1
                        break
                    if val == 1: #If variable is true, remove clause as it is satisfied
                        lCla.pop(ind1)
                        aux1 = ind1
                        break
                if lit == -lit_set: #If variable is negated, the reverse happens
                    fl = 1
                    if val == -1:
                        lCla.pop(ind1)
                        aux1 = ind1
                        break
                    if val == 1:
                        cla.pop(ind2)
                        aux1 = ind1
                        break

def linearAssign(lCla, dVar, val):
    for lit in range(nVar+1):
        if lit not in dVar:
            assignLit(lit, lCla, dVar, val)
            return
            
def DLISAssign(lCla, dVar, val):
    max = 0
    nOccVar = dict( [ (i, 0) for i in range(-nVar,nVar+1) ] ) #Dict for number of occurrences of a variable
    for cla in lCla:
        for lit in cla:
            nOccVar[lit] += 1
    for lit in range(-nVar,nVar+1):
        if nOccVar[lit] > max:
            max = lit
    
    assignLit(max, lCla, dVar, val)
    

def checkSat(lCla):
    if lCla == []: # sentence is true if all clauses were removed
        return 1
    for cla in lCla:
        if cla == []: # sentence is false if an empty clause is found (all lits were false in this clause)
            return -1
    return 0


def DPLL(lCla, dVar):
    global dVarSat
    check = checkSat(lCla)
    if check != 0:
        if check == 1:
            dVarSat = dVar
        return check
    
#    setUnit(lCla, dVar)
#    setPure(lCla, dVar)
    while(setUnit(lCla, dVar)): # Propagate unit symbols, only stopping when there are no unit clauses left
        pass
    while(setPure(lCla, dVar)): # Find all pure symbols
        pass

    dVar1 = deepcopy(dVar)
    lCla1 = deepcopy(lCla)
    dVar2 = deepcopy(dVar)
    lCla2 = deepcopy(lCla)
#    linearAssign(lCla1, dVar1,  1)
#    linearAssign(lCla2, dVar2, -1)
    DLISAssign(lCla1, dVar1,  1)
    DLISAssign(lCla2, dVar2, -1)
    return (DPLL(lCla1, dVar1) == 1) | (DPLL(lCla2, dVar2) == 1)
        
def printSat():
    lVarSat = []
    for i in range(nVar):
        if i+1 in dVarSat:
            lVarSat.append((i+1)*dVarSat[i+1])
        else:
            lVarSat.append((i+1))
    return ' '.join(map(str,lVarSat))