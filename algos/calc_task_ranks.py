def avg(arr):
    return sum(arr) / len(arr)


def calculate_upward_ranks(tasks):
    def recursive_upward_ranks(curr_task):
        # Base condition once your set
        # is empty just return the computation cost
        if curr_task.is_exit:
            # TODO: we use runtime or calc the avg here?
            avg_cost = avg(curr_task.costs)
            curr_task.up_rank = avg_cost
            return avg_cost

        all_ranks_of_curr_task = list()
        for child_edge in curr_task.children_edges:
            # Calc rank_u
            rank = child_edge.weight + recursive_upward_ranks(child_edge.node)
            all_ranks_of_curr_task.append(rank)
        task_costs = avg(curr_task.costs)
        max_rank = task_costs + max(all_ranks_of_curr_task)

        # Set to the task their rank
        curr_task.up_rank = max_rank
        return max_rank

    recursive_upward_ranks(tasks[0])
    return tasks


def calculate_downward_ranks(tasks):
    def recursive_downward_ranks(curr_task):
        # Base condition once your set
        # is empty just return the computation cost
        if curr_task.is_entry:
            # TODO: we use runtime or calc the avg here?
            avg_cost = avg(curr_task.costs)
            curr_task.down_rank = avg_cost
            return avg_cost

        all_ranks_of_curr_task = list()
        for parent_edge in curr_task.parents_edges:
            # Showing path/steps for debugging
            # if curr_task.wf_id == 0:
            #     print(f'{Back.CYAN if parent_edge.node.is_entry_task else Back.RESET}'
            #           f'{Fore.RED}{parent_edge.node.id}{Fore.RESET}{Back.RESET} ->', end=" ")
            # Calc rank_u
            rank = parent_edge.weight + recursive_downward_ranks(parent_edge.node) + avg(parent_edge.node.costs)
            all_ranks_of_curr_task.append(rank)
        max_rank = max(all_ranks_of_curr_task)

        # Set to the task their rank
        curr_task.down_rank = max_rank
        return max_rank

    recursive_downward_ranks(tasks[-1])
    return tasks
