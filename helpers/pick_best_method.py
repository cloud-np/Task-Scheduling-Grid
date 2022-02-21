from classes.scheduler import FillMethod
from helpers.examples.example_gen import ExampleGen
from helpers.simulation.simulation import Simulation
import random


def find_c1_example():
    run_methods = [{"name": "c1", "time_types": ["EST"], "fill_type": "NO-FILL"}]
    i = 0
    done = False
    while not done:
        random.seed(i)
        machines, workflows = ExampleGen.load_fixed_small_random()
        schedulers = Simulation(run_methods, machines, workflows).run_c1()
        if 393 < schedulers[0].schedule_len < 400:
            done = True
        i += 1
    return i, schedulers


def find_seed_for(fill_method: FillMethod, starting_seed: int = 0):
    i = starting_seed
    done = False
    run_methods = [
        {"name": "holes FASTEST-FIT", "time_types": ["EFT", "EFT"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT", "time_types": ["EFT", "EFT"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT", "time_types": ["EFT", "EFT"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT", "time_types": ["EFT", "EFT"], "fill_type": "WORST-FIT"},
    ]
    while not done:
        random.seed(i)
        machines, workflows = ExampleGen.load_fixed_small_random()
        schedulers = Simulation(run_methods, machines, workflows).run_paper_example()

        min_s = min(schedulers, key=lambda s: s.avg_workflow_makespan)
        all_avgs = [s.schedule_len for s in schedulers if s.fill_method != fill_method]
        # print(f"{min_s}\niter: {i}\n {''.join([f'{s.schedule_len} ' for s in schedulers])}")

        if min_s.fill_method == fill_method:
            done = min_s.schedule_len not in all_avgs
            for m in min_s.machines:
                if m.contains_wf_id(wf_id=1) is False:
                    done = False
            if not done:
                i += 1
        else:
            done = False
            i += 1
            # Visualizer.visualize_machines(min_s.machines)
    return i, min_s.workflows
