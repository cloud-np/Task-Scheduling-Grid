from classes.Task import TaskStatus
from algos.calculate_task_ranks import calculate_upward_ranks
from random import randint
from algos.calc_ex_time import compute_execution_time, compute_execution_time_genetics


def pick_machine_for_task(task, machines):
    # We pick the "first" available machine
    machine = min(machines, key=lambda m: m.schedule_len)
    tmp_time = compute_execution_time(task, machine)
    return machine, tmp_time


def get_best_machine_for_task(task, machines):
    times = list()
    for machine in machines:
        tmp_time = compute_execution_time(task, machine)
        times.append((machine, tmp_time))
    min_time = min(times, key=lambda tup: tup[1][1])
    return min_time[0], min_time[1]
# 1st
# Return a 2D array of strings. Each row represents a machines e.g:
# M0 [ 2 ] [ 8 ] [ 1 ] [ 9 ]
# M1 [ 5 ] [ 6 ] [ 4 ]
# M2 [ 7 ] [ 0 ] [ 3 ]
# def schedule_genetic_wf(tasks, machines, schedule_type="random"):
#     wf = [list() for _ in machines]
#
#     if schedule_type == "random":
#         # Pick a random machine row and append the task id
#         unscheduled_tasks = list(tasks)
#         while unscheduled_tasks:
#             # Remove an unscheduled task and add it to a random machine.
#             tmp_task = unscheduled_tasks.pop(randint(0, len(unscheduled_tasks) - 1))
#             wf[randint(0, len(machines) - 1)].append(f'T{tmp_task.id}')
#         return wf
#     elif schedule_type == "b-level":
#         raise Exception("Not Implemented yet!")
#     elif schedule_type == "t-level":
#         raise Exception("Not Implemented yet!")


# 2nd
def schedule_genetic_wf(copied_tasks, tasks, machines, schedule_type="random"):
    tasks_added = 0
    tasks_len = len(tasks)
    machines_len = len(machines)
    if schedule_type == "random":
        while tasks_added < tasks_len:
            # Pick and random task every time to try and add
            task = tasks[randint(0, tasks_len - 1)]
            machine = machines[randint(0, machines_len - 1)]
            if try_schedule_g_task(task, machine, copied_tasks, tasks):
                tasks_added += 1

    elif schedule_type == "b-level":
        calculate_upward_ranks(tasks)
        copied_tasks = [{"t_id": task.id,
                         "start": -1,
                         "end": -1,
                         "up_rank": task.up_rank} for task in tasks]
        copied_tasks.sort(reverse=True, key=lambda s_task: s_task["up_rank"])

        # raise Exception("Not Implemented yet!")
    elif schedule_type == "t-level":
        raise Exception("Not Implemented yet!")
    else:
        raise ValueError("Please specify a valid schedule-type for genetics!")


# Because we don't want to copy the whole Task class we make a shallow copy of it and keep some
# new info about it like the "start" and "end" time. So one idea (which I don't like much..) is
# to access the originals tasks to get the parents/children etc and use their id's to check in
# the copied list the variables we want..I did that so I can access them in O(1) instead of searching
# each task in O(n). BUT this works ONLY if you use the SAME wf and
# not multiple AND if you do not change the order of BOTH lists.
def try_schedule_g_task(task_copy, machine, copied_tasks, tasks):
    for parent_edge in tasks[task_copy["t_id"]].parents_edges:
        p_task = copied_tasks[parent_edge.node.id]
        if p_task["machine_id"] == -1:
            return False

    # Calculate the start time of the task
    task_copy["start"], task_copy["end"] = compute_execution_time_genetics(task_copy, machine, tasks)
    # Schedule it!
    machine.add_task(tasks[task_copy["id"]])

    # Update children slowest_parent
    raise Exception("Not Implemented Yet")
    # return True


def schedule_tasks(unscheduled, machines):
    i = 0
    for task in unscheduled:
        time_and_machine = get_best_machine_for_task(task, machines)
        # min_time[0] -> Machine
        # min_time[1] -> (start_time, end_time)
        schedule_task({'start': time_and_machine[1][0],
                       'end': time_and_machine[1][1]}, task,
                      machine=time_and_machine[0])
        i += 1

    # for task in unscheduled:
    #     print(f'{task} --- p: {task.parent_node.id}')


def schedule_tasks_for_cpop(machines, queue, critical_info):
    critical_path = critical_info[0]
    critical_machine_id = critical_info[1]

    while queue:
        # mpt -> max priority task
        # probably can make these two together later on
        mpt = max(queue, key=lambda t: t.priority)
        for i in range(len(queue)):
            if queue[i].id == mpt.id:
                queue.pop(i)
                break
        if mpt in critical_path:
            # Here we send on purpose only the critical_machine
            schedule_tasks([mpt], [machines[critical_machine_id]])
            # start = machines[critical_machine_id].schedule_len
            # end = start + mpt.costs[critical_machine_id]
            # schedule_task({'start': start, 'end': end}, mpt, machines[critical_machine_id])

        else:
            # You run schedule_tasks and you simply send just one task so it works fine.
            schedule_tasks([mpt], machines)
        for child_edge in mpt.children_edges:
            child = child_edge.node
            # The status of the child gets updated by the parent. In more details the every task
            # has a counter called "parents_till_ready" every parent that gets scheduled reduce
            # this value by once for his children.
            if child.status == TaskStatus.READY:
                queue.append(child)


def schedule_task(min_time, task, machine):
    task.machine_id = machine.id
    task.start = min_time['start']
    task.end = min_time['end']
    task.update_children_and_self_status()

    machine.add_task(task)


def pick_machine_for_critical_path(critical_path, machines):
    machines_costs = list()
    for machine in machines:
        machine_critical_cost = 0
        for task in critical_path:
            machine_critical_cost += task.costs[machine.id]
        machines_costs.append((machine_critical_cost, machine.id))

    # Machine selected for the critical path
    return min(machines_costs, key=lambda tup: tup[0])[1]


def create_critical_path(tasks):
    critical_path = list()
    entry_task = None
    # Find an entry task
    for task in tasks:
        if task.is_entry_task:
            entry_task = task
            break

    entry_priority = round(entry_task.priority, 5)
    temp_task = entry_task
    critical_path.append(temp_task)

    # Start from an entry task and run until you find an exit task.
    # Then the critical path would be ready.
    while temp_task.is_exit_task is False:
        for child_edge in temp_task.children_edges:
            if round(child_edge.node.priority, 5) == entry_priority:
                temp_task = child_edge.node
                critical_path.append(child_edge.node)
                break

    # The second return is supposed to be the initialised
    return critical_path, [entry_task]

