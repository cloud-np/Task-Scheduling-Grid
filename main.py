from testing.simulation import run_simulation

if __name__ == "__main__":

    run_methods = [{"name": "holes FASTEST-FIT", "time_types": ["EST", "EST"], "fill_type": "FASTEST-FIT"},
                   {"name": "holes BEST-FIT", "time_types": ["EST", "EST"], "fill_type": "BEST-FIT"},
                   {"name": "holes FIRST-FIT", "time_types": ["EST", "EST"], "fill_type": "FIRST-FIT"},
                   {"name": "holes WORST-FIT", "time_types": ["EST", "EST"], "fill_type": "WORST-FIT"},
                #    {"name": "c1", "time_types": ["EST"], "fill_type": "NO-FILL"},
                #    {"name": "c2", "time_types": ["EST"], "fill_type": "NO-FILL"},
                #    {"name": "c3", "time_types": ["EST"], "fill_type": "NO-FILL"}]
    # run_methods = ["holes EFT-EST", "holes EST-EFT", "holes EFT-EFT", "holes EST-EST", "holes LST-EFT", "holes LST-EST", "holes LFT-EST", "holes LFT-EFT", "holes LST-LST", "holes LFT-LFT"]
    visuals = True
    # visuals = False
    print("\n\n\t\tFOR N = 5")
    run_simulation(5, run_methods, visuals)
    print("\n\n\t\tFOR N = 10")
    run_simulation(10, run_methods, visuals)
    print("\n\n\t\tFOR N = 20")
    run_simulation(20, run_methods, visuals)
    # run_simulation(20, run_methods=["c3"], visuals=False)
