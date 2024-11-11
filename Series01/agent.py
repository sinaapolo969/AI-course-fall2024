# vacuum agent
import random
from abstract_agent import AbstractAgent, Action, State

# simple reflexive agent

class SimpleReflexive(AbstractAgent):

    def __init__(self) -> None:
        pass

    def step(self, percept:State) -> Action:
        action = Action()

        if percept.status == 0:
            print(f"The room was clean!")
            if percept.room == [1, 0] and percept.room != None:
                action.selected_action = 'U'
            if percept.room == [0, 1] and percept.room != None:
                action.selected_action = 'L'
            if percept.room == [0, 0]: # location sensor doesnt matter in this case, it would be random anyway!
                action.selected_action = random.choice(Action.ACTIONS - 'S') # for [0, 0] room agnet will move randomly

            print(f"I'll go {action.selected_action[0]}")
            return action
        
        elif percept.status == 1:
            print(f"The room was dirty! I'll do cleaning.")
            action.selected_action = 'S'
            return action
        else:
            print('I have no idea what to do! random move')
            action.selected_action = random.choice(Action.ACTIONS)
            print(f"I'll do {action.selected_action[0]}")
            return action
