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
#       phi[k][0..2] = 3 Variables in Clause k
class DeltaMaxSAT:
    def __init__(self, phi, delta=0.125, max_num_clauses=5):
        self.MAX_NUM_CLAUSES_PER_CNF = max_num_clauses
        self.delta = delta
        self.phi = phi
        self.cnf = CNF(from_clauses=self.phi)

    # returns a tuple (max_num_clauses, clauses, var_assignment)
    #   max_num_clauses: Int; the maximum number of clauses solvable such that
    #           |C [solved]| / |C [total]| >= 1 - delta
    #   clauses: List[List[Int]; clauses[i] = C_i = ith clause
    #   var_assignment: List[Int];
    #       if var_assignment[i] = k > 0 then x_k = True
    #       if var_assignment[i] = -k < 0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 then x_k = False
    #       This is to be consistent with the PySAT notation
    #
    # if no solution is found (all clauses unsolvable or none satisfying the delta-bound) will return (None, None, None)
    def solve(self):
        # solvability check: is there at least one solvable clause?
        # if not, don't bother going through the recursion
        quick_check_passed = False
        for clause in self.phi:
            cnf = CNF(from_clauses=[clause])
            with Solver(bootstrap_with=cnf) as solver:
                if solver.solve():
                    quick_check_passed = True
                    break
        # not a single satisfiable clause
        if not quick_check_passed:
            return (None, None, None)

        return self._solve(max_num_clauses=min(self.MAX_NUM_CLAUSES_PER_CNF, len(self.phi)), clauses=self.phi)



    # helper function for solve()
    def _solve(self, max_num_clauses, clauses):
        if max_num_clauses == 0:
            return (None, None, None)

        cnf = CNF(from_clauses=clauses)
        with Solver(bootstrap_with=cnf) as solver:
            status = solver.solve()
            permutations = [clauses[:i] + clauses[i+1:] for i in range(len(clauses))] # all possible combinations with one element removed
            if not status: # current num clauses invalid, try one less
                for _cnf in permutations:
                    return _solve(max_num_clauses - 1, _cnf)

            inBound = float(max_num_clauses) / float(len(self.phi)) >= 1.0 - self.delta
            if not inBound: # current num clauses invalid, try one less
                for _cnf in permutations:
                    return _solve(max_num_clauses - 1, _cnf)

            # CNF is solvable and in-bound
            return (max_num_clauses, clauses, solver.get_model())




if __name__ == '__main__':
    print('main() is empty right now :(')





