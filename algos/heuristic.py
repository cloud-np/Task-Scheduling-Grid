from algos.calculate_task_ranks import calculate_upward_ranks
from classes.Workflow import Workflow
from typing import List
from colorama import Fore
from algos.schedule_wfs_and_tasks import schedule_tasks_heft, schedule_tasks_round_robin_heft, \
    schedule_workflow, schedule_tasks_cpop, pick_machine_for_critical_path, TimeType


def heft(tasks, machines):

    # Phase 1
    calculate_upward_ranks(tasks)
    # We sort the tasks based of their up_rank
    tasks.sort(key=lambda task: task.up_rank, reverse=True)
    # Phase 2
    schedule_tasks_heft(tasks, machines)
    return {'tasks': tasks, 'machines': machines}


def round_robin_heft(tasks, machines, n_wfs):
    calculate_upward_ranks(tasks)
    tasks.sort(key=lambda task: task.up_rank, reverse=True)

    schedule_tasks_round_robin_heft(tasks, machines, n_wfs)

    return {'tasks': tasks, 'machines': machines}


# C1 From paper: Scheduling Multiple DAGs onto Heterogeneous Systems
def multiple_workflows_c1(workflows, machines):
    all_tasks = Workflow.connect_wfs(workflows, machines)
    return heft(all_tasks, machines)


# C2 From paper: Scheduling Multiple DAGs onto Heterogeneous Systems
def multiple_workflows_c2(workflows, machines):
    # 1. Connect all workflows with one "BIG" entry node and one "BIG" exit node.
    all_tasks = Workflow.connect_wfs(workflows, machines)
    # 2. Get the level for each task.
    levels = Workflow.level_order(all_tasks)

    # 3. Schedule based of the order of their level
    # Maybe we should run heft based of how many levels we have.
    for level, tasks in levels.items():
        if len(tasks) != 0:
            heft(tasks, machines)


# C3 From paper: Scheduling Multiple DAGs onto Heterogeneous Systems
def multiple_workflows_c3(workflows, machines):
    # 1. Connect all workflows with one "BIG" entry node and one "BIG" exit node.
    all_tasks = Workflow.connect_wfs(workflows, machines)
    # 2. Run HEFT in round-robin-fashion
    return round_robin_heft(all_tasks, machines, len(workflows))


# C4 From paper: Scheduling Multiple DAGs onto Heterogeneous Systems
def multiple_workflows_c4(workflows, machines):
    # Critical-path entry task
    cp_infos = sorted([{'info': wf.cp_info, 'linked': False} for wf in workflows],
                      key=lambda cp_info: cp_info['info']['entry'].up_rank, reverse=True)

    linkables = list()
    # Small half dags
    for scp in cp_infos[len(cp_infos) // 2:]:
        if scp['linked'] is True:
            continue

        scp_entry = scp['info']['entry']
        # Big half dags
        for bcp in cp_infos[:len(cp_infos) // 2]:
            bcp_entry = bcp['info']['entry']
            # Skip the same wf
            if scp['info']['entry'].wf_id == bcp['info']['entry'].id:
                continue

            for cp_task in bcp['info']['critical_path']:
                rank_diff = bcp_entry.up_rank - cp_task.up_rank
                if rank_diff >= scp_entry.up_rank:
                    linkables.append(
                        (scp_entry, cp_task, rank_diff - scp_entry.up_rank))
    for link in linkables:
        # DEBUG
        print(f"[{'A' if link[0].wf_id == 0 else 'B'}]-{link[0].str_col_id()} ---> "
              f"[{'A' if link[1].wf_id == 0 else 'B'}]-{link[1].str_col_id()} "
              f"diff = {Fore.GREEN}{link[2]}{Fore.RESET}")

    all_tasks = list()
    for wf in workflows:
        # Get the minimum link
        min_link = get_min_link_for_wf(linkables, wf)
        if min_link is not None:
            create_link(min_link, wf)
        all_tasks.extend(wf.tasks)
    return heft(all_tasks, machines)


def c4_heft(all_tasks, machines):
    pass


def create_link(min_link, small_wf):
    small_dag_task = small_wf.cp_info['entry']
    big_dag_task = min_link[1]

    small_dag_task.add_child(0, big_dag_task)
    big_dag_task.add_parent(0, small_dag_task)


# Can do it with min but wanted something slighly different
def get_min_link_for_wf(linkables, wf):
    min_link = None
    for link in linkables:
        if link[0].wf_id == wf.id:
            if min_link is None or min_link[2] < link[2]:
                min_link = link
    if min_link is not None:
        linkables.remove(min_link)
    return min_link


def multiple_workflows_scheduling(workflows, machines):
    sorted_wfs: List[Workflow] = sorted(
        workflows, key=lambda wf_: wf_.calc_ccr(), reverse=True)

    j = len(sorted_wfs) - 1
    for i in range(int(len(sorted_wfs) / 2)):
        schedule_workflow(sorted_wfs[i], machines,
                          TimeType.EFT, try_fill_hole=True)
        schedule_workflow(sorted_wfs[j], machines,
                          TimeType.EST, try_fill_hole=True)
        j -= 1


def cpop(wf):
    critical_path, [entry_node, _] = wf.create_critical_path()
    critical_machine_id = pick_machine_for_critical_path(
        critical_path, wf.machines)
    schedule_tasks_cpop(
        wf.machines, [entry_node], (critical_path, critical_machine_id))
    return {'tasks': wf.tasks, 'machines': wf.machines}
