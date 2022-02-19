from helpers.examples.example_data import HOLE_METHOD_VARIATIONS
# from helpers.visuals.visualize import Visualizer
from helpers.examples.example_gen import ExampleGen
<<<<<<< HEAD
from helpers.simulation.simulation import Simulation, save_sims_to_excel
from classes.scheduler import FillMethod
from helpers.pick_best_method import find_seed_for, find_c1_example
=======
from helpers.simulation.simulation import Simulation
>>>>>>> testing


if __name__ == "__main__":

<<<<<<< HEAD
    # Variations. This should be its own file.
    #    {"name": "c1", "time_types": ["EST"], "fill_type": "NO-FILL"},
    #    {"name": "c2", "time_types": ["EST"], "fill_type": "NO-FILL"},
    #    {"name": "c3", "time_types": ["EST"], "fill_type": "NO-FILL"}]
    # run_methods = [HOLE_METHOD_VARIATIONS["EFT_variations"], HOLE_METHOD_VARIATIONS["compositions"], HOLE_METHOD_VARIATIONS['holes-paper-2011']]
    # run_methods = [HOLE_METHOD_VARIATIONS["EFT_variations"]]
    # run_methods = [HOLE_METHOD_VARIATIONS["compositions"], HOLE_METHOD_VARIATIONS['criticals_unsorted']]
    # run_methods = [HOLE_METHOD_VARIATIONS["compositions"], HOLE_METHOD_VARIATIONS['criticals_unsorted']]
    # run_methods = [{"name": "c1", "time_types": ["EST"], "fill_type": "NO-FILL"}]
    # run_methods = sum(run_methods, [])
=======
    # variations. this should be its own file.
    #    {"name": "c1", "time_types": ["est"], "fill_type": "no-fill"},
    #    {"name": "c2", "time_types": ["est"], "fill_type": "no-fill"},
    #    {"name": "c3", "time_types": ["est"], "fill_type": "no-fill"}]
    # run_methods = [HOLE_METHOD_VARIATIONS["EFT_variations"]]
    run_methods = [HOLE_METHOD_VARIATIONS["compositions"]]
    run_methods = [HOLE_METHOD_VARIATIONS["criticals_sorted"], HOLE_METHOD_VARIATIONS["criticals_unsorted"]]

    # run_methods = [{"name": "crit_u best-fit", "fill_type": "best-fit"}]
    run_methods = sum(run_methods, [])
>>>>>>> testing
    # run_methods = HOLE_METHOD_VARIATIONS["EFT_variations"]
    # run_methods = [{"name": "holes2011 FASTEST-EDF", "fill_type": "FASTEST-FIT", "priority_type": "EDF"}]
    # for wf_size in [50, 100, 200, 300, 400, 500, 1000]:
    # for wf_size in [5, 10, 20, 30, 50]:
    # schedulers = []
    # n = 8
    # ss = []
# for n in [1, 2]:
<<<<<<< HEAD
    # for n_machines in [4, 8]:
    #     for network in [12]:
    #         # machines, workflows = ExampleGen.load_random_wfs([n_machines, network * 125], wf_size)
    #         machines, workflows = ExampleGen.load_all_types([n_machines, network * 125], 100, n_times=n)
    #         print(f"n-wfs: {n} machines: {n_machines}  network: {network}")
    #         # Simulation(run_methods, machines, workflows, visuals=False, save_fig=False, show_fig=True, save_sim=True, show_machines=False).run()
    #         ss = Simulation(run_methods, machines, workflows, visuals=False, save_fig=False, show_fig=False, save_sim=True, show_machines=False).run()
    #         for s in ss:
    #             print(s)
=======
    for n_machines in [8]:
        for network in [50]:
            machines, workflows = ExampleGen.load_random_wfs([n_machines, network * 125], 10)
            # machines, workflows = ExampleGen.load_all_types([n_machines, network * 125], 100, n_times=n)
            print(f"n-wfs: {n} machines: {n_machines}  network: {network}")
            # Simulation(run_methods, machines, workflows, visuals=False, save_fig=False, show_fig=True, save_sim=True, show_machines=False).run()
            ss = Simulation(run_methods, machines, workflows, visuals=True, save_fig=False, show_fig=True, save_sim=False, show_machines=True).run()
            for s in ss:
                print(s)
>>>>>>> testing
    # ss = sum(ss, ())
    # save_sims_to_excel(ss, n)
    # for [FillMethod.BEST_FIT, FillMethod.FASTEST_FIT, FillMethod.]
    # seed, wfs = find_seed_for(FillMethod.BEST_FIT, starting_seed=0)
    # # print(seed)
    # for t in wfs[1].tasks:
    #     print(t)
    #     for e in t.children_edges:
    #         print(f"\t{e.weight}")

    # for t in wfs[1].tasks:
    #     print(t)
    #     for e in t.children_edges:
    #         print(f"\t{e.weight}")
    # schedulers = sum(schedulers, [])
    # save_sims_to_excel(schedulers, 7 * n)
    #     for network in [50, 500]:
    #         for n_cores in [4, 8, 16, 32]:
    #             # machines = Machine.load_n_static_machines(n_cores, network * 125)
    #             # workflows = Workflow.load_random_workflows(machines, wf_size)
    #             machines, workflows = Example.load_all_types([n_cores, network * 125], wf_size)
    #             Simulation(run_methods, machines, workflows, visuals=False, save_fig=False, show_fig=True, save_sim=True, show_machines=False).run()
    # avg_makespan from both for each bin packing method

    # FIRST-FIT 89
    # FASTEST-FIT 172
    # BEST-FIT 1
    # WORST-FIT 0
    _iter, schedulers = find_c1_example()
    print(_iter)
    # _iter, min_s, schedulers = find_seed_for(FillMethod.NO_FILL, starting_seed=0)
    for t in schedulers[0].workflows[0].tasks:
        print(t.runtime, end=" ")
        print(t)
    for s in schedulers:
        # if min_s is s:
        #     continue
        print(s)
        for t in s.workflows[1].tasks:
            print(t.runtime, end=" ")
            print(t)
    # machines, workflows = Example.load_all_types([4, 35], 100)
    # Simulation(run_methods, machines, workflows, visuals=False, save_fig=False, show_fig=True, save_sim=True, show_machines=True).run()

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
