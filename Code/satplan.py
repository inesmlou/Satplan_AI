import sys
import satsolver
import Encoder

# arranja a informação inicial retirada do ficheiro de input
plan = Encoder.initPlan(sys.argv)
result = 'UNSAT'
t = 0

while result == 'UNSAT':

    t += 1
    # chama o encoder para criar a sentence de tudo o que acontece para certo t
    SATsentence, SATvariables = Encoder.encode(plan, t)
    # dá a frase codificada ao solver
    result = satsolver.satSolver(SATsentence)

# quando encontra solução chama o decoder para traduzir para acções
solution = Encoder.decode(result, plan[0], SATvariables, t)
