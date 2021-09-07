from helpers.simulation.simulation import run_n_sims, run_sim, run_save_n_sims_to_excel
from example_data import HOLE_METHOD_VARIATIONS

if __name__ == "__main__":

    # Variations. This should be its own file.
    #    {"name": "c1", "time_types": ["EST"], "fill_type": "NO-FILL"},
    #    {"name": "c2", "time_types": ["EST"], "fill_type": "NO-FILL"},
    #    {"name": "c3", "time_types": ["EST"], "fill_type": "NO-FILL"}]
    run_methods = HOLE_METHOD_VARIATIONS["EFT_variations"]
    # run_methods = HOLE_METHOD_VARIATIONS["holes-2011-BEST-FIT"]
    # run_methods = HOLE_METHOD_VARIATIONS["holes-2011-WORST-FIT"]
    # run_methods = HOLE_METHOD_VARIATIONS["holes-2011-FIRST-FIT"]
    # run_methods = [{"name": "holes2011 EFT-EFT", "time_types": ["EFT", "EFT"], "fill_type": "FASTEST-FIT", "priority_type": "LSTF"}]
    # run_methods = ["holes EFT-EST", "holes EST-EFT", "holes EFT-EFT", "holes EST-EST", "holes LST-EFT", "holes LST-EST", "holes LFT-EST", "holes LFT-EFT", "holes LST-LST", "holes LFT-LFT"]
    # n = 5
    # print(f"\n\n\t\tFOR N = {n}")
    # run_simulation(n, run_methods, visuals=True, save_fig=False, show_fig=False)
    # run_n_sims([5, 10], run_methods)
    run_save_n_sims_to_excel([5, 10, 15, 20, 25, 30, 35], run_methods)
