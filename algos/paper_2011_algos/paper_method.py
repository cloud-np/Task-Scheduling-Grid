from typing import Any
import random
from classes.scheduler import TimeType, PriorityType

# Just a placeholder name unti I find a better one.


class Paper2011:

    def __init__(self, workflows, machines, machine_select_method=TimeType.EFT, task_select_method=PriorityType.EDF) -> None:
        # We keep a typical arrived time of each workflow to check later on if
        # they have to get removed because they didn't meet the deadend.
        self.workflow_dicts: Any = sorted([{"wf": wf, "arrived_time": random.randint(0, 100)} for wf in workflows], key=lambda wfd: wfd["arrived_time"])
        self.timer = 0
        self.machine_select_method = machine_select_method
        self.task_select_method = task_select_method
        # We give each machine a local que
        self.machines_dicts = [{"m": m, "local_q": []} for m in machines]
        self.global_q = []
        self.run_scheduler()

    def run_scheduler(self):
        self.global_q.append(wfd["wf"].get_ready_tasks() for wfd in self.workflow_dicts)
        # Flatten the lists inside our list.
        self.global_q = sum(self.global_q, [])

        while len(self.global_q) > 0:
            # 1. Task selection based on the given priority

            # 2. Machine selection based on the method given e.g: EFT
            #   - In the machine selection phase we try to first fill the holes
            #     if possible. If we cannot fill any hole then we go ahead and lock
            #     the position equal to the potensial pos of the task.
            break
