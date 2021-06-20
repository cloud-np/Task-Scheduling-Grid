from simulation.simulation import run_simulation
from example_data import HOLE_METHOD_VARIATIONS

if __name__ == "__main__":

    # Variations. This should be its own file.
    #    {"name": "c1", "time_types": ["EST"], "fill_type": "NO-FILL"},
    #    {"name": "c2", "time_types": ["EST"], "fill_type": "NO-FILL"},
    #    {"name": "c3", "time_types": ["EST"], "fill_type": "NO-FILL"}]
    run_methods = HOLE_METHOD_VARIATIONS["EFT_variations"]
    # run_methods = ["holes EFT-EST", "holes EST-EFT", "holes EFT-EFT", "holes EST-EST", "holes LST-EFT", "holes LST-EST", "holes LFT-EST", "holes LFT-EFT", "holes LST-LST", "holes LFT-LFT"]
    # visuals = True
    visuals = False
    # print("\n\n\t\tFOR N = 5")
    # run_simulation(5, run_methods, visuals)
    print("\n\n\t\tFOR N = 10")
    run_simulation(10, run_methods, visuals)
    # print("\n\n\t\tFOR N = 20")
    # run_simulation(20, run_methods, visuals)
    # run_simulation(20, run_methods=["c3"], visuals=False)
