from algos.heuristic import multiple_workflows_scheduling
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
    #     for child in wf.tasks[0].children_edges:
    #         op.append(child.node)

    multiple_workflows_scheduling(workflows, machines)
    for machine in machines:
        machine.print_info()
    # for wf in sorted(workflows, key=lambda wf_: wf_.calc_ccr()):
    #     print(f"id: {wf.id} crc: {wf.calc_ccr()}")

    # for task in workflows[0].tasks:
    #     print(task.avg_cost())

    # print(len(workflows))
    # wf = Workflow(id_=0, file_data='datasets/epigenomics-workflow.json')

    # workflows = bga()
    # cpop(wf.tasks, wf.machines)
    # for wf in workflows:
    #     wf.avg_comp_cost()
    #     check_workflow(wf)
    # check_workflow(wfi
