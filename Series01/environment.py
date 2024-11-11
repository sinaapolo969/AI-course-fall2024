# Vacuum world
import random
from typing import Tuple, Any
from perfmeasure import *



class VacuumWorld:

    def __init__(self, size=(4, 4), L_sahpe = False, observability='Fully', num_agents=1,
                 non_deterministic=False, sequential=False, dynamic=False,
                 continuous=False, perf_measure:PerfurmanceMeasure=None, 
                 no_location_sensor=False, no_status_sensor=False) -> None:
        # Env attributes
        self.size = size
        self.observability = observability
        self.num_agents = num_agents
        self.non_deterministic = non_deterministic
        self.sequential = sequential
        self.dynamic = dynamic
        self.continuous = continuous
        self.L_shape = L_sahpe
        self.pref_measure = perf_measure
        self.no_location_sensor = no_location_sensor
        self.no_status_sensor = no_status_sensor
        self.location = [0, 0]

        self.__initialize_rooms()

    def __initialize_rooms(self):
        self.rooms = []
        if self.L_shape:
            self.rooms.append([random.choice([0, 1]) for _ in range(2)])
            self.rooms.append([random.choice([0, 1])])
            print(self.rooms)
        else:
            for i in range(self.size[0]):
                self.rooms.append([random.choice([0, 1]) for _ in range(self.size[1])])

    def successor(self, move) -> list:
        """
        returns if its possible to move to that room or not.
        """

        if move == 'S':
            return None
        x, y = self.location[0], self.location[1]
        moves = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
        dx, dy = moves[move]
        new_x, new_y = x + dx, y + dy
        if new_y == 1:
            if new_x == 0:
                return True
        elif new_y == 0:
            if 0 <= new_x < 2:              
                return True
        return False

    def get_status(self) -> float | list[float]:
        """
        get the status of current loc.
        """
        if self.no_status_sensor:
            return None
        return self.rooms[self.location[0]][self.location[1]]

    def step(self, action):
        """
        get action from agent and updates the rooms.
        """            
        if self.successor(action) == True:
            self.pref_measure.F1 += 1
        elif self.successor(action) == False:
            self.pref_measure.F2 += 1
            return self.location
        if action == 'S':
            if self.non_deterministic:
                if random.random() < 0.8:
                    self.rooms[self.location[0]][self.location[1]] = 0
                    self.pref_measure.F4 += 1
                else:
                    print(f"Agent failed to clean the room {self.location}")
                    self.pref_measure.F3 += 1
            else:
                self.rooms[self.location[0]][self.location[1]] = 0
                self.pref_measure.F4 += 1

        else:
            if self.non_deterministic:
                if random.random() > 0.8:
                    print(f"Agent failed to move to {action}")
                    moves = ['U', 'D', 'L', 'R']
                    act = random.choice(moves)
                    action = act
            if self.successor(action) == True:
                if action == 'R':
                    self.location[1] += 1
                elif action == 'L':
                    self.location[1] -= 1
                elif action == 'U':
                    self.location[0] -= 1
                elif action == 'D':
                    self.location[0] += 1
            elif self.successor(action) == False:
                return self.location
        
        dirty_rooms = 0
        for room in self.rooms:
            dirty_rooms += sum(room)
        self.pref_measure.F5 += dirty_rooms
        return self.location

    def goal_test(self):
        res = 0
        for row in self.rooms:
            res += sum(row)
        if res <= 0:
            return True
        else:
            return False
