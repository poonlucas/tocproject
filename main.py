import pdb

from pysat.formula import CNF
from pysat.solvers import Solver
import numpy as np
import mdp

# class to solve a delta-MAX-SAT
#   cnf: CNF solver from PySAT
#   phi: boolean formula
#       phi[k] = Clause k
#       phi[k][0..2] = 3 Variables in Clause k
class DeltaMaxSAT:
    def __init__(self, phi, delta=0.125, max_num_clauses=5, debug=False):
        self.MAX_NUM_CLAUSES_PER_CNF = max_num_clauses
        self.delta = delta
        self.phi = phi
        self.solution = self.solve(debug=debug)

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
    def solve(self, debug=False):
        # solvability check: is there at least one solvable clause?
        # if not, don't bother going through the recursion
        quick_check_passed = False
        if debug:
            print('beginning quick check')
            print('phi:', self.phi)
        for clause in self.phi:
            if debug:
                print('checking clause:', clause)
            cnf = [clause]
            if debug:
                print('cnf:', cnf)
            with Solver(bootstrap_with=cnf) as solver:
                if debug:
                    print('inside solver')
                if solver.solve():
                    if debug:
                        print('quick check passed')
                    quick_check_passed = True
                    break
        # not a single satisfiable clause
        if not quick_check_passed:
            if debug:
                print('quick check failed')
            return (0, None, None)

        return self._solve(max_num_clauses=min(self.MAX_NUM_CLAUSES_PER_CNF, len(self.phi)), clauses=self.phi, debug=debug)



    # helper function for solve()
    # Given:
    #   max_num_clauses: Int
    #
    # determines if there is a solution where max_num_clauses of clauses are satisfied
    # if not, then recursively determines if max_num_clauses - 1 clausea are satisfied
    # will return (0, None, None) if no solution is found
    def _solve(self, max_num_clauses, clauses, debug=False):
        if debug:
            print('entered helper function')
        if max_num_clauses == 0:
            if debug:
                print('no clauses: return (0, None, None)')
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
                solved_subcnf_arr[i] = self._solve(max_num_clauses - 1, _cnf)

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

if __name__ == '__main__':
    # change seed to None if you want unpredictable seeds to be passed into MDP
    SEED = 10
    NUM_TESTS = 1
    MAX_NUM_CLAUSES = 5
    HORIZON = 5

    np.random.seed(SEED)

    for _ in range(NUM_TESTS):
        _mdp = mdp.MDP(horizon=HORIZON, max_preferences=MAX_NUM_CLAUSES)
        all_prefs = _mdp.preferences
        print('preferences:', all_prefs)

        # generate a CNF from the given preferences
        #   maybe a list comprehension would be better here? idk tho
        #cnf = list(map(lambda arr: list(map(lambda x: -x, arr)), all_prefs))
        # remove extra empty arrays since they can mess up the PySAT solver
        cnf = []
        for pref in all_prefs:
            if len(pref) == 0:
                continue
            cnf.append([int(-x) for x in pref])
        print('phi:', cnf)

        # solve the formed CNF
        # delta=1: convert DeltaMaxSAT to just MaxSAT
        dms = DeltaMaxSAT(phi=cnf, delta=1, max_num_clauses=MAX_NUM_CLAUSES)
        print('solution:', dms.solution)

        solution = [i for i in range(1, HORIZON)]
        for a in dms.solution[2]:
            solution[abs(a) - 1] = a
        _mdp.visualize(solution)





