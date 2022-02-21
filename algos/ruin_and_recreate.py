from classes.workflow import Workflow
from classes.task import Task, TaskStatus
from typing import List, Iterable
import random
from helpers.examples.example_gen import ExampleGen
from classes.scheduler import Scheduler, TimeType
from classes.machine import Machine
from algos.optimizer import try_update_best_schedule


class RuinRecreate:

    def __init__(self, workflow: Workflow, machines: List[Machine], ruin_method="random"):
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
        scheduled_workflow = workflow = self.og_workflow
        # Since we give just one workflow to copy there is only one in the list
        is_better = False
        i = 0
        while not is_better:
            # Refresh the data
            workflows, machines = ExampleGen.re_create_example([workflow], self.og_machines, reset_task_status=True)
            workflow = workflows[0]

            # Ruin part
            ruined_tasks_ids = self.__ruin(scheduled_workflow)

            # Recreate part
            self.__recreate(workflow, machines, ruined_tasks_ids)

            if workflow.wf_len < scheduled_workflow.wf_len:
                # if i >= 4:
                is_better = True
                scheduled_workflow = workflow
                i += 1
            # print(workflow.wf_len)

        return workflow, machines

    def __ruin(self, workflow: Workflow):
        if self.ruin_method == "random":
            return [(t.id, t.machine_id) for t in workflow.tasks if random.randint(0, 10) < 5]
        # elif self.ruin_method == "time-based":
        #     # NOTE this is not working yet
        #     # return [(t.id, t.machine_id) for t in workflow.tasks if self.time_space[0] < t.start < self.time_space[1]]
        #     pass
        else:
            raise Exception("Unknown ruin method")

    def __recreate(self, workflow: Workflow, machines: List[Machine], ruined_tasks_ids):
        for task in workflow.tasks:
            if m_id := [r_info[1] for r_info in ruined_tasks_ids if r_info[0] == task.id]:
                Scheduler.schedule_task_machine(task, [m for m in machines if m.id != m_id[0]], TimeType.EFT)
            if task.status != TaskStatus.SCHEDULED:
                Scheduler.schedule_task_machine(task, machines, TimeType.EFT)
        workflow.set_scheduled(True)
