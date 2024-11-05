from environment import VacuumWorld
from agent import SimpleReflexive
from perfmeasure import PerfurmanceMeasure
from tabulate import tabulate

pref_measure = PerfurmanceMeasure()
env = VacuumWorld(size=(5, 5), L_sahpe=True, perf_measure=pref_measure)
agent = SimpleReflexive()

while not env.goal_test():
    percept = env.get_status()
    action = agent.action(percept)
    state = env.step(action)
    print(env.rooms)

headers = ["Agent Moves", "Unsuccessful Agent Moves", "Unsuccessful Vacuums", "Successful Vacuums", "Dirty Rooms After Step"]
values = [pref_measure.F1, pref_measure.F2, pref_measure.F3, pref_measure.F4, pref_measure.F5]

# Print the table
table = tabulate([values], headers=headers, tablefmt="grid")
print(table)