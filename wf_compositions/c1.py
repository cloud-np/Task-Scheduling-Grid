import classes.workflow as wf
from algos.heuristic import heft

# C1 From paper: Scheduling Multiple DAGs onto Heterogeneous Systems


def multiple_workflows_c1(workflows, machines):
    all_tasks = wf.Workflow.connect_wfs(workflows, machines)
    return heft(all_tasks, machines)
