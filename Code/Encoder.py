#############################################################
#                    Authors:                               #
#               Christopher Edgley  75258                   #
#               Inês Lourenço       75637                   #
#############################################################

import re
import itertools
import EncoderUtils

##########################################################################
## 1. INITIAL STATE
##########################################################################

# Função que abre o ficheiro e trata da informação
def initPlan(argv):
    
    global sentence
    sentence=[]
    
    #Função que guarda os dados do ficheiro
    allLines, initState, goalState, aLine = EncoderUtils.saveVariables(argv)

    # Save all constants
    parenthesis = re.findall('\(.*?\)', str(allLines))
    parenthesis = re.sub('[()]', ' ', str(parenthesis))
    wordList = re.sub("[^\w]", " ", parenthesis).split()
    
    constants = []
    for word in wordList:
        if word[0].isupper():
            for const in constants:
                if const == word:               
                    break
            else:
                constants.append(word)                  

    # Save all predicates and actions
    atoms=[]
    actions=[]
    actName=[]
    frameLength = []
    for acti in aLine:
        
        # Para as ACTIONS
    #   actions = [[name, [preconds], [effects]], [...]]
        preconds = re.findall(r'\: (.*?)\ -> ',acti)
        preconds=''.join(map(str, preconds)).split(' ')
        frameLength.append(len(preconds))
        effects = re.findall(r'\-> (.*)',acti)
        effects = ''.join(map(str, effects)).split(' ')
        acti = ''.join(map(str, acti)).split(' ')
        actName.append(acti[1])
        actions.append([[acti[1]], preconds, effects])

        # Para os PREDICATES
        actios = acti[3:len(acti)] + initState + goalState
        for actPred in actios:

            if actPred[0]=='-':                         #Elimina a negação
                actPred = actPred[1:len(actPred)]
            if actPred[0].islower():                 # se calhar pode ser tirada a condição
                atom = re.findall(r'(.*?)\(.*?\)', actPred)
                for pred in atoms:                              # PREDICATES
                    atom2 = re.findall(r'(.*?)\(.*?\)', pred)
                    if atom2 == atom:               
                        break
                else:
                    atoms.append(actPred)
            #else não faz nada
    initialState, atomListComb = EncoderUtils.organizeVariables(atoms, initState, constants)
    
    return actName, initialState, goalState, constants, actions, atoms, atomListComb


##########################################################################

# cria os frameAxioms e passa as actions para CNF
def findEffects (at, count, actListComb, frameAxioms, actionsCNF, t):
 
    for acoes in actListComb:

        for comb in acoes:

            for preEFF in comb[1:]:
                
                ########################################################
                # 4 Actions to CNF - Only does this one time, to create the actions in CNF
                
                if count== 0:
                    actionsCNF.extend(['-'+comb[0], preEFF, 0])     # o "0" no fim é para ficar já no SAT format 
                ########################################################
                    
                if preEFF[-1] == str(t):  
                   
                    if preEFF[0] == '-':
                        if at == preEFF[1:-1]:
                            break
                    else:
                        if preEFF[:-1] == at:
                            break
            # se nunca fez break é porque para esse atomo não encontrou nenhum effect.
#           # logo tem que adicionar às frameAxioms
            else:
                frameAxioms.extend([at+str(t-1), '-'+comb[0], '-'+at+str(t), 0])    # o "0" no fim é para ficar já no SAT format
                frameAxioms.extend(['-'+at+str(t-1), '-'+comb[0], at+str(t), 0])
#                            
    return [frameAxioms, actionsCNF]        


        
###################################################################################################
    
