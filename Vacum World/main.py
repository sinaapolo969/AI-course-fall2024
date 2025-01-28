from environment import VacuumWorld
from agent import SimpleReflexive
from perfmeasure import PerfurmanceMeasure
from tabulate import tabulate


params = [
    {"non_deterministic_vacuum": False, "non_determenistic_move": False, "dynamic": False, "no_location_sensor": False, "no_status_sensor": False},
    {"non_deterministic_vacuum": False, "non_determenistic_move": False, "dynamic": False, "no_location_sensor": False, "no_status_sensor": True},
    {"non_deterministic_vacuum": False, "non_determenistic_move": False, "dynamic": False, "no_location_sensor": True, "no_status_sensor": False},
    {"non_deterministic_vacuum": False, "non_determenistic_move": False, "dynamic": True, "no_location_sensor": False, "no_status_sensor": False},
    {"non_deterministic_vacuum": False, "non_determenistic_move": True, "dynamic": False, "no_location_sensor": False, "no_status_sensor": False},
    {"non_deterministic_vacuum": True, "non_determenistic_move": False, "dynamic": False, "no_location_sensor": False, "no_status_sensor": False},
    {"non_deterministic_vacuum": True, "non_determenistic_move": False, "dynamic": True, "no_location_sensor": False, "no_status_sensor": False},
    {"non_deterministic_vacuum": True, "non_determenistic_move": False, "dynamic": False, "no_location_sensor": True, "no_status_sensor": False},
    {"non_deterministic_vacuum": True, "non_determenistic_move": False, "dynamic": False, "no_location_sensor": False, "no_status_sensor": True},
    {"non_deterministic_vacuum": False, "non_determenistic_move": True, "dynamic": True, "no_location_sensor": False, "no_status_sensor": False},
    {"non_deterministic_vacuum": False, "non_determenistic_move": True, "dynamic": False, "no_location_sensor": True, "no_status_sensor": False},
    {"non_deterministic_vacuum": False, "non_determenistic_move": True, "dynamic": False, "no_location_sensor": False, "no_status_sensor": True},
    {"non_deterministic_vacuum": False, "non_determenistic_move": False, "dynamic": True, "no_location_sensor": True, "no_status_sensor": False},
    {"non_deterministic_vacuum": False, "non_determenistic_move": False, "dynamic": True, "no_location_sensor": False, "no_status_sensor": True},
    {"non_deterministic_vacuum": True, "non_determenistic_move": False, "dynamic": True, "no_location_sensor": True, "no_status_sensor": False},
    {"non_deterministic_vacuum": True, "non_determenistic_move": False, "dynamic": True, "no_location_sensor": False, "no_status_sensor": True},
    {"non_deterministic_vacuum": False, "non_determenistic_move": True, "dynamic": True, "no_location_sensor": True, "no_status_sensor": False},
    {"non_deterministic_vacuum": False, "non_determenistic_move": True, "dynamic": True, "no_location_sensor": False, "no_status_sensor": True},
]

for param in params:
    pref_measure = PerfurmanceMeasure()
    agent = SimpleReflexive()
    env = VacuumWorld(agent=agent, L_sahpe=True, perf_measure=pref_measure, **param)
    for i in range(100): 
        env.run(1)
        env.reset()
    headers = ["Agent Moves", "Unsuccessful Agent Moves", "Unsuccessful Vacuums", "Successful Vacuums", "Dirty Rooms After Step"]
    values = [pref_measure.F1, pref_measure.F2, pref_measure.F3, pref_measure.F4, pref_measure.F5]

    table = tabulate([values], headers=headers, tablefmt="grid")
    print(table)
    with open("results.txt", "a") as f:
        f.write(str(param) + "\n")
        f.write(table)
        f.write("\n")