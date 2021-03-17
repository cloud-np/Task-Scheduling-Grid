from testing.simulation import run_simulation
from compare_methods import *
from classes.Machine import Machine
from classes.Workflow import Workflow
from helpers.visualize import Visualizer

if __name__ == "__main__":

    run_methods = ["holes", "c1", "c2", "c3", "c4"]
    run_simulation(5, run_methods, True)
    run_simulation(10, run_methods, True)
    run_simulation(20, run_methods, True)
    # run_simulation(20, run_methods=["c3"], visuals=False)


