class Action:

    ACTIONS = ['U', 'D', 'L', 'R', 'S']
    COSTS = {'U': 1, 'D': 1, 'L': 1, 'R': 1, 'S': 1}
    def __init__(self, action=None):
        self.selected_action = action

class State:
    
    def __init__(self, room, status):
        self.room = room
        self.status = status


class AbstractAgent():
    def __init__(self) -> None:
        self.action = Action()
        pass

    def run(self, percept:State, step_size=1) -> Action:
        for _ in range(step_size):
            action = self.step(percept) 
        return action
    
    def step(self, percept: State) -> Action:
        return self.run(percept)