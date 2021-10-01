from algos.paper_2011_algos.paper_method import Paper2011
from helpers.examples.example_data import HOLE_METHOD_VARIATIONS
from helpers.visuals.visualize import Visualizer
from helpers.examples.example_gen import Example
from classes.workflow import Workflow
from classes.machine import Machine
from helpers.simulation.simulation import Simulation


if __name__ == "__main__":

    # Variations. This should be its own file.
    #    {"name": "c1", "time_types": ["EST"], "fill_type": "NO-FILL"},
    #    {"name": "c2", "time_types": ["EST"], "fill_type": "NO-FILL"},
    #    {"name": "c3", "time_types": ["EST"], "fill_type": "NO-FILL"}]
    run_methods = [
        {"name": "holes FASTEST-FIT",
         "time_types": ["EFT", "EFT"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT",
         "time_types": ["EFT", "EFT"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT",
         "time_types": ["EFT", "EFT"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT",
         "time_types": ["EFT", "EFT"], "fill_type": "WORST-FIT"},
    ]

    # run_methods = [HOLE_METHOD_VARIATIONS["EFT_variations"]]
    # run_methods = [{"name": "c1", "time_types": ["EST"], "fill_type": "NO-FILL"}]
    # run_methods = sum(run_methods, [])
    # run_methods = HOLE_METHOD_VARIATIONS["EFT_variations"]
    # run_methods = [{"name": "holes2011 FASTEST-EDF", "fill_type": "FASTEST-FIT", "priority_type": "EDF"}]
    # for wf_size in [50, 100, 200, 300, 400, 500, 1000]:
    #     for network in [50, 500]:
    #         for n_cores in [4, 8, 16, 32]:
    #             # machines = Machine.load_n_static_machines(n_cores, network * 125)
    #             # workflows = Workflow.load_random_workflows(machines, wf_size)
    #             machines, workflows = Example.load_all_types([n_cores, network * 125], wf_size)
    #             Simulation(run_methods, machines, workflows, visuals=False, save_fig=False, show_fig=True, save_sim=True, show_machines=False).run()
    done = False
    while not done:
        machines, workflows = Example.load_small_example()
        # avg_makespan from both for each bin packing method
        done = Simulation(run_methods, machines, workflows, visuals=False, save_fig=False, show_fig=True, save_sim=True, show_machines=True).run()

    # machines, workflows = Example.load_medium_example()
    # machines = Machine.load_n_static_machines(2)
    # for wf in workflows:
    #     print(f"comm: {round(wf.avg_com_cost, 3)} comp: {round(wf.avg_comp_cost, 3)} ccr: {round(wf.ccr, 3)}")
    # schedules, _, machines = run_sim(run_methods[0], machines, workflows, visuals=True, show_fig=True, save_sim=True)
    # run_methods = sum(run_methods, [])

    # run_methods = HOLE_METHOD_VARIATIONS["holes-2011-BEST-FIT"]
    # run_methods = HOLE_METHOD_VARIATIONS["holes-2011-WORST-FIT"]
    # run_methods = HOLE_METHOD_VARIATIONS["holes-2011-FIRST-FIT"]
    # run_methods = ["holes EFT-EST", "holes EST-EFT", "holes EFT-EFT", "holes EST-EST", "holes LST-EFT", "holes LST-EST", "holes LFT-EST", "holes LFT-EFT", "holes LST-LST", "holes LFT-LFT"]
    # print(f"\n\n\t\tFOR N = {n}")
    # run_sim(run_methods=run_methods, load_example=True, visuals=True, save_fig=False, show_fig=True)
    # run_n_sims([50], run_methods, ns_machines=[4], save_sim=False)
    # run_save_n_sims_to_excel([5, 10, 15, 20, 25, 30, 35], run_methods)