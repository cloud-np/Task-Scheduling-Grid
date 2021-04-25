import algos.schedule_wfs_and_tasks as scheduler


def holes_scheduling(workflows, machines, time_types, hole_filling_type):
    """This method is used to schedule with method holes.

    This basically creates the more holes it can in the schedule
    on perpuse so it can fill them later with tasks with high computation
    cost and low communication cost.

    Args:
        workflows (list(Workflow)): Contains information about the workflows.
        machines (list(Machine)): Contains information about the machines.
        time_types (list(TimeType)): Shows the time type we should use for each workflow to be schedules with. e.g: EFT - EST
    """
    sorted_wfs = sorted(workflows, key=lambda wf_: wf_.calc_ccr(), reverse=True)

    j = len(sorted_wfs) - 1
    for i in range(len(sorted_wfs) // 2):
        scheduler.schedule_workflow(sorted_wfs[i], machines, time_types[0], hole_filling_type=hole_filling_type)
        scheduler.schedule_workflow(sorted_wfs[j], machines, time_types[1], hole_filling_type=hole_filling_type)
        j -= 1

    # This is incase we have an odd number of workflows so one is left out without a pair.
    # Not the cleanest way to handle this but works for now.
    for wf in workflows:
        if wf.scheduled is False:
            scheduler.schedule_workflow(wf, machines, time_types[0], hole_filling_type=hole_filling_type)
