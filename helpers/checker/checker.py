from colorama import Fore

SUCCESS = f'{Fore.GREEN}The schedule is valid!{Fore.RESET}'


def schedule_checker(tasks, machines):
    # Check if there is one and only task running at a certain time
    # NOTE: The tasks should be in the order the got
    # added otherwise this would return an error!
    for machine in machines:
        prev_task = machine.tasks[0]
        total_len = 0
        for task in machine.tasks:
            if task.end < total_len:
                return error(task, total_len, prev_task)
            else:
                prev_task = task
                total_len = task.end

    for task in tasks:
        for edge in task.children_edges:
            if edge.node.start < task.end:
                return child_starts_before_parent_error(parent=task, child=edge.node)
    return print(SUCCESS)


def error(task, total_len, prev_task):
    raise Exception(f'task.end < total_len\n{task} start: {task.start_str()} end: {task.end_str()} \n'
                    f'{prev_task} start: {prev_task.start_str()} end: {prev_task.end_str()}\ncurr_len: {total_len}\n')


def child_starts_before_parent_error(parent, child):
    raise Exception(f'{Fore.LIGHTRED_EX}Child Starts before parent finishes!!{Fore.RESET}\n'
                    f'{Fore.LIGHTRED_EX}PARENT:{Fore.RESET} {parent}  ----> {Fore.LIGHTRED_EX}CHILD:{Fore.RESET} '
                    f'{child}\n Child-start: {child.start}  Parent-end: {parent.end}\n')
