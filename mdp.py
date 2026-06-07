import pdb
from itertools import product

import numpy as np
import graphviz


def check_clause(clause, assignment):
    for literal in clause:
        if (literal > 0 and assignment[abs(literal) - 1] == 1) or (literal < 0 and assignment[abs(literal) - 1] == 0):
            return True
    return False


class MDP:
    def __init__(self, phi, num_variables: int, num_clauses: int, solution):
        self.phi = phi
        self.horizon = num_variables + 1
        self.num_clauses = num_clauses
        self.solution = [-1] * num_variables
        for v in solution:
            self.solution[abs(v) - 1] = 1 if v > 0 else 0

        self.states = []
        for h in range(1, self.horizon + 1):
            assigned = np.array(list(product([0, 1], repeat=h-1)), dtype=int)
            unassigned = -np.ones((2 ** (h-1), num_variables - (h-1)), dtype=int)
            states_h = np.concatenate((assigned, unassigned), axis=1)
            self.states.append(states_h)

    def reward(self, assignment):
        correct_clauses = [check_clause(clause, assignment) for clause in self.phi]
        return correct_clauses.count(True) / self.num_clauses

    def visualize(self):
        graph = graphviz.Digraph(comment='MDP')
        graph.attr(rankdir='LR')
        for h, state_h in enumerate(self.states):
            with graph.subgraph(name=str(h)) as c:
                for state in state_h:
                    color = 'black'
                    if np.all(state[:h] == self.solution[:h]):
                        color = 'red'
                    c.node(str(state),
                           label=(str(state) if h < self.horizon - 1 else f'{state}, {self.reward(state)}'),
                           color=color)
                    if h - 1 >= 0:
                        prev = state.copy()
                        prev[h - 1] = -1
                        c.edge(str(prev), str(state), color=color)

        graph.render(directory='mdp', view=True)


if __name__ == '__main__':
    mdp = MDP([[-1, 2, -3], [1, 2, 4]], 4, 2, [-1, 2, 3, 4])
    mdp.visualize()
