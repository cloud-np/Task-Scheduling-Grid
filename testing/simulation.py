from compare_methods import run_method
from classes.Machine import Machine
from colorama import Fore, Back
from classes.Workflow import Workflow
from helpers.visualize import Visualizer


def run_simulation(n, run_methods, visuals):
    # VISUAL SCHEDULE ----------
    # schedule = {"tasks": all_tasks}
    # create_schedule_json(schedule)

    # FINAL TESTING -----------
    # is_our_method = True
    # workflows = Workflow.load_paper_example_workflows(machines)

    slowest_machines = list()
    for name in run_methods:
        machines = Machine.load_4_machines()
        workflows = Workflow.load_example_workflows(machines=machines, n=n)
        run_method(name, machines, workflows)
        max_machine = max(machines, key=lambda m: m.schedule_len)
        slowest_machines.append({"machine": max_machine, "method_used": name})

        if name == "holes":
            for machine in machines:
                print(f'{machine.str_id()} filled_holes: {machine.holes_filled}')
        print(f"\t{Back.MAGENTA}METHOD USED: {Fore.LIGHTYELLOW_EX}{name}{Fore.RESET}{Back.RESET}")
        print(f'\n{max_machine.str_id()}\n{max_machine.str_schedule_len()}')

    if visuals is True:
        Visualizer.compare_schedule_len(slowest_machines)
