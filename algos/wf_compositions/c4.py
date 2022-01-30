from algos.heuristic import heft

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
    # for link in linkables:
    #     # DEBUG
    #     print(f"[{'A' if link[0].wf_id == 0 else 'B'}]-{link[0].str_col_id()} ---> "
    #           f"[{'A' if link[1].wf_id == 0 else 'B'}]-{link[1].str_col_id()} "
    #           f"diff = {Fore.GREEN}{link[2]}{Fore.RESET}")

    all_tasks = []
    for wf in workflows:
        # Get the minimum link
        min_link = get_min_link_for_wf(linkables, wf)
        if min_link is not None:
            create_link(min_link, wf)
        all_tasks.extend(wf.tasks)
    # return heft(all_tasks, machines)


def create_link(min_link, small_wf):
    small_dag_task = small_wf.cp_info['entry']
    big_dag_task = min_link[1]

    small_dag_task.add_child(0, big_dag_task)
    big_dag_task.add_parent(0, small_dag_task)


# Can do it with min but wanted something slighly different
def get_min_link_for_wf(linkables, wf):
    min_link = None
    for link in linkables:
        if link[0].wf_id == wf.id and (
            min_link is None or min_link[2] < link[2]
        ):
            min_link = link
    if min_link is not None:
        linkables.remove(min_link)
    return min_link
