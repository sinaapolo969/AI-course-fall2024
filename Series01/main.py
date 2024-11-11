from environment import VacuumWorld
from agent import SimpleReflexive
from perfmeasure import PerfurmanceMeasure
from tabulate import tabulate


for i in range(100):
    pref_measure = PerfurmanceMeasure()
    agent = SimpleReflexive()
    env = VacuumWorld(size=(5, 5), agent=agent, L_sahpe=True, perf_measure=pref_measure, non_deterministic=True, 
                    no_status_sensor=True, no_location_sensor=True)
    
    env.run(1)
    headers = ["Agent Moves", "Unsuccessful Agent Moves", "Unsuccessful Vacuums", "Successful Vacuums", "Dirty Rooms After Step"]
    values = [pref_measure.F1, pref_measure.F2, pref_measure.F3, pref_measure.F4, pref_measure.F5]

    # Print the table
    table = tabulate([values], headers=headers, tablefmt="grid")
    print(table)