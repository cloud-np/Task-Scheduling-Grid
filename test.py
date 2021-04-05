from classes.Workflow import Workflow
from classes.Machine import Machine
from algos.heuristic import multiple_workflows_c4, multiple_workflows_c1, multiple_workflows_c2, multiple_workflows_c3
from algos.heuristic import heft
from colorama import Fore, Back
from helpers.visualize import Visualizer


if __name__ == "__main__":

    machines = Machine.load_4_machines()
    workflows = Workflow.load_paper_example_workflows(machines)
    # workflows = Workflow.load_example_workflows(machines, n=5)
    # for task in workflows[1].tasks:
    #     if task.name == 'B1':
    #         for edge in task.children_edges:
    #             print(edge)

    print(f"\t{Back.MAGENTA}METHOD USED: {Fore.LIGHTYELLOW_EX}C4{Fore.RESET}{Back.RESET}")
    schedule = multiple_workflows_c4(workflows, machines)
    # schedule = heft(tasks=workflows[1].tasks, machines=machines)
    # multiple_workflows_c1(workflows, machines)
    max_machine = max(machines, key=lambda m: m.schedule_len)

    print(f'\n{max_machine.str_id()}\n{max_machine.str_schedule_len()}')
    # for machine in machines:
    #     print(machine.str_colored())
    # print(f'\n{max_machine.str_id()}\n{max_machine.str_schedule_len()}')
    # Visualizer.visualize_machines(machines)
    # Visualizer.visualize_tasks(schedule['tasks'])
