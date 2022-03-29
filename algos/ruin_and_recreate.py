from classes.workflow import Workflow
from classes.task import Task, TaskStatus
from typing import List, Iterable
import random
from helpers.examples.example_gen import ExampleGen
from helpers.utils import find_perc_diff
from classes.scheduler import Scheduler, TimeType
from classes.machine import Machine


class RuinRecreate:

    RR_COUNTODOWN = 3000

    def __init__(self, workflow: Workflow, machines: List[Machine], ruin_method="random"):
        self.og_workflow: Workflow = workflow
        self.og_machines: List[Machine] = machines
        self.ruin_method: str = ruin_method
        self.rr_countdown: int = RuinRecreate.RR_COUNTODOWN

        self.comp_srt: List[Workflow] = sorted(self.og_workflow.tasks, key=lambda t: t.avg_cost())
        self.comm_srt: List[Workflow] = sorted(self.og_workflow.tasks, key=lambda t: sum(e.weight for e in t.children_edges))

        # NOTE: To get the time_space dynamically we need to have the workflow length.
        self.time_space = (20, 300)
        self.ten_perc = int(len(workflow.tasks) * 10 / 100)
        self.ruin_lb = 0
        self.ruin_ub = self.ten_perc

        if self.ruin_method == "comp":
            self.sorted_tasks = sorted(workflow.tasks, key=lambda t: t.avg_cost())
        elif self.ruin_method == "comm":
            self.sorted_tasks = sorted(workflow.tasks, key=lambda t: t.avg_comm_cost())

        # Find the part you want to ruin

        # Ruin the part
        # self.__ruin()

    def run(self):
        # Get the order of the tasks.
        # scheduled_tasks: Iterable[Task] = sorted(self.og_workflow.tasks, key=lambda t: t.start)
        best_scheduled_workflow = self.og_workflow
        # Since we give just one workflow to copy there is only one in the list
        end_loop = False

        while not end_loop:
            # Refresh the data
            workflows, machines = ExampleGen.re_create_example([best_scheduled_workflow], self.og_machines, reset_task_status=True)
            unscheduled_workflow = workflows[0]

            # Ruin part
            ruined_tasks_ids = self.__ruin(best_scheduled_workflow)

            # Recreate part
            self.__recreate(unscheduled_workflow, machines, ruined_tasks_ids)
            best_scheduled_workflow, end_loop = self.greedy_keep(unscheduled_workflow, best_scheduled_workflow)

        return best_scheduled_workflow, machines

    def greedy_keep(self, workflow, best_scheduled_workflow):
        self.rr_countdown -= 1

        if self.rr_countdown <= 0 and best_scheduled_workflow.wf_len < self.og_workflow.wf_len:
            return best_scheduled_workflow, True
        if workflow.wf_len < best_scheduled_workflow.wf_len:
            self.rr_countdown = RuinRecreate.RR_COUNTODOWN
            return workflow, False
        if self.ruin_method == "comp" or self.ruin_method == "comm":
            if self.ruin_ub >= len(workflow.tasks):
                return best_scheduled_workflow, True
        return best_scheduled_workflow, False

    def __ruin(self, workflow: Workflow):
        if self.ruin_method == "random":
            return [(t.id, t.machine_id) for t in workflow.tasks if random.randint(0, 10) < 5]
        if self.ruin_method == "comp" or self.ruin_method == "comm":
            print(self.ruin_lb, self.ruin_ub)
            data = [(t.id, t.machine_id) for t in self.sorted_tasks[self.ruin_lb:self.ruin_ub]]
            self.ruin_lb = self.ruin_ub
            self.ruin_ub += self.ten_perc
            return data
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
