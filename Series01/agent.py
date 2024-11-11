# vacuum agent
import random


# simple reflexive agent

class SimpleReflexive:

    def __init__(self) -> None:
        pass

    def action(self, percept):
        possible_moves = ['U', 'D', 'L', 'R', 'S']
        moves = ['U', 'D', 'L', 'R']
        if percept == 0:
            print(f"The room was clean!")
            act = random.choice(moves)
            print(f"I'll go {act[0]}")
            return act[0]
        elif percept == 1:
            print(f"The room was dirty! I'll do cleaning.")
            return 'S'
        else:
            print('I have no idea what to do! random move')
            act = random.choice(possible_moves)
            print(f"I'll do {act[0]}")
            return act[0]
