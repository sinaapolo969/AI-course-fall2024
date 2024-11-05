# vacuum agent
import random


# simple reflexive agent

class SimpleReflexive:

    def __init__(self) -> None:
        pass

    def action(self, percept):
        if percept == 0:
            print(f"The room was clean!")
            moves = ['U', 'D', 'L', 'R']
            act = random.choice(moves)
            print(f"I'll go {act[0]}")
            return act[0]
        else:
            print(f"The room was dirty! I'll do cleaning.")
            return 'S'
