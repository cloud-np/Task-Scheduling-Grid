from helpers.examples.example_data import HOLE_METHOD_VARIATIONS
# from helpers.visuals.visualize import Visualizer
from helpers.examples.example_gen import ExampleGen
from helpers.simulation.simulation import Simulation


if __name__ == "__main__":

    run_methods = [HOLE_METHOD_VARIATIONS["compositions"]]
    run_methods = [HOLE_METHOD_VARIATIONS["criticals_sorted"], HOLE_METHOD_VARIATIONS["criticals_unsorted"]]

    run_methods = sum(run_methods, [])
    n = 8
    ss = []
    for n_machines in [8]:
        for network in [50]:
            machines, workflows = ExampleGen.load_random_wfs([n_machines, network * 125], 10)
            # machines, workflows = ExampleGen.load_all_types([n_machines, network * 125], 100, n_times=n)
            print(f"n-wfs: {n} machines: {n_machines}  network: {network}")
            # Simulation(run_methods, machines, workflows, visuals=False, save_fig=False, show_fig=True, save_sim=True, show_machines=False).run()
            ss = Simulation(run_methods, machines, workflows, visuals=True, save_fig=False, show_fig=True, save_sim=False, show_machines=True).run()
            for s in ss:
                print(s)

    # FIRST-FIT 89
    # FASTEST-FIT 172
    # BEST-FIT 1
    # WORST-FIT 0