from environment import VacuumWorld
from agent import SimpleReflexive

env = VacuumWorld(size=(5, 5))
agent = SimpleReflexive()

while not env.goal_test():
    percept = env.get_status()
    action = agent.action(percept, successor=env.successor)
    state = env.step(action)
    agent.curr_x = state[0]
    agent.curr_y = state[1]
    print(env.rooms)
