def avg(arr):
    return sum(arr) / len(arr)


def calculate_upward_ranks(tasks):
    def calc_upward(curr_task):
        # Base condition once your set
        # is empty just return the computation cost
        if curr_task.is_exit:
            curr_task.up_rank = avg(curr_task.costs)
            return curr_task.up_rank

        curr_task.up_rank = avg(curr_task.costs) + max(che.weight + calc_upward(che.node) for che in curr_task.children_edges)
        return curr_task.up_rank

    calc_upward(tasks[0])
    return tasks


def calculate_downward_ranks(tasks):
    def calc_downward(curr_task):
        # Base condition once your set
        # is empty just return the computation cost
        if curr_task.is_entry:
            curr_task.down_rank = avg(curr_task.costs)
            return curr_task.down_rank

        curr_task.down_rank = max(avg(pe.node.costs) + pe.weight + calc_downward(pe.node) for pe in curr_task.parents_edges)
        return curr_task.down_rank

    calc_downward(tasks[-1])
    return tasks
