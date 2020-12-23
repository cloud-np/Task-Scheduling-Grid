import copy
import math
from colorama import Fore, Back, Style


def avg(arr):
    return sum(arr) / len(arr)


def calculate_upward_ranks(tasks):
    def recursive_upward_ranks(curr_task):
        # Base condition once your set
        # is empty just return the computation cost
        # if curr_task.name.startswith('Dummy') and curr_task.is_exit_node:
        if curr_task.is_exit_task:
            # TODO: we use runtime or calc the avg here?
            avg_cost = avg(curr_task.costs)
            curr_task.up_rank = avg_cost
            return avg_cost

        all_ranks_of_curr_node = list()
        for child in curr_task.children_edges:
            # Showing path/steps for debugging
            # print(f'{Back.CYAN if tasks[i].is_exit_node else Back.RESET}'
            #       f'{Fore.RED}{i + 1}{Fore.RESET}{Back.RESET} ')
            # Calc rank_u
            rank = child.weight + recursive_upward_ranks(child.node)
            all_ranks_of_curr_node.append(rank)
        max_rank = avg(curr_task.costs) + max(all_ranks_of_curr_node)

        # Set to the task their rank
        curr_task.up_rank = max_rank
        return max_rank

    recursive_upward_ranks(tasks[0])


def calculate_downward_ranks(tasks):
    def recursive_downward_ranks(curr_task):
        # Base condition once your set
        # is empty just return the computation cost
        # if curr_task.name.startswith('Dummy') and curr_task.is_exit_node:
        if curr_task.is_entry_task:
            # TODO: we use runtime or calc the avg here?
            avg_cost = avg(curr_task.costs)
            curr_task.down_rank = avg_cost
            return avg_cost

        all_ranks_of_curr_node = list()
        for parent_edge in curr_task.parents_edges:
            # Showing path/steps for debugging
            # print(f'{Back.CYAN if tasks[i].is_exit_node else Back.RESET}'
            #       f'{Fore.RED}{i + 1}{Fore.RESET}{Back.RESET} ')
            # Calc rank_u
            rank = parent_edge.weight + recursive_downward_ranks(parent_edge.node) + avg(parent_edge.node.costs)
            all_ranks_of_curr_node.append(rank)
        max_rank = max(all_ranks_of_curr_node)

        # Set to the task their rank
        curr_task.down_rank = max_rank
        return max_rank

    recursive_downward_ranks(tasks[len(tasks) - 1])

