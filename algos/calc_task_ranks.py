def avg(arr):
    return sum(arr) / len(arr)


def calculate_upward_ranks(tasks):
    def calc_upward(curr_task):
        # Base condition once your set
        # is empty just return the computation cost
        if curr_task.is_exit:
            curr_task.up_rank = avg(curr_task.costs)
            return curr_task.up_rank

        curr_task.up_rank = avg(curr_task.costs) + max(e.weight + calc_upward(e.node) for e in curr_task.children_edges)
        return curr_task.up_rank

    calc_upward(tasks[0])
    return tasks


def calculate_downward_ranks(tasks):
    def recursive_downward_ranks(curr_task):
        # Base condition once your set
        # is empty just return the computation cost
        if curr_task.is_entry:
            avg_cost = avg(curr_task.costs)
            curr_task.down_rank = avg_cost
            return avg_cost

        all_ranks_of_curr_task = []
        for parent_edge in curr_task.parents_edges:
            # Showing path/steps for debugging
            # if curr_task.wf_id == 0:
            # print(f'{Back.CYAN if parent_edge.node.is_entry else Back.RESET} {Fore.RED}{parent_edge.node.id}{Fore.RESET}{Back.RESET} ->', end=" ")
            # Calc rank_u
            rank = parent_edge.weight + recursive_downward_ranks(parent_edge.node) + avg(parent_edge.node.costs)
            all_ranks_of_curr_task.append(rank)
        max_rank = max(all_ranks_of_curr_task)

        # Set to the task their rank
        curr_task.down_rank = max_rank
        return max_rank

    recursive_downward_ranks(tasks[-1])
    return tasks
