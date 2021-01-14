import copy
from algos.calculate_task_ranks import calculate_upward_ranks, calculate_downward_ranks
from algos.schedule_tasks import *


def heft(tasks, machines):

    # Phase 1
    calculate_upward_ranks(tasks)
    # We sort the tasks based of their up_rank
    tasks.sort(key=lambda task: task.up_rank, reverse=True)
    # Phase 2
    schedule_tasks(tasks, machines)
    return {'tasks': tasks, 'machines': machines}

# def example_heft():
#     tasks, machines = setup_data_example()
#
#     # Phase 1
#     calculate_upward_ranks(tasks)
#     # We sort the tasks based of their up_rank
#     tasks.sort(key=lambda task: task.up_rank, reverse=True)
#     # Phase 2
#     schedule_tasks(tasks, machines)
#     return {'tasks': tasks, 'machines': machines}


def cpop(tasks, machines):
    # Calculate downward and upward ranks
    calculate_downward_ranks(tasks)
    calculate_upward_ranks(tasks)
    for task in tasks:
        task.set_priority(task.down_rank + task.up_rank)

    critical_path, queue = create_critical_path(tasks)
    critical_machine_id = pick_machine_for_critical_path(critical_path, machines)
    schedule_tasks_for_cpop(machines, queue, (critical_path, critical_machine_id))
    return {'tasks': tasks, 'machines': machines}
