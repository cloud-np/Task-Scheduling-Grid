from algos.heuristic import multiple_workflows_scheduling
from classes.Task import TaskStatus
from classes.Machine import Machine
from classes.Workflow import Workflow

if __name__ == "__main__":
    # # 4. Add the dummy nodes properly
    # Task.add_dummy_nodes(tasks, machines)

    # # 5. Get the schedule from preferred algorithm.
    # schedule = heft(tasks, machines)
    # schedule = example_heft()
    # workflows = Workflow.generate_multiple_workflows(n_wfs=20, user_set_tasks=20)
    # workflows = Workflow.generate_multiple_workflows(n_wfs=20, machines=machines)
    machines = Machine.get_4_machines()
    workflows = Workflow.load_example_workflows(machines=machines)

    # for wf in workflows:
    # for task in workflows[3].tasks:
    #     for child in task.children_edges:
    #         print(f"{task} child --> {child.node} weight: {child.weight}")
    #

    multiple_workflows_scheduling(workflows, machines)
    max_machine = max(machines, key=lambda m: m.schedule_len)
    for machine in machines:
        print(machine)

    print(f'\n\n{max_machine.str_id()}\n{max_machine.str_schedule_len()}')

    # for wf in workflows:
    #     for task in wf.tasks:
    #         if task.machine_id == -1:
    #             print(f"MACHINE_ID: {task}")

    # print(len(workflows))
    # wf = Workflow(id_=0, file_data='datasets/epigenomics-workflow.json')

    # workflows = bga()
    # cpop(wf.tasks, wf.machines)
    # for wf in workflows:
    #     wf.avg_comp_cost()
    #     check_workflow(wf)
    # check_workflow(wfi
