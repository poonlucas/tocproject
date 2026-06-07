import pdb
from itertools import product

import numpy as np
import graphviz


class MDP:
    def __init__(self, phi, num_variables: int, num_clauses: int, solution):
        self.phi = phi
        self.horizon = num_variables + 1
        self.num_clauses = num_clauses
        self.solution = solution

        self.states = []
        for h in range(1, self.horizon + 1):
            assigned = np.array(list(product([0, 1], repeat=h-1)), dtype=int)
            unassigned = -np.ones((2 ** (h-1), num_variables - (h-1)), dtype=int)
            states_h = np.concatenate((assigned, unassigned), axis=1)
            self.states.append(states_h)

    def reward(self, assignment):
        # check number of satisfied clauses
        correct_clauses = 1
        return correct_clauses / self.num_clauses

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
    mdp = MDP(-1, 3, 3, [0, 1, 1])
    mdp.visualize()
