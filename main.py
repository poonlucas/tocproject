from pysat.formula import CNF
from pysat.solvers import Solver

# TUTORIAL SCRIPT FROM WEBSITE TO GET A FEEL FOR HOW TO USE PYSAT
# (-x1 OR x2) AND (-x1 OR -x2)
#cnf = CNF(from_clauses=[[-1, 2], [-1,-2]])

#with Solver(bootstrap_with=cnf) as solver:
    # call solver for this formula
 #   print('formula is', f'{"s" if solver.solve() else "uns"}atisfiable')

    # the formula is satisfiable, thus has a model
  #  print('and the model is:', solver.get_model())

    # minisat assumption inferface?
   # print('formula is', f'{"s" if solver.solve(assumptions=[1, 2]) else "uns"}atisfiable', 'assuming x1 and x2')

    # the formula is unsatisfiable
    #print('and the unsatisfiable core is:', solver.get_core())

# class to solve a delta-3-MAX-SAT
#   cnf: CNF solver from PySAT
#   phi: boolean formula
#       phi[k] = Clause k
#   phi[k][0..2] = 3 Variables in Clause k
class DeltaMaxSAT:
    def __init__(self, delta, phi):
        self.delta = delta
        self.cnf = CNF(from_clauses=phi)
        self.phi = phi

    # returns True if solvable, False otherwise
    def solve(self):
        with Solver(bootstrap_with=self.cnf) as solver:
            return True if solver.solve() else False







if __name__ == '__main__':
    phi = [[1], [-1]]
    dms = DeltaMaxSAT(delta=0.125, phi=phi)
    status = dms.solve()
    if status:
        print('Solvable')
    else:
        print('Unsolvable')





