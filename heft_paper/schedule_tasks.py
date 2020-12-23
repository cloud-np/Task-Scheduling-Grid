from classes.Task import TaskStatus


def compute_execution_time(task, machine):

    if task.name.startswith('Dummy'):
        # This is only for the dummy OUT node
        if task.is_exit_task is True:
            cost = task.slowest_parent['parent_task'].end
            return [cost, cost]
        # This is only for the dummy IN node
        else:
            return [0, 0]
        # If between the child and the parent the machine doesn't change
        # then the communication cost is 0.
    elif task.is_entry_task:
        return [machine.schedule_len, machine.schedule_len + task.costs[machine.id]]
    elif task.slowest_parent['parent_task'].machine_id == machine.id:
        communication_time = 0
    else:
        # The communication_time in kbs
        communication_time = task.slowest_parent['communication_time']
        # Get the time that is needed based on the machine network.
        communication_time = machine.calc_communication_cost(communication_time)

    #  parent_end + communication_time + cost_of_task_in_this_process
    # We pick the one that is bigger so we can ensure the child task starts
    # after the parent.
    start = max(task.slowest_parent['parent_task'].end + communication_time, machine.schedule_len)
    end = start + task.costs[machine.id]
    return [start, end]


def schedule_tasks(unscheduled, machines):
    i = 0
    for task in unscheduled:
        times = list()
        for machine in machines:
            tmp_time = compute_execution_time(task, machine)
            times.append((machine, tmp_time))
        min_time = min(times, key=lambda tup: tup[1][1])
        # min_time[0] -> Machine
        # min_time[1] -> (start_time, end_time)
        schedule_task({'start': min_time[1][0], 'end': min_time[1][1]}, task, machine=min_time[0])
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

