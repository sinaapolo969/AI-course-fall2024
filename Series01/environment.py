# Vacuum world
import random
from typing import Tuple, Any


class VacuumWorld:

    def __init__(self, size=(4, 4), L_sahpe = False, observability='Fully', num_agents=1,
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
        self.L_shape = L_sahpe
        self.location = [0, 0]

        self.__initialize_rooms()

    def __initialize_rooms(self):
        self.rooms = []
        if self.L_shape:
            self.rooms.append([random.choice([0, 1]) for _ in range(2)])
            self.rooms.append([random.choice([0, 1])])
        for i in range(self.size[0]):
            self.rooms.append([random.choice([0, 1]) for _ in range(self.size[1])])

    def successor(self) -> list:
        """
        returns a list of possible actions.
        """
        x, y = self.location[0], self.location[1]
        successors = []
        moves = {(-1, 0): 'U', (1, 0): 'D', (0, -1): 'L', (0, 1): 'R'}
        for dx, dy in moves.keys():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size[0] and 0 <= new_y < self.size[1]:
                successors.append(list(moves[(dx, dy)]))
        return successors

    def get_status(self) -> float | list[float]:
        """
        get the status of current loc.
        """
        return self.rooms[self.location[0]][self.location[1]]

    def step(self, action):
        """
        get action from agent and updates the rooms.
        """
        if action == 'S':
            self.rooms[self.location[0]][self.location[1]] = 0
        elif action == 'R':
            self.location[1] += 1
        elif action == 'L':
            self.location[1] -= 1
        elif action == 'U':
            self.location[0] -= 1
        elif action == 'D':
            self.location[0] += 1
        return self.location

    def goal_test(self):
        res = 0
        for row in self.rooms:
            res += sum(row)
        if res <= 0:
            return True
        else:
            return False
