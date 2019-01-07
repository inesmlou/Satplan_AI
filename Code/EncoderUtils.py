import re
import itertools


# introduz o t desejado na expressão, consoante o t actual
def setHorizon(expression, t):
    if isinstance(expression, str):   
        newExpression = re.sub(r'\)',')'+str(t) ,expression)
        return newExpression
    else:
        newExpression = []
    
        for exp in expression:
            exp = exp + str(t)
            newExpression.append(exp)
        return newExpression
 
 
#####################################################################
#                           INIT PLAN
def openFile(arg):   
    filename = None
    iLine =[]
    gLine =[]
    aLine =[]

    if len(arg) == 2:
        filename = arg[1]
        for x in open(filename):
            x = x.split()
            x = ' '.join(x)
            if x == '':
                pass
            else: 
                if x[0] == 'I':
                    iLine = x.strip()
                elif x[0] == 'G':
                    gLine = x.strip()
                elif x[0] == 'A':
                    aLine.append(x.strip())
                else:
                    pass

        return [iLine, gLine, aLine]
        
#guarda a informação das linhas lidas em listas
def saveVariables(argv):
    allLines = ''
    
    [iLine, gLine, aLine] = openFile(argv)          

    allLines = iLine + gLine + ''.join(map(str, aLine))                        
    goalState = gLine.split()
    goalState= goalState[1:len(goalState)]

    initState = iLine.split()
    initState= initState[1:len(initState)]
    initState= setHorizon(initState, 0)
    
    return allLines, initState, goalState, aLine

# insere os atomos negados no initial space, aqueles que não foram ditos no ficheiro de entrada
def complement(num2, initState):
    for ini in initState:
        if num2 == ini[:-1]:
            return []
    else:
        return ['-'+num2+'0']
        
# descobre as variáveis existentes dentor dos parentesis
def getVariables (function):
    
    variables = re.findall('\(.*?\)', function)
    variables = re.sub('[()]', ' ', str(variables[0]))
    variables = re.sub("[^\w]"," ",variables).split()
    return variables
    
# calcula todas as combinações possíveis de constantes, de acordo com o número de variáveis pretendido
def getCombinations(variables, constants):
    
    if len(variables) == 1:
        newComb = constants
     
    else:
        newComb = list(itertools.permutations(constants, len(variables)))
#        newComb = list(itertools.product(constants, repeat= len(variables)))
    return newComb
    
# cria o complemento do estado inicial com as variaveis negadas e a combinação de todos os atomos grounded
def organizeVariables(atoms, initState, constants):
    
    atomListComb = []
    complementInit=[]
    for atom in atoms:
        
        atomVariables = getVariables(atom)
        atomNewComb = getCombinations(atomVariables, constants)
        for combination2 in atomNewComb:

            num2 = atom
            if len(atomVariables) == 1:
                num2 = re.sub(atomVariables[0], combination2, str(num2))
                
            else:
                for i in range(len(combination2)):
                    num2 = re.sub(atomVariables[i], combination2[i], str(num2))
            
            atomListComb.append(num2) 
            
            #Chama a função de cima e vê se esse atom está no init state ou não
            complementInit.extend(complement(num2, initState))
#    print(atomListComb)
    initialState = initState + complementInit
    
    return initialState, atomListComb


#########################################################################################
        
        
# cria a lista de acções, grounded
def defineActions( actions, constants, t):
 
    actListComb = []    
    #para cada acçao
    for act in actions:
        junto2=[]
        one=[]
        variables = getVariables(act[0][0])
        newCombList = getCombinations(variables, constants)

        actVariables=[]
        # para todos efeitos e precondições
        for actt in act:
            # para cada efeito e cada precondição
            for acttt in actt:
                
                one.extend(re.findall(r'(.*?)\(', acttt))
                two = '('
                var = getVariables(acttt)
                actVariables.append(var)
                four = ')'
        # para cada combinaçao de constantes       
        for combination in newCombList:
            
            junto=[]
            dictio=dict()
            # cria um dicionario para substituir as variavais desejadas por constantes
            for index, entry in enumerate(actVariables[0]):
                dictio[entry] = combination[index]
                
            for index2, acts in enumerate(actVariables):
                newAct=[]
                for letter in acts:
                    if letter in dictio:
                        newAct.append(dictio[letter])
                    else:
                        newAct.append(letter)
               
                if index2 < (1+len(act[1])):
                    time = t-1
                else:
                    time = t       
                junto.append(one[index2] + two + ','.join(newAct) + four + str(time))

            junto2.append(junto)
        actListComb.append(junto2)
                    
    return actListComb   
    
    
###########################################################################

#cria zeros entre cada entrada de uma lista, que representam ^ em CNF
def SATformat(expression):
    list1=expression
    list2= [0] * len(expression)
    result = [None]*(len(list1)+len(list2))
    result[::2] = list1
    result[1::2] = list2
    return result

