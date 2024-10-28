# Vacuum world
import random
from typing import Tuple, Any


class VacuumWorld:

    def __init__(self, size=(4, 4), observability='Fully', num_agents=1,
                 non_deterministic=False, sequential=False, dynamic=False,
                 continuous=False, ) -> None:
        # Env attributes
        self.size = size
        self.observability = observability
        self.num_agents = num_agents
        self.non_deterministic = non_deterministic
        self.sequential = sequential
        self.dynamic = dynamic
        self.continuous = continuous

        self.__initialize_rooms()

    def __initialize_rooms(self):
        self.rooms = []
        for i in range(self.size[0]):
            self.rooms.append([random.choice([0, 1]) for _ in range(self.size[1])])

    def successor(self, state) -> list:
        """
        inputs a state, and returns a list of possible actions.
        """
        x, y = state[0], state[1]
        successors = []
        moves = {(-1, 0): 'U', (1, 0): 'D', (0, -1): 'L', (0, 1): 'R'}
        for dx, dy in moves.keys():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size[0] and 0 <= new_y < self.size[1]:
                successors.append(list(moves[(dx, dy)]))
        return successors

    def get_status(self, state) -> float | list[float]:
        """
        get the status of input state.
        """
        return self.rooms[state[0]][state[1]]

    def set_status(self, state, action):
        """
        inputs a state and a status from agent and updates the rooms.
        """
        if action == 'S':
            self.rooms[state[0]][state[1]] = 0
        elif action == 'R':
            state[1] += 1
        elif action == 'L':
            state[1] -= 1
        elif action == 'U':
            state[0] -= 1
        elif action == 'D':
            state[0] += 1
        return state

    def goal_test(self):
        res = 0
        for row in self.rooms:
            res += sum(row)
        if res <= 0:
            return True
        else:
            return False
