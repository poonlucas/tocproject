import pdb
from itertools import product

import numpy as np
import graphviz


def check_preference(preference, assignment):
    for action in preference:
        if (action > 0 and assignment[abs(action) - 1] == 1) or (action < 0 and assignment[abs(action) - 1] == 0):
            return False
    return True


class MDP:
    def __init__(self, horizon: int = 5, max_preferences: int = 10):
        self.max_preferences = max_preferences
        self.horizon = horizon

        self.states = []
        for h in range(1, self.horizon + 1):
            assigned = np.array(list(product([0, 1], repeat=h-1)), dtype=int)
            unassigned = -np.ones((2 ** (h-1), self.horizon - 1 - (h-1)), dtype=int)
            states_h = np.concatenate((assigned, unassigned), axis=1)
            self.states.append(states_h)

        self.preferences = self.createPreferences()

    def createPreferences(self):
        preferences = [[]] * self.max_preferences
        var_choices = [x for x in range(-(self.horizon - 1), self.horizon)]
        var_choices.pop(self.horizon - 1)
        for i in range(self.horizon - 1):
            R = np.random.randint(1, self.horizon)
            preferences[i] = np.random.choice(var_choices, size=R, replace=False)
        return preferences

    def reward(self, assignment):
        violated_preferences = [check_preference(preference, assignment) for preference in self.preferences]
        return 1 - violated_preferences.count(True) / len(self.preferences)

    def visualize(self, solution):
        solution = [0 if a < 0 else 1 for a in solution]
        graph = graphviz.Digraph(comment='MDP')
        graph.attr(rankdir='LR')
        for h, state_h in enumerate(self.states):
            with graph.subgraph(name=str(h)) as c:
                for state in state_h:
                    color = 'black'
                    if np.all(state[:h] == solution[:h]):
                        color = 'red'
                    c.node(str(state),
                           label=(str(state) if h < self.horizon - 1 else f'{state}, {self.reward(state)}'),
                           color=color)
                    if h - 1 >= 0:
                        prev = state.copy()
                        prev[h - 1] = -1
                        c.edge(str(prev), str(state), color=color)

        graph.render(directory='mdp', view=True)
