from helpers.examples.example_gen import ExampleGen
from copy import copy
from classes.scheduler import Scheduler, get_time_type, get_fill_method, get_priority_type


# find_wf(wf_id, workflows)
def optimize_schedule(workflows, machines, best_sch):
    # 1. Get the order that the workflows got scheduled.
    order = copy(best_sch.schedule_order)
    # print(best_sch.schedule_order)
    j = i = 0
    pairs = []
    while i < len(workflows) - 1:
        if (j, i + 1) in pairs:
            i += 1
            continue
        order[j], order[i + 1] = order[i + 1], order[j]
        best_sch, is_better = try_update_best_schedule(workflows, machines, best_sch, order)
        if is_better:
            pairs.append((j, i + 1))
            if j + 2 < len(workflows):
                j += 1
                i = 0
        i += 1

    return best_sch, bool(best_sch.name.startswith('ordered'))


def try_update_best_schedule(workflows, machines, best_sch, order):
    new_workflows, new_machines = ExampleGen.re_create_example(workflows, machines)
    sch_name = f'ordered {best_sch.name}' if not best_sch.name.startswith('ordered') else best_sch.name
    ordered_sch = Scheduler(sch_name, data=[new_workflows, new_machines], schedule_order=order, time_types=best_sch.time_types_str, fill_method=best_sch.fill_method_str, priority_type=best_sch.priority_type_str)
    ordered_sch.run()
    if best_sch.schedule_len > ordered_sch.schedule_len:
        return ordered_sch, True
    return best_sch, False


def find_wf(wf_id, workflows):
    wf = [_wf for _wf in workflows if _wf.id == wf_id]
    if len(wf) != 1:
        raise Exception('Found 0 or more than 1 workflow with the one id.')
    return wf[0]
