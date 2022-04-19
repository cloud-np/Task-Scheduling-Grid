from classes.workflow import Workflow
from classes.task import Task, TaskStatus
from typing import List, Iterable
import random
from helpers.examples.example_gen import ExampleGen
from helpers.utils import find_perc_diff
from classes.scheduler import Scheduler, TimeType, FillMethod
from classes.machine import Machine


class RuinRecreate:

    RR_COUNTODOWN = 100
    END_COUNTDOWN = 500

    def __init__(self, workflow: Workflow, machines: List[Machine], ruin_method="random"):
        self.og_workflow: Workflow = workflow
        self.og_machines: List[Machine] = machines
        self.rr_method: str = ruin_method
        self.rr_countdown: int = RuinRecreate.RR_COUNTODOWN
        self.end_countdown: int = RuinRecreate.END_COUNTDOWN

        self.ten_perc: int = int(len(workflow.tasks) * 10 / 100)
        self.ruin_lb: int = 0
        self.ruin_ub: int = self.ten_perc

        if self.rr_method == "random":
            self.__ruin = self.random_ruin
            self.__recreate = self.std_recreate
        if self.rr_method == "comm" or self.rr_method == "comp":
            self.sorted_tasks = sorted(workflow.tasks, key=lambda t: t.avg_cost()) if self.rr_method == "comp" else sorted(workflow.tasks, key=lambda t: t.avg_com_cost())
            self.__ruin = self.com_comp_ruin
            self.__recreate = self.std_recreate
        elif self.rr_method == "time":
            start = random.randint(0, int(workflow.wf_len))
            self.time_window: int = (start, start + int(workflow.wf_len * 10 / 100))
            self.__recreate = self.std_recreate
            self.__recreate = self.time_recreate
        elif self.rr_method == "order":
            self.__ruin = self.order_ruin
            self.__recreate = self.order_recreate
        elif self.rr_method == "level":
            self.ruin_level: int = 0
            _, self.max_level = Workflow.level_order(workflow.tasks)
            self.__ruin = self.level_ruin
            self.__recreate = self.std_recreate
        else:
            raise Exception("Unknown Ruin and Recreate method given!")
        # elif self.ruin_method == "uprank":
        #     self.sorted_tasks = sorted(workflow.tasks, key=lambda t: t.up_rank)

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
            workflows, machines = ExampleGen.re_create_example(
                [best_scheduled_workflow], self.og_machines, reset_task_status=True)
            unscheduled_workflow = workflows[0]

            # Ruin part
            ruined_tasks_ids = self.__ruin(best_scheduled_workflow)

            # Recreate part
            self.__recreate(unscheduled_workflow, machines, ruined_tasks_ids)
            best_scheduled_workflow, end_loop = self.greedy_keep(
                unscheduled_workflow, best_scheduled_workflow)

        return best_scheduled_workflow, machines

    def greedy_keep(self, wf, best_wf):
        self.rr_countdown -= 1
        self.end_countdown -= 1

        if self.rr_countdown <= 0 and best_wf.wf_len < self.og_workflow.wf_len:
            return best_wf, True
        elif self.end_countdown <= 0:
            return best_wf, True
        if wf.wf_len < best_wf.wf_len:
            self.rr_countdown = RuinRecreate.RR_COUNTODOWN
            self.end_countdown = RuinRecreate.END_COUNTDOWN
            return wf, False
        if self.rr_method == "comp" or self.rr_method == "comm":
            if self.ruin_ub >= len(wf.tasks):
                return best_wf, True
        if self.rr_method == "level":
            if self.ruin_level >= self.max_level:
                return best_wf, True
        return best_wf, False

    def com_comp_ruin(self, workflow: Workflow):
        ruin_ids = [(t.id, t.machine_id) for t in self.sorted_tasks[self.ruin_lb:self.ruin_ub]]
        self.ruin_lb = self.ruin_ub
        self.ruin_ub += self.ten_perc
        return ruin_ids

    def com_comp_recreate(self, workflow: Workflow, machines: List[Machine], ruined_mt_ids):
        ...

    def random_ruin(self, workflow: Workflow):
        return [(t.id, t.machine_id) for t in workflow.tasks if random.randint(0, 10) < 2]

    def random_recreate(self, workflow: Workflow, machines: List[Machine], ruined_mt_ids):
        ...

    def time_ruin(self, workflow: Workflow):
        ruin_ids = [(t.id, t.machine_id) for t in filter(lambda x: self.time_window[0] <= x.start <= self.time_window[1], workflow.tasks)]
        start = random.randint(0, int(workflow.wf_len))
        self.time_window: int = (start, start + int(workflow.wf_len * 10 / 100))
        return ruin_ids

    def time_recreate(self, workflow: Workflow, machines: List[Machine], ruined_mt_ids):
        ...

    def level_ruin(self, workflow: Workflow):
        ...

    def level_recreate(self, workflow: Workflow, machines: List[Machine], ruined_mt_ids):
        ...

    def order_ruin(self, workflow: Workflow):
        return random.shuffle([t for t in workflow.tasks])

    def order_recreate(self, workflow: Workflow, machines: List[Machine], ruined_mt_ids):
        def update_childen(task):
            if len(task.children_edges):
                return

            for e in task.children_edges:
                child = e.node
                update_childen(child)
                child.start = task.end + e.weight if task.machine.id != child.machine.id else 0

        def find_atm_slowest_parent(task):
            if task.is_entry:
                return None
            # Remove the parents that have not been scheduled
            return max(task.parents_edges, key=lambda e: e.node.end if e.node.end is not None else -1)

        def compute_exec_time(task, m_id, potensial_start_time):
            parent_edge = find_atm_slowest_parent(task)

            # if no parent was scheduled we can start at the potensial start time and adjuct accordingly later on.
            if parent_edge is None or parent_edge.node.end is None:
                return [potensial_start_time, potensial_start_time + task.costs[m_id]]
            elif parent_edge.node.machine_id == m_id:
                communication_time = 0
            else:
                communication_time = parent_edge.weight

            start = max(parent_edge.node.end + communication_time, potensial_start_time)
            end = start + task.costs[m_id]
            return start, end

        for task in workflow.tasks:
            all_times = [{"times": compute_exec_time(task, m.id, m.time_on_machine), "m": m} for m in machines]
            s = min(all_times, key=lambda x: x['times'][0])
            Scheduler.schedule_task(s['times'], task, s['m'], hole=None, unsafe_scheduling=False)
            update_childen(task)
        workflow.set_scheduled(True)

    def __ruin(self, workflow: Workflow):
        if self.rr_method == "level":
            return [(t.id, t.machine_id) for t in workflow.tasks if t.level == self.ruin_level]
        # if self.ruin_method == "order":
        #     return
        # elif self.ruin_method == "time-based":
        #     # NOTE this is not working yet
        #     # return [(t.id, t.machine_id) for t in workflow.tasks if self.time_space[0] < t.start < self.time_space[1]]
        #     pass

    def std_recreate(self, workflow: Workflow, machines: List[Machine], ruined_mt_ids):
        # # for task in sorted(workflow.tasks, key=lambda t: t.up_rank, reverse=True):
        # for task in workflow.tasks:
        #     # print(task.id, task.status)
        #     if m_id := [mt_ids[1] for mt_ids in ruined_mt_ids if mt_ids[0] == task.id]:
        #         Scheduler.schedule_task_machine(task, [m for m in machines if m.id != m_id[0]], TimeType.EFT)
        #     if task.status != TaskStatus.UNSCHEDULED:
        #         Scheduler.schedule_task_machine(task, machines, TimeType.EFT)

        for task in workflow.tasks:
            if m_id := [r_info[1] for r_info in ruined_mt_ids if r_info[0] == task.id]:
                Scheduler.schedule_task_machine(
                    task, [m for m in machines if m.id != m_id[0]], TimeType.EFT)
            if task.status != TaskStatus.SCHEDULED:
                Scheduler.schedule_task_machine(task, machines, TimeType.EFT)
        workflow.set_scheduled(True)
