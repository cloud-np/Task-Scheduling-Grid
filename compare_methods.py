from algos.heuristic import multiple_workflows_scheduling, \
    multiple_workflows_c1, \
    multiple_workflows_c2, \
    multiple_workflows_c3, \
    multiple_workflows_c4


def run_method(pick, machines, workflows):
    if pick == "holes":
        method = multiple_workflows_scheduling
    elif pick == "c1":
        method = multiple_workflows_c1
    elif pick == "c2":
        method = multiple_workflows_c2
    elif pick == "c3":
        method = multiple_workflows_c3
    elif pick == "c4":
        method = multiple_workflows_c4
    else:
        raise ValueError(f"Not a valid method option: {pick}")

    method(workflows, machines)