# converte as frases para o formato desejado dar ao solver
def convertToSAT(sentence):
    SATsent=''
    SATvariables = []
    if sentence[0][0] == '-':
        SATvariables.append(sentence[0])
    else:
        SATvariables.append(sentence[0])
    #    
    nCla = 0        # number of clauses
    for sat in sentence:
        if sat == 0:
            nCla += 1
            SATsent = SATsent + '0 '
            
        else:
            for var in SATvariables:
                if var == sat:
                    SATsent = SATsent + str(SATvariables.index(var)+1) + ' '
                    break
                elif sat == '-'+var:
                    SATsent = SATsent + str(-(SATvariables.index(var)+1)) + ' '
                    break
            else:
                if sat[0] == '-':
                    SATvariables.append(sat[1:len(sat)])
                    SATsent = SATsent + str(-len(SATvariables)) + ' '
                    continue
                else:
                    SATvariables.append(sat)
                    SATsent = SATsent + str(len(SATvariables)) + ' '
                    continue
                
    return SATsent, SATvariables, nCla
    
#########################################################################

#trata do encoding de todo o algoritmo
def encode(plan, t):
    global sentence
    
    # 1. Define o initial space com os atomos verdadeiros e os falsos
    actName, initialState, goalState, constants, actions, atoms, atomListComb = plan
    SATinitial = EncoderUtils.SATformat(initialState)
    
    # 2. Define o goal, com o respectivo t
    goalState = EncoderUtils.setHorizon(goalState, t)
    SATgoal = EncoderUtils.SATformat(goalState)
    
    # 3. Cria a lista com todas as acções, grounded
    actListComb = EncoderUtils.defineActions(actions, constants, t)

    # 4.  Exactly one action at each time step
    atLeastOne = []
    for eachAction in actListComb:
        for eachComb in eachAction:
            atLeastOne.append(eachComb[0])
    
    atMostOne=[]           
    for ac in itertools.combinations(atLeastOne, 2):  
        ac1 = list(ac)
        ac1[0] = '-'+ac1[0]
        ac1[1] = '-'+ac1[1]
        ac1.append(0)
        atMostOne.extend(ac1)    
    atLeastOne.append(0)
    
    # 5. Cria os frame axioms e converte a lista das acções já grounded para CNF
    frameAxioms=[]
    count=0
    actionsCNF=[]  
    for at in atomListComb:
        [frameAxioms, actionsCNF] = findEffects(at, count, actListComb, frameAxioms, actionsCNF, t)
        count=count+1


    ###########################################################################
    #################################### SAT FORMAT ###########################
    # A sentence é: initialState ^goalState ^actions^frameAxioms^atmost/least
    # Cria a sentence final, juntando todas as partes em cima indicadas

    sentence = sentence + actionsCNF + frameAxioms + atLeastOne + atMostOne 
    
    ##########################################################################
    # Converte para números para dar ao solver
    
    SATsent, SATvariables, nCla = convertToSAT(SATinitial + sentence + SATgoal)

    sCla= 'p cnf ' + str(len(SATvariables)) + ' ' + str(nCla) + ' ' + SATsent
       
    return sCla, SATvariables
    
    
##################################################################################################################################################

# recebe a atribuição de valores true e falso e converte de volta para acções
def decode(sVarSat, actName, SATvariables, t):
    
    # Não deveria acontecer
    if sVarSat == 'UNSAT':
        return 'UNSAT'
        
    result = sVarSat.split()
    
#    encontra o nome das acções existentes
    actionName = []
    for name in actName:
        actionName.extend(re.findall(r'(.*?)\(.*?\)', name))
                
    finalAssignment = [0]*t        
    
    # percorre todo o resultado
    for index, res in enumerate(result):

        if res[0] != '-':        # Só interessam as positivas
            
            for name2 in actionName:
                
                varIsAct = re.findall(r'(.*?)\(.*?\)', SATvariables[index])
                # se for uma acção, e o assignment tiver sido positivo, então faz parte da solução
                if varIsAct[0] == name2:
                    
                    for final in finalAssignment:   
                        # junta à solução, na posição correspondente ao respectivo instante em que ocorre
                        finalAssignment[int(SATvariables[index][-1])] = SATvariables[index][:-1]
                        break
    
    # converte a resposta para o formato desejado e imprime                
    answer=''               
    for sol in finalAssignment:
        s = re.findall(r'(.*?)\(.*?\)', sol)
        
        answer = s[0]
        rest = EncoderUtils.getVariables(sol)
        for variab in rest:
            answer = answer+ ' ' + variab
        print(answer)
    return answer

#########################################################################



