from colorama import Fore

SUCCESS = f'{Fore.GREEN}The schedule is valid!{Fore.RESET}'


def schedule_checker(schedule):
    tasks = [wf.tasks for wf in schedule.workflows]
    tasks = sum(tasks, [])

    # Check for task overlaps
    has_overlap, tasks = check_task_overlaps(schedule.machines)
    if has_overlap:
        raise Exception(
            f"{schedule.method_used_info()} t1: {tasks[0]} t2: {tasks[1]} ")

    # Check for correct order in tasks
    wrong_order, tasks = check_order_in_tasks(tasks)
    if wrong_order:
        raise Exception(f'{schedule.method_used_info()}'
                        f'{Fore.LIGHTRED_EX}Child Starts before parent finishes!!{Fore.RESET}\n'
                        f'{Fore.LIGHTRED_EX}PARENT:{Fore.RESET} {tasks[0]}  ----> {Fore.LIGHTRED_EX}CHILD:{Fore.RESET} '
                        f'{tasks[1]}\n Child-start: {tasks[1].start}  Parent-end: {tasks[0].end}\n')


def workflow_checker(workflow):
    has_overlap, tasks = check_task_overlaps(workflow.machines)
    if has_overlap:
        raise Exception(f"From Workflow[{workflow.id}] t1: {tasks[0]} t2: {tasks[1]} are overlapping!")

    wrong_order, tasks = check_order_in_tasks(workflow.tasks)
    if wrong_order:
        raise Exception(f'{Fore.LIGHTRED_EX}Child Starts before parent finishes!!{Fore.RESET}\n'
                        f'{Fore.LIGHTRED_EX}PARENT:{Fore.RESET} {tasks[0]}  ----> {Fore.LIGHTRED_EX}CHILD:{Fore.RESET} '
                        f'{tasks[1]}\n Child-start: {tasks[1].start}  Parent-end: {tasks[0].end}\n')


def check_task_overlaps(machines):
    for m in machines:
        for i in range(len(m.tasks)):
            t1 = m.tasks[i]
            for j in range(i + 1, len(m.tasks)):
                t2 = m.tasks[j]
                max_start = t1.start if t1.start > t2.start else t2.start
                min_end = t1.end if t1.end < t2.end else t2.end
                if max_start < min_end:
                    return True, [t1, t2]
    return False, None


def check_order_in_tasks(tasks):
    for task in tasks:
        for edge in task.children_edges:
            if edge.node.start < task.end:
                return True, [task, edge.node]
    return False, None


def error(task, total_len, prev_task):
    raise Exception(f'task.end < total_len\n{task} start: {task.start_str()} end: {task.end_str()} \n'
                    f'{prev_task} start: {prev_task.start_str()} end: {prev_task.end_str()}\ncurr_len: {total_len}\n')
