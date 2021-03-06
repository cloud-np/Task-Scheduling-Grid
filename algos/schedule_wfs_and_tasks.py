from classes.Task import TaskStatus
from enum import Enum
from algos.calc_ex_time import compute_execution_time


class TimeType(Enum):
    EST = 0
    EFT = 1
    LST = 2
    LFT = 3


def pick_machine_for_task(task, machines):
    # We pick the "first" available machine
    machine = min(machines, key=lambda m: m.schedule_len)
    tmp_time = compute_execution_time(task, machine.id, machine.schedule_len)
    return machine, tmp_time


def is_hole_fillable(task, m_id, hole):
    # Check if the parent end interfere with the child start
    # pred: predicted
    [pred_start, pred_end] = compute_execution_time(task, m_id, hole.start)
    if pred_end <= hole.end:
        return True, [pred_start, pred_end]
    else:
        return False, [-1 , -1]


def comp_st(times):
    return times[1]["start"]


def comp_ft(times):
    return times[1]["end"]


def schedule_workflow(wf, machines, time_type, try_fill_hole):
    for task in wf.tasks:
        schedule_task_to_best_machine(task, machines, time_type, try_fill_hole)


# TimeType.EFT
# FIXME Way to slow.
def schedule_tasks_round_robin_heft(unscheduled, machines, n_wfs):
    diff_wfs = set()

    skip_robin = False
    i = 0
    while unscheduled:
        old_len = len(unscheduled)
        task = unscheduled[i]

        # Task is not ready yet
        if task.parents_till_ready != 0:
            i += 1
            continue

        if skip_robin or (task.wf_id not in diff_wfs):
            schedule_task_to_best_machine(task, machines, TimeType.EFT)
            if task.name.startswith("Dummy"):
                diff_wfs.add(task.wf_id)
            print(f"Scheduled: {task}")
            unscheduled.pop(i)
            i -= 1

        # If we end up looping through all the workflows
        # then go ahead and reset the set.
        if len(diff_wfs) == n_wfs:
            i = 0
            diff_wfs = set()

        if old_len == len(unscheduled):
            skip_robin = True
        else:
            skip_robin = False


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
            # start = machines[critical_machine_id].schedule_len
            # end = start + mpt.costs[critical_machine_id]
            # schedule_task({'start': start, 'end': end}, mpt, machines[critical_machine_id])

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


def get_machine_and_time(task, machines, time_type, try_fill_hole=False):
    holes_times = list()
    times = list()
    no_valid_holes = True
    for machine in machines:
        if try_fill_hole:
            for hole in machine.holes:
                [is_fillable, tmp_hole_time] = is_hole_fillable(task, machine.id, hole)
                if is_fillable:
                    holes_times.append((machine, {"start": tmp_hole_time[0], "end": tmp_hole_time[1], "hole": hole}))
                    no_valid_holes = False

        if no_valid_holes:
            [start, end] = compute_execution_time(task, machine.id, machine.schedule_len)
            times.append((machine, {"start": start, "end": end}))

    # Prioritize to fill the holes first.
    if time_type == TimeType.EST:
        time = min(holes_times, key=comp_st) if holes_times else min(times, key=comp_st)
    elif time_type == TimeType.EFT:
        time = min(holes_times, key=comp_ft) if holes_times else min(times, key=comp_ft)
    elif time_type == TimeType.LST:
        time = max(holes_times, key=comp_st) if holes_times else max(times, key=comp_st)
    elif time_type == TimeType.LFT:
        time = max(holes_times, key=comp_ft) if holes_times else max(times, key=comp_ft)
    else:
        raise ValueError(f"Please enter a valid time-type e.g: TimeType.EST")

    hole = time[1]["hole"] if no_valid_holes is False else None
    return time, hole


def schedule_task_to_best_machine(task, machines, time_type, try_fill_hole=False):
    time_and_machine, hole = get_machine_and_time(task, machines, time_type, try_fill_hole)
    # min_time[0] -> Machine
    # min_time[1] -> (start_time, end_time)
    schedule_task({'start': time_and_machine[1]["start"],
                   'end': time_and_machine[1]["end"]}, task,
                  machine=time_and_machine[0], hole=hole)


# This function schedules the task and returns the new
def schedule_task(sch_time, task, machine, hole=None):
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
    exit_task = temp_task
    # The second return is supposed to be the initialised
    return critical_path, [entry_task, exit_task]

