from classes.workflow import Workflow
from classes.task import Task, TaskStatus
from typing import List, Iterable
import random
from helpers.examples.example_gen import ExampleGen
from classes.scheduler import Scheduler, TimeType
from classes.machine import Machine
from algos.optimizer import try_update_best_schedule


# class Solution:
#     def __init__(self, workflow: Workflow):


class RuinRecreate:

    def __init__(self, workflow: Workflow, machines: List[Machine], ruin_method="random"):
        # self.solution = Solution(workflow)
        # self.og_scheduled_tasks: List[int] = [(t.id, t.machine_id) for t in sorted(workflow.tasks, key=lambda t: t.start)]
        self.og_workflow: Workflow = workflow
        self.og_machines: List[Machine] = machines
        self.ruin_method: str = ruin_method

        # NOTE: To get the time_space dynamically we need to have the workflow length.
        self.time_space = (20, 300)

        # Find the part you want to ruin

        # Ruin the part
        # self.__ruin()

    def run(self):
        # Get the order of the tasks.
        # scheduled_tasks: Iterable[Task] = sorted(self.og_workflow.tasks, key=lambda t: t.start)

        # Since we give just one workflow to copy there is only one in the list
        is_better = False
        while not is_better:
            workflows, machines = ExampleGen.re_create_example([self.og_workflow], self.og_machines, reset_task_status=True)
            workflow = workflows[0]

            # Ruin part
            if self.ruin_method == "random":
                ruined_tasks_ids = [(t.id, t.machine_id) for t in self.og_workflow.tasks if random.randint(0, 10) < 5]
            elif self.ruin_method == "time-based":
                ruined_tasks_ids = [(t.id, t.machine_id) for t in self.og_workflow.tasks if self.time_space[0] < t.start < self.time_space[1]]
            else:
                raise Exception("Unknown ruin method")

            # Recreate part
            for task in workflow.tasks:
                if m_id := [r_info[1] for r_info in ruined_tasks_ids if r_info[0] == task.id]:
                    Scheduler.schedule_task_machine(task, [m for m in machines if m.id != m_id[0]], TimeType.EFT)
                if task.status != TaskStatus.SCHEDULED:
                    Scheduler.schedule_task_machine(task, machines, TimeType.EFT)

            workflow.set_scheduled(True)
            if workflow.wf_len < self.og_workflow.wf_len:
                is_better = True

        return workflow, machines

    def __ruin(self, workflow: Workflow):
        pass

    def __recreate(self, workflow: Workflow):
        pass
