# vacuum agent
import random


# simple reflexive agent

class SimpleReflexive:

    def __init__(self) -> None:
        self.curr_x = 0
        self.curr_y = 0

    def action(self, percept, successor):
        if percept == 0:
            print(f"The room was clean!")
            possible_act = successor([self.curr_x, self.curr_y])
            act = random.choice(possible_act)
            return act[0]
        else:
            print(f"The room was dirty!")
            return 'S'
