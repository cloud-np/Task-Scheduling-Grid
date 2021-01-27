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


def schedule_workflow(wf, machines):
    schedule_tasks_for_heft(wf.tasks, machines)


def schedule_tasks_for_heft(unscheduled, machines):
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
            schedule_tasks_for_heft([mpt], [machines[critical_machine_id]])
            # start = machines[critical_machine_id].schedule_len
            # end = start + mpt.costs[critical_machine_id]
            # schedule_task({'start': start, 'end': end}, mpt, machines[critical_machine_id])

        else:
            # You run schedule_tasks and you simply send just one task so it works fine.
            schedule_tasks_for_heft([mpt], machines)
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

