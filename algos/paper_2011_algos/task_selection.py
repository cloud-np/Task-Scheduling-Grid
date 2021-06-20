

# We the pick the task that has the smallest workflow deadline
def edf_picker(ready_tasks):
    return min(ready_tasks, key=lambda task: task.wf_deadline)

# We the pick the task with the biggest up_rank


def hlf_picker(ready_tasks):
    return max(ready_tasks, key=lambda task: task.up_rank)

# NOTE: Question about the STk and what "t" var is in the paper.


def lstf_picker(ready_tasks):
    ...
