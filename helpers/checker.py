from colorama import Fore

SUCCESS = f'{Fore.GREEN}The schedule is valid!{Fore.RESET}'


def schedule_checker(schedule):
    tasks = [wf.tasks for wf in schedule.workflows]
    tasks = sum(tasks, [])

    # Check for task overlaps
    for m in schedule.machines:
        for i in range(len(m.tasks)):
            t1 = m.tasks[i]
            for j in range(i + 1, len(m.tasks)):
                t2 = m.tasks[j]
                max_start = t1.start if t1.start > t2.start else t2.start
                min_end = t1.end if t1.end < t2.end else t2.end
                if max_start < min_end:
                    raise Exception(f"{schedule.method_used_info()} t1: {t1} t2: {t2} ")

    # Check for correct order in tasks
    for task in tasks:
        for edge in task.children_edges:
            if edge.node.start < task.end:
                return child_starts_before_parent_error(schedule, parent=task, child=edge.node)


def error(task, total_len, prev_task):
    raise Exception(f'task.end < total_len\n{task} start: {task.start_str()} end: {task.end_str()} \n'
                    f'{prev_task} start: {prev_task.start_str()} end: {prev_task.end_str()}\ncurr_len: {total_len}\n')


def child_starts_before_parent_error(schedule, parent, child):
    raise Exception(f'{schedule.method_used_info()}'
                    f'{Fore.LIGHTRED_EX}Child Starts before parent finishes!!{Fore.RESET}\n'
                    f'{Fore.LIGHTRED_EX}PARENT:{Fore.RESET} {parent}  ----> {Fore.LIGHTRED_EX}CHILD:{Fore.RESET} '
                    f'{child}\n Child-start: {child.start}  Parent-end: {parent.end}\n')
