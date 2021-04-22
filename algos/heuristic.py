from algos.calculate_task_ranks import calculate_upward_ranks
import algos.schedule_wfs_and_tasks as scheduler 
# from algos.schedule_wfs_and_tasks import schedule_tasks_heft, schedule_tasks_round_robin_heft, \
#     schedule_tasks_cpop, pick_machine_for_critical_path


def heft(tasks, machines):

    # Phase 1
    calculate_upward_ranks(tasks)
    # We sort the tasks based of their up_rank
    tasks.sort(key=lambda task: task.up_rank, reverse=True)
    # Phase 2
    scheduler.schedule_tasks_heft(tasks, machines)
    return {'tasks': tasks, 'machines': machines}


def round_robin_heft(tasks, machines, n_wfs):
    calculate_upward_ranks(tasks)
    tasks.sort(key=lambda task: task.up_rank, reverse=True)

    scheduler.schedule_tasks_round_robin_heft(tasks, machines, n_wfs)

    return {'tasks': tasks, 'machines': machines}


def cpop(wf):
    critical_path, [entry_node, _] = wf.create_critical_path()
    critical_machine_id = scheduler.pick_machine_for_critical_path(
        critical_path, wf.machines)
    scheduler.schedule_tasks_cpop(
        wf.machines, [entry_node], (critical_path, critical_machine_id))
    return {'tasks': wf.tasks, 'machines': wf.machines}
