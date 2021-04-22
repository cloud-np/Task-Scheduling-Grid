from classes.Machine import Machine
from colorama import Fore, Back
from classes.Workflow import Workflow
from classes.Schedule import Schedule
from helpers.visualize import Visualizer


def run_simulation(n, run_methods, visuals):
    # VISUAL SCHEDULE ----------
    # schedule = {"tasks": all_tasks}
    # create_schedule_json(schedule)

    # FINAL TESTING -----------
    # is_our_method = True
    # workflows = Workflow.load_paper_example_workflows(machines)

    slowest_machines = list()
    for method in run_methods:
        machines = Machine.load_4_machines()
        workflows = Workflow.load_example_workflows(machines=machines, n=n)
        schedule = Schedule(name=method['name'], workflows=workflows, machines=machines, time_types=method["time_types"], fill_type=method["fill_type"])

        schedule.run()
        schedule.info()

        slowest_machines.append({"machine": schedule.get_slowest_machine(), "method_used": schedule.method_used_info()})

    if visuals is True:
        Visualizer.compare_schedule_len(slowest_machines, len(workflows))
