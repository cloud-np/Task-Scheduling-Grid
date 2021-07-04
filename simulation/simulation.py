from classes.machine import Machine
from colorama import Fore, Back
from classes.workflow import Workflow
from classes.scheduler import Scheduler
from helpers.checker import schedule_checker
from visuals.visualize import Visualizer


# TODO One idea is to pass schedule functions to the
# run() method of the Schedule obj. This sounds a bit cleaner.
# than making it pick a the correct function as init time.
def run_simulation(n, run_methods, visuals):
    # VISUAL SCHEDULE ----------
    # schedule = {"tasks": all_tasks}
    # create_schedule_json(schedule)

    # FINAL TESTING -----------
    # is_our_method = True
    # workflows = Workflow.load_paper_example_workflows(machines)

    workflows: list = list()
    slowest_machines = list()
    for method in run_methods:
        machines = Machine.load_4_machines()
        workflows = Workflow.load_example_workflows(machines=machines, n=n)
        schedule = Scheduler(name=method['name'], workflows=workflows, machines=machines, time_types=method.get("time_types"), fill_type=method["fill_type"], priority_type=method.get("priority_type"))

        schedule.run()
        schedule.info()

        slowest_machines.append({"machine": schedule.get_slowest_machine(), "method_used": schedule.method_used_info()})

    if visuals is True:
        # Visualizer.compare_schedule_len(slowest_machines, len(workflows))
        Visualizer.compare_hole_filling_methods(slowest_machines)
