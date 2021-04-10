from testing.simulation import run_simulation

if __name__ == "__main__":

    run_methods = ["holes", "c1", "c2", "c3"]
    # visuals = True
    visuals = False
    run_simulation(5, run_methods, visuals)
    run_simulation(10, run_methods, visuals)
    run_simulation(20, run_methods, visuals)
    # run_simulation(20, run_methods=["c3"], visuals=False)
