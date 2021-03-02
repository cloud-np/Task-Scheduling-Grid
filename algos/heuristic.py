from algos.calculate_task_ranks import calculate_downward_ranks, calculate_upward_ranks
from classes.Workflow import Workflow
from typing import List
from algos.schedule_wfs_and_tasks import *


def heft(tasks, machines):

    # Phase 1
    calculate_upward_ranks(tasks)
    # We sort the tasks based of their up_rank
    tasks.sort(key=lambda task: task.up_rank, reverse=True)
    # Phase 2
    schedule_tasks_heft(tasks, machines)
    return {'tasks': tasks, 'machines': machines}


def round_robin_heft(tasks, machines, n_wfs):
    calculate_upward_ranks(tasks)
    tasks.sort(key=lambda task: task.up_rank, reverse=True)

    schedule_tasks_round_robin_heft(tasks, machines, n_wfs)

    return {'tasks': tasks, 'machines': machines}


# C1 From paper: Scheduling Multiple DAGs onto Heterogeneous Systems
def multiple_workflows_c1(workflows, machines):
    all_tasks = Workflow.connect_wfs(workflows)
    return heft(all_tasks, machines)


# C2 From paper: Scheduling Multiple DAGs onto Heterogeneous Systems
def multiple_workflows_c2(workflows, machines):
    # 1. Connect all workflows with one "BIG" entry node and one "BIG" exit node.
    all_tasks = Workflow.connect_wfs(workflows)
    # 2. Get the level for each task.
    levels = Workflow.level_order(all_tasks)

    # 3. Schedule based of the order of their level
    # Maybe we should run heft based of how many levels we have.
    for level, tasks in levels.items():
        for task in tasks:
            # HEFT
            pass


def multiple_workflows_c3(workflows, machines):
    # 1. Connect all workflows with one "BIG" entry node and one "BIG" exit node.
    all_tasks = Workflow.connect_wfs(workflows)
    # 2. Run HEFT in round-robin-fashion
    round_robin_heft(all_tasks, machines, len(workflows))


def multiple_workflows_scheduling(workflows, machines):
    sorted_wfs: List[Workflow] = sorted(workflows, key=lambda wf_: wf_.calc_ccr(), reverse=True)

    j = len(sorted_wfs) - 1
    for i in range(int(len(sorted_wfs) / 2)):
        schedule_workflow(sorted_wfs[i], machines, TimeType.EFT, try_fill_hole=True)
        schedule_workflow(sorted_wfs[j], machines, TimeType.EST, try_fill_hole=True)
        j -= 1


def cpop(tasks, machines):
    # Calculate downward and upward ranks
    calculate_downward_ranks(tasks)
    calculate_upward_ranks(tasks)
    for task in tasks:
        task.set_priority(task.down_rank + task.up_rank)

    critical_path, queue = create_critical_path(tasks)
    critical_machine_id = pick_machine_for_critical_path(critical_path, machines)
    schedule_tasks_cpop(machines, queue, (critical_path, critical_machine_id))
    return {'tasks': tasks, 'machines': machines}
