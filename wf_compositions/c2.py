import classes.workflow as wf
from algos.heuristic import heft

# C2 From paper: Scheduling Multiple DAGs onto Heterogeneous Systems


def multiple_workflows_c2(workflows, machines):
    # 1. Connect all workflows with one "BIG" entry node and one "BIG" exit node.
    all_tasks = wf.Workflow.connect_wfs(workflows, machines)
    # 2. Get the level for each task.
    levels = wf.Workflow.level_order(all_tasks)

    # 3. Schedule based of the order of their level
    # Maybe we should run heft based of how many levels we have.
    for level, tasks in levels.items():
        if len(tasks) != 0:
            heft(tasks, machines)
