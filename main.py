from algos.heuristic import multiple_workflows_scheduling, \
    multiple_workflows_c1, \
    multiple_workflows_c2, \
    multiple_workflows_c3, \
    multiple_workflows_c4
from classes.Task import TaskStatus
from classes.Machine import Machine
from classes.Workflow import Workflow
from helpers.export_schedule import create_schedule_json

if __name__ == "__main__":

    machines = Machine.get_4_machines()
    workflows = Workflow.load_example_workflows(machines=machines, is_our_method=True)
    # workflows = Workflow.load_paper_example_workflows(machines)

    # for task in workflows[0].cp_info["critical_path"]:
    #     print(task)
    # multiple_workflows_c4(workflows, machines)

    # VISUAL SCHEDULE ----------
    # schedule = {"tasks": all_tasks}
    # create_schedule_json(schedule)

    # FINAL TESTING -----------
    # is_our_method = False
    # machines = Machine.get_4_machines()
    # workflows = Workflow.load_example_workflows(machines=machines, is_our_method=is_our_method)


    # all_tasks = Workflow.connect_wfs(workflows)
    
    # if is_our_method:
    #     multiple_workflows_scheduling(workflows, machines)
    # else:
    #     multiple_workflows_c2(workflows, machines)

    # max_machine = max(machines, key=lambda m: m.schedule_len)

    # for machine in machines:
    #     print(machine)

    # if is_our_method:
    #     for machine in machines:
    #         print(f'{machine.str_id()} filled_holes: {machine.holes_filled}')
    # print(f'\n\n{max_machine.str_id()}\n{max_machine.str_schedule_len()}')