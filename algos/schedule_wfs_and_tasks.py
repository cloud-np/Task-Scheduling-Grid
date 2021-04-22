from classes.task import TaskStatus
from classes.schedule import FillMethod, TimeType
from algos.calc_ex_time import compute_execution_time

# TODO move to schedule.py


def pick_machine_for_task(task, machines):
    # We pick the "first" available machine
    machine = min(machines, key=lambda m: m.schedule_len)
    tmp_time = compute_execution_time(task, machine.id, machine.schedule_len)
    return machine, tmp_time


def is_hole_fillable(task, m_id, hole):
    # Check if the parent end interfere with the child start
    # pred: predicted
    pred_start, pred_end = compute_execution_time(task, m_id, hole.start)
    if pred_end <= hole.end:
        return {"start": pred_start, "end": pred_end, "gap_left": hole.gap - (pred_end - pred_start)}
    else:
        return None


def schedule_workflow(wf, machines, time_type, hole_filling_type):
    wf.scheduled = True
    for task in wf.tasks:
        schedule_task_to_best_machine(task, machines, time_type, hole_filling_type)


def schedule_tasks_round_robin_heft(unscheduled, machines, n_wfs):
    diff_wfs = set()

    i = 0
    wfs_remaining = n_wfs
    # Schedule the first connecting dag because its wf_id is -1
    schedule_task_to_best_machine(unscheduled.pop(0), machines, TimeType.EFT)
    j = 0
    while unscheduled:
        if len(unscheduled) == i:
            i = 0
        task = unscheduled[i]

        j += 1
        # Task is not ready yet go to the next one
        if task.parents_till_ready != 0 or task.wf_id in diff_wfs:
            i += 1
        else:
            schedule_task_to_best_machine(task, machines, TimeType.EFT)
            if task.name.startswith("Dummy-Out") or (task.children_names is not None and len(task.children_names)) == 0:
                wfs_remaining -= 1
            diff_wfs.add(task.wf_id)
            # print(f"Scheduled: {task}")
            # print(task.str_colored())
            unscheduled.pop(i)
            i -= 1

        # If we end up looping through all the workflows
        # then go ahead and reset the set.
        if len(diff_wfs) >= wfs_remaining:
            diff_wfs = set()


def schedule_tasks_heft(unscheduled, machines):
    for task in unscheduled:
        schedule_task_to_best_machine(task, machines, TimeType.EFT)


def schedule_tasks_cpop(machines, queue, critical_info):
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
            schedule_tasks_heft([mpt], [machines[critical_machine_id]])
        else:
            # You run schedule_tasks and you simply send just one task so it works fine.
            schedule_tasks_heft([mpt], machines)
        for child_edge in mpt.children_edges:
            child = child_edge.node
            # The status of the child gets updated by the parent. In more details the every task
            # has a counter called "parents_till_ready" every parent that gets scheduled reduce
            # this value by once for his children.
            if child.status == TaskStatus.READY:
                queue.append(child)


def pick_machine_based_on_timetype(time_type, times):
    # Prioritize to fill the holes first.
    if time_type == TimeType.EST:
        time = min(times, key=compare_start)
    elif time_type == TimeType.EFT:
        time = min(times, key=compare_end)
    elif time_type == TimeType.LST:
        time = max(times, key=compare_start)
    elif time_type == TimeType.LFT:
        time = max(times, key=compare_end)
    else:
        raise ValueError(f"This is not a valid time_type: {time_type}")
    return time


def compare_start(times):
    return times["start"]


def compare_end(times):
    return times["end"]


def get_machine_and_time(task, machines, time_type, hole_filling_type=FillMethod.NO_FILL):
    holes_times = list()
    task_times_on_machines = list()
    best_time = None
    for machine in machines:
        # Try to find the existing holes (in the current machine) to fill.
        if hole_filling_type != FillMethod.NO_FILL:
            for hole in machine.holes:
                valid_hole_info = is_hole_fillable(task, machine.id, hole)
                if valid_hole_info is not None:
                    holes_times.append({"machine": machine, "hole": hole, **valid_hole_info})

        # If no valid holes were found try to look into the current machine
        # and find the execution time of the specific task in the machine. 
        if len(holes_times) == 0:
            [start, end] = compute_execution_time(task, machine.id, machine.schedule_len)
            task_times_on_machines.append({"machine": machine, "start": start, "end": end})

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
        best_time = pick_machine_based_on_timetype(time_type, task_times_on_machines)

    if best_time is None:
        raise ValueError(f"No machine or hole in a machine was assigned to: {task}")
    return best_time


def schedule_task_to_best_machine(task, machines, time_type, hole_filling_type=FillMethod.NO_FILL):
    time_and_machine = get_machine_and_time(task, machines, time_type, hole_filling_type)

    schedule_task({'start': time_and_machine["start"],
                   'end': time_and_machine["end"]}, task,
                  machine=time_and_machine["machine"], hole=time_and_machine.get('hole'))


# This function schedules the task and returns the new
def schedule_task(sch_time, task, machine, hole):
    task.machine_id = machine.id
    task.start = sch_time['start']
    task.end = sch_time['end']
    task.update_children_and_self_status()

    if hole is None:
        machine.add_task(task)
    else:
        machine.add_task_to_hole(task, hole)


def pick_machine_for_critical_path(critical_path, machines):
    machines_costs = list()
    for machine in machines:
        machine_critical_cost = 0
        for task in critical_path:
            machine_critical_cost += task.costs[machine.id]
        machines_costs.append((machine_critical_cost, machine.id))

    # Machine selected for the critical path
    return min(machines_costs, key=lambda tup: tup[0])[1]


def construct_critical_path(tasks):
    critical_path = list()
    entry_task = None
    # Find an entry task
    for task in tasks:
        if task.is_entry:
            entry_task = task
            break

    entry_priority = round(entry_task.priority, 5)
    temp_task = entry_task
    critical_path.append(temp_task)

    # Start from an entry task and run until you find an exit task.
    # Then the critical path would be ready.
    while temp_task.is_exit is False:
        for child_edge in temp_task.children_edges:
            if round(child_edge.node.priority, 5) == entry_priority:
                temp_task = child_edge.node
                critical_path.append(child_edge.node)
                break
    exit_task = temp_task
    # The second return is supposed to be the initialised
    return critical_path, [entry_task, exit_task]
