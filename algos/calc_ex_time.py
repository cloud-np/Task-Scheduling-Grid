# Running this function means we already have
# as a fact that all the parent tasks are done
# before we get in here and check for the slowest parent
def compute_execution_time(task, m_id, start_time):
    # TODO: Maybe can just change this to DummyIn
    #       not worth looking atm...
    if task.name.startswith('Dummy'):
        # This is only for the dummy OUT node
        if task.is_exit is True:
            return [start_time, start_time]
        # This is only for the dummy IN node
        else:
            return [0, 0]
        # If between the child and the parent the machine doesn't change
        # then the communication cost is 0.
    elif task.is_entry:
        return [start_time, start_time + task.costs[m_id]]
    elif task.slowest_parent['parent_task'].machine_id == m_id:
        communication_time = 0
    else:
        # The com_time was calculated at the parsing phase.
        communication_time = task.slowest_parent['communication_time']

    #  parent_end + communication_time + cost_of_task_in_this_machine
    # We pick the one that is bigger so we can ensure the child task starts
    # after the parent.
    start = max(task.slowest_parent['parent_task'].end + communication_time, start_time)
    end = start + task.costs[m_id]
    return [start, end]
