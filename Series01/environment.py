# Vacuum world
import random
from typing import Tuple, Any
from perfmeasure import *
from abstract_agent import *



class VacuumWorld:

    def __init__(self, agent:AbstractAgent, size=(4, 4), L_sahpe= False, num_agents=1,
                 non_deterministic_vacuum=False, non_determenistic_move=False, sequential=False, dynamic=False,
                 continuous=False, perf_measure:PerfurmanceMeasure=None, 
                 no_location_sensor=False, no_status_sensor=False) -> None:
        # Env attributes
        self.size = size
        self.num_agents = num_agents
        self.non_deterministic_vacuum = non_deterministic_vacuum
        self.non_determenistic_move = non_determenistic_move
        self.sequential = sequential
        self.dynamic = dynamic
        self.continuous = continuous
        self.L_shape = L_sahpe
        self.pref_measure = perf_measure
        self.no_location_sensor = no_location_sensor
        self.no_status_sensor = no_status_sensor
        self.location = [0, 0]
        self.abs_agent = agent

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
        return self.rooms[self.location[0]][self.location[1]]

    def get_clean_rooms_location(self) -> int:
        """
        get the location of the clean rooms.
        """
        clean_rooms = []
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                if self.rooms[i][j] == 0:
                    clean_rooms.append([i, j])
        return clean_rooms
    
    def run(self, step_size=1) -> Any:
        """
        get action from agent and updates the rooms.
        """
        while not self.goal_test():
            if self.no_location_sensor:
                percept = State(None, self.get_status())
            elif self.no_status_sensor:
                percept = State(self.location, None)
            else:
                percept = State(self.location, self.get_status())
            action = self.abs_agent.run(percept, step_size=step_size)    
            if self.dynamic: 
                if random.random() < 0.2:
                    clean_rooms = self.get_clean_rooms_location()
                    if len(clean_rooms) > 0:
                        random_room = random.choice(clean_rooms)
                        self.rooms[random_room[0]][random_room[1]] = 1
            if self.successor(action.selected_action) == True:
                self.pref_measure.F1 += 1
            elif self.successor(action.selected_action) == False:
                self.pref_measure.F2 += 1

            if action.selected_action == 'S':
                if self.non_deterministic_vacuum:
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
                if self.non_determenistic_move:
                    if random.random() > 0.8:
                        print(f"Agent failed to move to {action.selected_action}")
                        action.selected_action = random.choice(Action.ACTIONS)
                        print(f"Agent will move to {action.selected_action}")
                if self.successor(action.selected_action) == True:
                    if action.selected_action == 'R':
                        self.location[1] += 1
                    elif action.selected_action == 'L':
                        self.location[1] -= 1
                    elif action.selected_action == 'U':
                        self.location[0] -= 1
                    elif action.selected_action == 'D':
                        self.location[0] += 1
            
            dirty_rooms = 0
            for room in self.rooms:
                dirty_rooms += sum(room)
            self.pref_measure.F5 += dirty_rooms

        return
    
    def goal_test(self):
        res = 0
        for row in self.rooms:
            res += sum(row)
        if res <= 0:
            return True
        else:
            return False
