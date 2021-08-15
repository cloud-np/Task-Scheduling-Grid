import classes.workflow as wf
from algos.heuristic import round_robin_heft

# C3 From paper: Scheduling Multiple DAGs onto Heterogeneous Systems


def multiple_workflows_c3(workflows, machines):
    # 1. Connect all workflows with one "BIG" entry node and one "BIG" exit node.
    all_tasks = wf.Workflow.connect_wfs(workflows, machines)
    # 2. Run HEFT in round-robin-fashion
    return round_robin_heft(all_tasks, machines, len(workflows))
