from typing import Any
import random

# Just a placeholder name unti I find a better one.


class Paper2011:

    def __init__(self, workflows, machines) -> None:
        self.workflow_dicts: Any = sorted(
            [{"wf": wf, "arrived_time": random.randint(
                0, 100)} for wf in workflows],
            key=lambda wfd: wfd["arrived_time"]
        )
        self.timer = 0
        self.machines_dicts = [{"m": m, "local_q": list()} for m in machines]
        self.global_q = list()
        self.run_scheduler()

    def run_scheduler(self):
        self.global_q.append(*self.workflow_dicts[0]["wf"].get_ready_tasks())

        while len(self.global_q) > 0:
            break
