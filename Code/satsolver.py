#############################################################
#      ooooo       .o.        .oooooo..o oooooooooo.        #
#      '888'      .888.      d8P'    'Y8 '888'   'Y8b       #
#       888      .8"888.     Y88bo.       888      888      #
#       888     .8' '888.     '"Y8888o.   888      888      #
#       888    .88ooo8888.        '"Y88b  888      888      #
#       888   .8'     '888.  oo     .d8P  888     d88'      #
#      o888o o88o     o8888o 8""88888P'  o888bood8P'        #
#                                                           #
#                                                           #
#                 Project 2 - SATPLAN                       #
#                                                           #
#                    Authors:                               #
#               Christopher Edgley  75258                   #
#               Inês Lourenço       75637                   #
#                                                           #
#############################################################

import DPLL
import DPLL2
import walkSAT

def satSolver(sCla):
    
    dVar = DPLL.initSat(sCla)
    sat = DPLL.DPLL(dVar)
    if sat == 1:
        return DPLL.printSat()
    else:
        return 'UNSAT'
    
def satSolver2(sCla):
    
    lCla, dVar = DPLL2.initSat(sCla)
    sat = DPLL2.DPLL(lCla, dVar)
    if sat == 1:
        return DPLL2.printSat()
    else:
        return 'UNSAT'

def walkSatSolver(sCla):
    
    lCla, dVar = walkSAT.initSat(sCla)
    sat = walkSAT.walkSAT(lCla, dVar)
    if sat == 1:
        return walkSAT.printSat()
    else:
        return 'UNSAT'