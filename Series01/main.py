from environment import VacuumWorld
from agent import SimpleReflexive

env = VacuumWorld(size=(5, 5))
agent = SimpleReflexive()

while not env.goal_test():
    curr_state = [agent.curr_x, agent.curr_y]
    percept = env.get_status(curr_state)
    action = agent.action(percept, successor=env.successor)
    state = env.set_status(curr_state, action)
    agent.curr_x = state[0]
    agent.curr_y = state[1]
    print(env.rooms)
