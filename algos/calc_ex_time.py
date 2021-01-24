
# Running this function means we already have
# as a fact that all the parent tasks are done
# before we get in here and check for the slowest parent
def compute_execution_time(task, machine):
    # TODO: Maybe can just change this to DummyIn
    #       not worth changing atm...
    if task.name.startswith('Dummy'):
        # This is only for the dummy OUT node
        if task.is_exit_task is True:
            return [machine.schedule_len, machine.schedule_len]
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
        communication_time = machine.calc_com_cost(communication_time)

    #  parent_end + communication_time + cost_of_task_in_this_machine
    # We pick the one that is bigger so we can ensure the child task starts
    # after the parent.
    start = max(task.slowest_parent['parent_task'].end + communication_time, machine.schedule_len)
    end = start + task.costs[machine.id]
    return [start, end]


def compute_execution_time_genetics(task_copy, machine, tasks, copied_tasks):
    task = tasks[task_copy["id"]]
    slowest_parent_copy = copied_tasks[task_copy["slowest_parent"]["parent_id"]]
    if task.name.startswith('Dummy'):
        # This is only for the dummy OUT node
        if task.is_exit_task is True:
            return [machine.schedule_len, machine.schedule_len]
        # This is only for the dummy IN node
        else:
            return [0, 0]
        # If between the child and the parent the machine doesn't change
        # then the communication cost is 0.
    elif task.is_entry_task:
        return [machine.schedule_len, machine.schedule_len + task.costs[machine.id]]
    elif slowest_parent_copy["machine_id"] == machine.id:
        communication_time = 0
    else:
        # The communication_time in kbs
        communication_time = task_copy["slowest_parent"]["com_time"]
        # Get the time that is needed based on the machine network.
        communication_time = machine.calc_com_cost(communication_time)

    #  parent_end + communication_time + cost_of_task_in_this_machine
    # We pick the one that is bigger so we can ensure the child task starts
    # after the parent.
    start = max(slowest_parent_copy["end"] + communication_time, machine.schedule_len)
    end = start + task.costs[machine.id]
    return [start, end]
