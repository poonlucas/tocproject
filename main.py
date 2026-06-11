from pysat.formula import CNF
from pysat.solvers import Solver
import numpy as np
import mdp

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
    #       if var_assignment[i] = -k < 0 then x_k = False
    #       This is to be consistent with the PySAT notation
    #
    # if no solution is found (all clauses unsolvable or none satisfying the delta-bound) will return (0, None, None)
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
    # Given:
    #   max_num_clauses: Int
    #
    # determines if there is a solution where max_num_clauses of clauses are satisfied
    # if not, then recursively determines if max_num_clauses - 1 clausea are satisfied
    # will return (0, None, None) if no solution is found
    def _solve(self, max_num_clauses, clauses):
        if max_num_clauses == 0:
            return (0, None, None)

        cnf = CNF(from_clauses=clauses)
        with Solver(bootstrap_with=cnf) as solver:
            status = solver.solve()
            permutations = [clauses[:i] + clauses[i+1:] for i in range(len(clauses))] # all possible combinations with one element removed
            inBound = float(max_num_clauses) / float(len(self.phi)) >= 1.0 - self.delta
            if status and inBound: # CNF is solvable and in-bound
                return (max_num_clauses, clauses, solver.get_model())

            # else invalid, try again with less clauses
            solved_subcnf_arr = len(permutations) * [(None, None, None)]
            for i, _cnf in enumerate(permutations):
                solved_subcnf_arr[i] = self._solve(max_number_clauses - 1, _cnf)

            max_sol = (0, None, None)
            for sol_tuple in solved_subcnf_arr:
                if sol_tuple[0] is None:
                    continue
                if sol_tuple[0] > max_sol[0]:
                    max_sol = sol_tuple

            if max_sol[0] == 0:
                return (0, None, None)
            return max_sol
# ============== END OF CLASS DeltaMaxSAT =========================




class TestDeltaMaxSAT:
    def __init__(self, num_test_cnf, max_num_clauses=5, max_num_vars=10, seed=None):
        self.max_num_clauses = max_num_clauses
        self.num_test_cnf = num_test_cnf
        self.max_num_vars = max_num_vars
        self.seed = seed

    # start creating and running test cases
    #   creates random 3-CNF formulas with at most 'max_num_clauses' clauses
    #   will create 'num_test_cnf' test cases (one 3-CNF instance being a single test case)
    def run(self):
        ...

    # create a CNF with at most self.max_num_vars variables per clause and self.max_num_clauses clauses per boolean formula
    def _createCNF(self, debug=False):
        np.random.seed(self.seed)
        cnf = self.max_num_clauses * [0]
        # ex: num_variables = 3
        # --> var_choices = [-3, -2, -1, 1, 2, 3]
        # the pop serves to remove the element '0' which is in var_choices upon creation
        var_choices = [x for x in range(-self.max_num_vars, self.max_num_vars + 1)]
        var_choices.pop(self.max_num_vars)
        if debug:
            print(f'var_choices = {var_choices}')
        for i in range(self.max_num_clauses):
            # CNF calls for R <= self.max_num_vars random variables per clause
            R = np.random.randint(1, self.max_num_vars + 1)
            cnf[i] = np.random.choice(var_choices, size=R, replace=False)

        if debug:
            print('cnf =')
            for clause in cnf:
                print(clause)


    def print(self):
        print('max_num_vars =', self.max_num_vars)
        print('max_num_clauses =', self.max_num_clauses)
        print('num_test_cnf =', self.num_test_cnf)
        print('seed =', self.seed)
# end of class TestDeltaMaxSAT ========================



if __name__ == '__main__':
    print('main() is empty right now :(')
    print('testing TestDeltaMaxSAT')
    tdms = TestDeltaMaxSAT(num_test_cnf=5)
    tdms.print()
    tdms._createCNF(debug=True)

