from compare_methods import *
from classes.Task import TaskStatus
from classes.Machine import Machine
from classes.Workflow import Workflow
from helpers.export_schedule import create_schedule_json
from helpers.visualize import Visualizer

if __name__ == "__main__":

    # VISUAL SCHEDULE ----------
    # schedule = {"tasks": all_tasks}
    # create_schedule_json(schedule)

    # FINAL TESTING -----------
    is_our_method = False
    # is_our_method = True
    # workflows = Workflow.load_paper_example_workflows(machines)
    
    slowest_machines = list()
    for name in ["holes", "c1", "c2", "c3", "c4"]:
        machines = Machine.get_4_machines()
        workflows = Workflow.load_example_workflows(machines=machines, n=5)
        run_method(name, machines, workflows)
        max_machine = max(machines, key=lambda m: m.schedule_len)
        slowest_machines.append({"machine": max_machine, "method_used": name})

        if name == "holes":
            for machine in machines:
                print(f'{machine.str_id()} filled_holes: {machine.holes_filled}')
        print(f'\n\n{max_machine.str_id()}\n{max_machine.str_schedule_len()}')

    Visualizer.compare_schedule_len(slowest_machines)

