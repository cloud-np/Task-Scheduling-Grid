from algos.schedule_wfs import pick_machine_based_on_timetype
from classes.scheduler import FillMethod


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


def calc_time_on_machine(task, machines, time_type, hole_filling_type=FillMethod.NO_FILL):
    holes_times = list()
    task_times_on_machines = list()
    best_time = None
    for machine in machines:
        # Try to find the existing holes (in the current machine) to fill.
        if hole_filling_type != FillMethod.NO_FILL:
            for hole in machine.holes:
                valid_hole_info = hole.is_fillable(task, machine.id)
                if valid_hole_info is not None:
                    holes_times.append(
                        {"machine": machine, "hole": hole, **valid_hole_info})

        # If no valid holes were found try to look into the current machine
        # and find the execution time of the specific task in the machine.
        if len(holes_times) == 0:
            [start, end] = compute_execution_time(
                task, machine.id, machine.schedule_len)
            task_times_on_machines.append(
                {"machine": machine, "start": start, "end": end})

    # If there are holes to fill prioritize them.
    if len(holes_times) > 0:
        if hole_filling_type == FillMethod.FASTEST_FIT:
            best_time = pick_machine_based_on_timetype(time_type, holes_times)
        elif hole_filling_type == FillMethod.BEST_FIT:
            best_time = min(holes_times, key=lambda t: t["gap_left"])
        elif hole_filling_type == FillMethod.FIRST_FIT:
            # We could write this to run faster but I think we will losse readility
            best_time = holes_times[0]
        elif hole_filling_type == FillMethod.WORST_FIT:
            best_time = max(holes_times, key=lambda t: t["gap_left"])
    # If no holes were found.
    else:
        best_time = pick_machine_based_on_timetype(
            time_type, task_times_on_machines)

    if best_time is None:
        raise ValueError(
            f"No machine or hole in a machine was assigned to: {task}")
    return best_time
