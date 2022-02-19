from enum import Enum
from typing import List, Any, Optional
import os
from colorama import Fore, Back
from classes.workflow import Workflow
from dataclasses import dataclass
from classes.task import TaskStatus, TaskBlueprint
from helpers.checker import schedule_checker
from algos.calc_task_ranks import calculate_upward_ranks


class TimeType(Enum):
    EST = 0
    EFT = 1
    LST = 2
    LFT = 3


class PriorityType(Enum):
    HLF = 0
    EDF = 1
    LSTF = 2


class FillMethod(Enum):
    NO_FILL = -1
    FASTEST_FIT = 0
    BEST_FIT = 1
    FIRST_FIT = 2
    WORST_FIT = 3


@dataclass
class ScheduleBlueprint:
    name: str
    workflows: List[List[TaskBlueprint]]
    machines: List[Any]
    priority_type: PriorityType
    fill_method: FillMethod
    time_types: List[TimeType]


class Scheduler:
    def __init__(self, name: str, data, time_types: List[str], fill_method: str, schedule_order: Optional[List[int]] = None, priority_type=None, output_path: str = "./simulation_output"):
        workflows, machines = data
        self.name: str = name
        self.workflows: List[Workflow] = workflows
        self.machines = machines
        self.avg_workflow_makespan: Optional[float] = None
        self.output_path: str = output_path
        self.critical_tasks = []
        self.schedule_wfs_order: List[int] = schedule_order
        # if not time_types[0].__class__ == str and time_types[1].__class__ == str and fill_method.__class__ == str and
        # E.g: sim_out/5.txt
        self.output_file: str = f"{self.output_path}/bw_{int(self.machines[0].network_kbps / 125)}_wfs_{len(workflows)}_machines_{len(self.machines)}.txt"
        self.time_types_str = time_types

        if time_types is not None:
            # Get time types e.g: EFT = earliest finish time
            self.time_types: List[TimeType] = [get_time_type(ttype) for ttype in time_types]

        self.priority_type_str = priority_type
        self.priority_type: PriorityType = get_priority_type(priority_type)

        # Get fill type e.g: FASTEST-FIT = pick the hole that has gives the best time.
        self.fill_method_str = fill_method
        self.fill_method: FillMethod = get_fill_method(fill_method)
        # The method that we gonna run the schedule.
        self.schedule_method: Any = self.get_scheduling_method(name)

        self.is_scheduling_done: bool = False

    # This function schedules the task and returns the new
    @staticmethod
    def schedule_task(times, task, machine, hole=None):
        task.machine_id = machine.id
        task.start = times[0]
        task.end = times[1]
        task.update_children_and_self_status()

        if hole is None:
            machine.add_task(task)
        else:
            machine.add_task_to_hole(task, hole)

    def get_slowest_machine(self):
        if self.is_scheduling_done is True:
            return max(self.machines, key=lambda m: m.time_on_machine)
        else:
            raise Exception("You should run the scheduling method first.")

    def __str__(self):
        _str = f"\t{Back.MAGENTA}{Fore.LIGHTYELLOW_EX}{self.method_used_info()}{Fore.RESET}{Back.RESET}"
        # if self.name.startswith("holes"):
        #     print(f"Time saved = {Fore.GREEN}{sum([m.holes_saved_time for m in self.machines])}{Fore.RESET}")

        slowest_machine = self.get_slowest_machine()
        _str += f'\n{slowest_machine.str_col_schedule_len()}\n'
        _str += f'\n{Fore.RED}AVG MAKESPAN:{Fore.RESET} {self.avg_workflow_makespan}\n'
        _str += f"n-tasks: {Fore.MAGENTA}{sum(len(wf.tasks) for wf in self.workflows)}{Fore.RESET} machines: {Fore.MAGENTA}{len(self.machines)}{Fore.RESET} network: {Fore.MAGENTA}{self.machines[0].network_kbps / 125}{Fore.RESET}\n"
        return _str

    def get_blueprint(self):
        return ScheduleBlueprint(self.name, [[t.get_blueprint() for t in wf.tasks] for wf in self.workflows], self.machines, self.priority_type, self.fill_method, self.time_types)

    def save_blueprint(self):
        blp_self = self.get_blueprint()

        lines = [f"({m.id}, {m.name}, {m.n_cpu}, {m.speed}, {m.network_kbps})\n" for m in self.machines]
        lines.insert(0, f"{self.priority_type}, {self.fill_method}, {self.time_types}\n")
        for blp_tasks in blp_self.workflows:
<<<<<<< HEAD
            for bt in blp_tasks:
                lines.append(
                    f'TaskBlueprint({bt.id_}, {bt.wf_id}, "{bt.name}", {bt.runtime}, {bt.children_names}, {bt.parents_names}, {1 if bt.is_entry else 0}, {bt.is_entry}, {bt.is_exit}),\n'
                )
=======
            lines.extend(
                f'TaskBlueprint({bt.id_}, {bt.wf_id}, "{bt.name}", {bt.runtime}, {bt.children_names}, {bt.parents_names}, {1 if bt.is_entry else 0}, {bt.is_entry}, {bt.is_exit}),\n'
                for bt in blp_tasks
            )
>>>>>>> testing

        with open(f"./{get_fill_method(self.fill_method)}.txt", "w") as f:
            f.writelines(lines)

    def get_whole_idle_time(self):
        return sum(m.get_idle_time() for m in self.machines)

    def run_example(self):
        self.example_hole_scheduling()
        self.is_scheduling_done = True
        self.schedule_len = self.get_schedule_len()
        schedule_checker(self)

    def run(self):
        self.schedule_method()
        self.is_scheduling_done = True
        self.schedule_len = self.get_schedule_len()
        self.machines_util_avg_perc = sum(m.get_util_perc(self.schedule_len) for m in self.machines) / len(self.machines)
        self.avg_workflow_makespan = sum(wf.wf_len for wf in self.workflows) / len(self.workflows)
        # schedule_checker(self)

    def method_used_info(self, concise=False):
        fill_method = None
        if not self.name.startswith("holes"):
            return self.name
        if concise:
            if self.fill_method == FillMethod.FASTEST_FIT:
                fill_method = "FST"
            elif self.fill_method == FillMethod.BEST_FIT:
                fill_method = "B"
            elif self.fill_method == FillMethod.FIRST_FIT:
                fill_method = "FR"
            elif self.fill_method == FillMethod.WORST_FIT:
                fill_method = "W"
        else:
            fill_method = get_fill_method(self.fill_method)

        if self.name.startswith("holes2011"):
            return f"{fill_method} {self.priority_type_str}\n"
        ttypes = [get_time_type(t) for t in self.time_types]
        return f"{'ordered ' if self.name.startswith('ordered') else ''}{fill_method}-{ttypes[0]}-{ttypes[1]}\n"

    def get_scheduled_info(self):
        def add_nl(_str):
            return f"{_str}\n"
        method_info = self.method_used_info()
        time_saved = None
        if self.name.startswith("holes"):
            time_saved = sum([m.holes_saved_time for m in self.machines])

        slowest_machine = self.get_slowest_machine()
        m_id = slowest_machine.str_id()
        schedule_len = slowest_machine.str_schedule_len()

        return [method_info, f"Holes Filled {self.get_holes_filled()}", add_nl(time_saved), add_nl(m_id), add_nl(schedule_len)]

    def get_holes_time_saved(self):
        return sum(m.holes_saved_time for m in self.machines)

    def get_holes_filled(self):
        return sum(m.holes_filled for m in self.machines)

    def get_schedule_len(self):
        slowest_machine = self.get_slowest_machine()
        return slowest_machine.time_on_machine

    def get_info_for_files(self) -> List[str]:
        name_info = "".join([f"-{time_type}" for time_type in self.time_types_str] if self.time_types_str is not None else "")
        return [f"{self.name}-{name_info}\t", f"{self.schedule_len}\t", f"{self.machines_util_avg_perc}\t", f"{self.avg_workflow_makespan}\n"]

    # NOTE:
    # avg_util of machines
    # avg_makespan of wfs
    def save_output_to_file(self):
        lines = self.get_info_for_files()

        # Create the path if it does not exist.
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        # If the file does not exist then add the titles.
        if not os.path.exists(self.output_file):
            lines.insert(0, "Method Name\tTotal Makespan\tAvg Machine util\tAvg workflow makespan\n")

        # Append to the correct file if it exists otherwise create it.
        with open(self.output_file, "a+") as f:
            f.writelines(lines)

    def get_scheduling_method(self, name):
        if name.startswith("holes2011"):
            return self.holes2011
        elif name.startswith("crit") or name.startswith("ordered crit"):
            return self.holes_scheduling_critical_tasks
        elif name.startswith("holes") or name.startswith("ordered holes"):
            return self.holes_scheduling
        elif name == "c1":
            return self.multiple_workflows_c1
        elif name == "c2":
            return self.multiple_workflows_c2
        elif name == "c3":
            return self.multiple_workflows_c3
        elif name == "c4":
            raise Exception("c4 composition is not implemented yet!")
            # return c4.multiple_workflows_c4
        else:
            raise ValueError(f"Not a valid method option: {name}")

    def find_critical_tasks(self):
        self.all_comp_cost = sum(wf.avg_comp_cost for wf in self.workflows)
        self.critical_tasks = [t for wf in self.workflows for t in wf.tasks if ((t.runtime / self.all_comp_cost) * 100) > 5]

    def holes_scheduling_critical_tasks(self):
        """This method is used to schedule with method holes.

        This basically tries to creates as many holes it can in the schedule
        on perpuse so it can fill them later with tasks with high computation
        cost and low communication cost.
        """
        if self.schedule_wfs_order is None:
            self.find_critical_tasks()
            self.schedule_order_for_critical_tasks()

        for wf_id in self.schedule_wfs_order:
            self.schedule_workflow(self.workflows[wf_id], TimeType.EFT)

    def schedule_order_for_critical_tasks(self):
        self.schedule_wfs_order = [self.workflows[i].id for i in [t.wf_id for t in sorted(self.critical_tasks, key=lambda t: t.runtime, reverse=True)]]
        self.add_left_out_wfs_in_order()

    def ccr_schedule_order(self):
        self.schedule_wfs_order = []
        sorted_wfs = sorted(self.workflows, key=lambda wf_: wf_.ccr, reverse=True)
        j = len(sorted_wfs) - 1
        for i in range(len(sorted_wfs) // 2):
            self.schedule_wfs_order.append(sorted_wfs[i].id)
            self.schedule_wfs_order.append(sorted_wfs[j].id)
            j -= 1
        self.add_left_out_wfs_in_order()

    def add_left_out_wfs_in_order(self):
        for wf in self.workflows:
            if wf.id not in self.schedule_wfs_order:
                self.schedule_wfs_order.append(wf.id)

    def holes_scheduling(self):
        """This method is used to schedule with method holes.

        This basically tries to creates as many holes it can in the schedule
        on perpuse so it can fill them later with tasks with high computation
        cost and low communication cost.
        """
        if self.schedule_wfs_order is None:
            self.ccr_schedule_order()

        for i, wf_id in enumerate(self.schedule_wfs_order):
            self.schedule_workflow(self.workflows[wf_id], self.time_types[i % 2])

    def view_machine_holes(self):
        for m in self.machines:
            print(f"M[{m.id}]")
            # print(m)
            for hole in m.holes:
                print(f"\t{hole}")

    def example_hole_scheduling(self):
        self.schedule_workflow(self.workflows[1], self.time_types[0])
        self.avg_workflow_makespan = sum(wf.wf_len for wf in self.workflows) / len(self.workflows)

    def schedule_workflow(self, wf, time_type):
        unscheduled = sorted(wf.get_ready_unscheduled_tasks(), key=lambda t: t.up_rank, reverse=True)
        self.schedule_tasks(unscheduled, time_type)
        wf.set_scheduled(True)

    def schedule_tasks(self, unscheduled, time_type):
        i = 0
        while len(unscheduled) > 0:
            if i >= len(unscheduled):
                i = 0
            un_task = unscheduled[i]

            if un_task.status == TaskStatus.READY:
                Scheduler.schedule_task_machine_or_hole(un_task, self.machines, time_type, self.fill_method)
                unscheduled.pop(i)
                i = 0
            else:
                i += 1

    def holes2011(self):
        def __schedule_workflows(wf, priority_type):
            # 1. Sort tasks in workflows based on the priority_type
            #   - EDF:  The deadline time from each workflow.
            #   - HLF:  Up-rank as usual.
            #   - LSTF: wf_deadline - curr_time - up_rank
            unscheduled = []

            if priority_type == PriorityType.HLF:
                unscheduled = sorted(wf.tasks, key=lambda t: t.up_rank)
            elif priority_type == PriorityType.EDF:
                # for t in wf.tasks:
                #     if t.wf_deadline is None:
                #         raise Exception("deadline is NONE")
                unscheduled = list(wf.tasks)
            elif priority_type == PriorityType.LSTF:
                curr_time = max(self.machines, key=lambda m: m.time_on_machine).time_on_machine
                unscheduled = sorted(wf.tasks, key=lambda t: t.calc_lstf(time=curr_time))

            self.schedule_tasks(unscheduled, TimeType.EST)

        for wf in self.workflows:
            __schedule_workflows(wf, self.priority_type)

        self.set_wfs_scheduled()

    def schedule_tasks_round_robin_heft(unscheduled, machines, n_wfs):
        diff_wfs = set()

        i = 0
        wfs_remaining = n_wfs
        # Schedule the first connecting dag because its wf_id is -1
        Scheduler.schedule_task_machine(unscheduled.pop(0), machines, TimeType.EFT)
        while unscheduled:
            if len(unscheduled) == i:
                i = 0
            task = unscheduled[i]

            # Task is not ready yet go to the next one
            if task.parents_till_ready != 0 or task.wf_id in diff_wfs:
                i += 1
            else:
                Scheduler.schedule_task_machine(task, machines, TimeType.EFT)
                if task.name.startswith("Dummy-Out") or (task.children_names is not None and len(task.children_names)) == 0:
                    wfs_remaining -= 1
                diff_wfs.add(task.wf_id)
                # print(f"Scheduled: {task}")
                # print(task.str_colored())
                unscheduled.pop(i)
                i -= 1

            # If we end up looping through all the workflows
            # then go ahead and reset the set.
            if len(diff_wfs) >= wfs_remaining:
                diff_wfs = set()

    @staticmethod
    def schedule_tasks_heft(unscheduled, machines):
        for task in unscheduled:
            Scheduler.schedule_task_machine(task, machines, TimeType.EFT)

    def schedule_tasks_cpop(self, queue, critical_info):
        critical_path = critical_info[0]
        critical_machine_id = critical_info[1]

        while queue:
            # mpt -> max priority task
            # probably can make these two together later on
            mpt = max(queue, key=lambda t: t.priority)
            for i in range(len(queue)):
                if queue[i].id == mpt.id:
                    queue.pop(i)
                    break
            if mpt in critical_path:
                # Here we send on purpose only the critical_machine
                Scheduler.schedule_tasks_heft([mpt], [self.machines[critical_machine_id]])
            else:
                # You run schedule_tasks and you simply send just one task so it works fine.
                Scheduler.schedule_tasks_heft([mpt], self.machines)
            for child_edge in mpt.children_edges:
                child = child_edge.node
                # The status of the child gets updated by the parent. In more details the every task
                # has a counter called "parents_till_ready" every parent that gets scheduled reduce
                # this value by once for his children.
                if child.status == TaskStatus.READY:
                    queue.append(child)

    @staticmethod
    def pick_machine_based_on_timetype(time_type, times):
        # Prioritize to fill the holes first.
        if time_type == TimeType.EST:
            time = min(times, key=compare_start)
        elif time_type == TimeType.EFT:
            time = min(times, key=compare_end)
        elif time_type == TimeType.LST:
            time = max(times, key=compare_start)
        elif time_type == TimeType.LFT:
            time = max(times, key=compare_end)
        else:
            raise ValueError(f"This is not a valid time_type: {time_type}")
        return time

    @staticmethod
    def schedule_task_machine_or_hole(task, machines, time_type, fill_method=FillMethod.NO_FILL):
        if task.status != TaskStatus.READY:
            raise Exception("Task is not ready! ", task)

        start, end, machine, hole = Scheduler.find_hole_or_machine(task, machines, time_type, fill_method)
        Scheduler.schedule_task((start, end), task, machine=machine, hole=hole)

    @staticmethod
    def schedule_task_machine(task, machines, time_type, fill_method=FillMethod.NO_FILL):
        if task.status != TaskStatus.READY:
            raise Exception(f"Task[{task.id}] wf[{task.wf_id}] has not ready state! It has status of: {task.status}")
        start, end, machine = Scheduler.find_machine(task, machines, time_type)

        Scheduler.schedule_task((start, end), task, machine=machine)

    @staticmethod
    def find_machine(task, machines, time_type):
        times = []
        best_time = None
        for machine in machines:
            start, end = compute_execution_time(task, machine.id, machine.time_on_machine)
            times.append({"machine": machine, "start": start, "end": end})
        best_time = Scheduler.pick_machine_based_on_timetype(time_type, times)

        if best_time is None:
            raise ValueError(f"No machine was assigned to: {task}")
        return best_time["start"], best_time["end"], best_time["machine"]

    @staticmethod
    def find_hole_or_machine(task, machines, time_type, fill_method):
        holes_times = []
        best_time = None
        for machine in machines:
            # Try to find the existing holes (in the current machine) to fill.
            if fill_method != FillMethod.NO_FILL:
                for hole in machine.holes:
                    start, end = compute_execution_time(task, machine.id, hole.start)
                    if hole.is_fillable(end):
                        holes_times.append({"machine": machine, "hole": hole, "start": start, "end": end, "gap_left": hole.gap - (end - start)})

        if not holes_times:
            return *Scheduler.find_machine(task, machines, time_type), None
        if fill_method == FillMethod.FASTEST_FIT:
            best_time = Scheduler.pick_machine_based_on_timetype(time_type, holes_times)
        elif fill_method == FillMethod.BEST_FIT:
            best_time = min(holes_times, key=lambda t: t["gap_left"])
        elif fill_method == FillMethod.FIRST_FIT:
            best_time = sorted(holes_times, key=lambda t: t['start'])[0]
        elif fill_method == FillMethod.WORST_FIT:
            best_time = max(holes_times, key=lambda t: t["gap_left"])
        return best_time["start"], best_time["end"], best_time["machine"], best_time['hole']

    # @staticmethod
    # def schedule_task_to_best_machine1(task, machines, time_type, fill_method=FillMethod.NO_FILL):
    #     if task.status != TaskStatus.READY:
    #         raise Exception("Task is not ready! ", task)
    #     start, end, machine, hole = Scheduler.find_machine(task, machines, time_type, fill_method)

    #     Scheduler.schedule_task((start, end), task, machine=machine, hole=hole)

    # @staticmethod
    # def find_best_machine1(task, machines, time_type, fill_method=FillMethod.NO_FILL):
    #     holes_times = []
    #     task_times_on_machines = []
    #     best_time = None
    #     for machine in machines:
    #         # Try to find the existing holes (in the current machine) to fill.
    #         if fill_method != FillMethod.NO_FILL:
    #             for hole in machine.holes:
    #                 start, end = compute_execution_time(task, machine.id, hole.start)
    #                 if hole.is_fillable(end):
    #                     holes_times.append({"machine": machine, "hole": hole, "start": start, "end": end, "gap_left": hole.gap - (end - start)})

    #         # If no valid holes were found try to look into the current machine
    #         # and find the execution time of the specific task in the machine.
    #         if len(holes_times) == 0:
    #             start, end = compute_execution_time(task, machine.id, machine.time_on_machine)
    #             task_times_on_machines.append({"machine": machine, "start": start, "end": end})

    #     # If there are holes to fill prioritize them.
    #     if len(holes_times) > 0:
    #         if fill_method == FillMethod.FASTEST_FIT:
    #             best_time = Scheduler.pick_machine_based_on_timetype(time_type, holes_times)
    #         elif fill_method == FillMethod.BEST_FIT:
    #             best_time = min(holes_times, key=lambda t: t["gap_left"])
    #         elif fill_method == FillMethod.FIRST_FIT:
    #             best_time = sorted(holes_times, key=lambda t: t['start'])[0]
    #         elif fill_method == FillMethod.WORST_FIT:
    #             best_time = max(holes_times, key=lambda t: t["gap_left"])
    #     # If no holes were found.
    #     else:
    #         # best_time = Scheduler.pick_machine_based_on_timetype(time_type, task_times_on_machines)
    #         best_time = Scheduler.pick_machine_based_on_making_holes(task, task_times_on_machines)
    #         # best_time = Scheduler.pick_machine_based_on_timetype(time_type, task_times_on_machines)

    #     if best_time is None:
    #         raise ValueError(f"No machine or hole was assigned to: {task}")
    #     return best_time["start"], best_time["end"], best_time["machine"], best_time.get('hole')

    @staticmethod
    def pick_machine_based_on_making_holes(task, times):
        def actual_time(nt, m):
            return nt * m.n_cpu / 4
        # EFT
        eft = min(times, key=compare_end)
        eft_gap = eft['start'] - eft['machine'].time_on_machine
        best_time = None
        for t in times:
            if t is eft:
                continue
            m = t['machine']
            gap = t['start'] - m.time_on_machine
            time_saved = actual_time(gap, m)
            if time_saved > actual_time(t['end'] + eft_gap - eft['end'], eft['machine']):
                if best_time is not None and best_time['val'] < time_saved:
                    best_time = t
                    best_time['val'] = time_saved
                else:
                    best_time = {**t, 'val': time_saved}
        if best_time is None:
            best_time = eft
        return best_time

    @staticmethod
    def heft(tasks, machines):
        # Phase 1
        calculate_upward_ranks(tasks)
        # We sort the tasks based of their up_rank
        tasks.sort(key=lambda task: task.up_rank, reverse=True)
        # Phase 2
        Scheduler.schedule_tasks_heft(tasks, machines)

    @staticmethod
    def round_robin_heft(tasks, machines, n_wfs):
        calculate_upward_ranks(tasks)
        tasks.sort(key=lambda task: task.up_rank, reverse=True)

        Scheduler.schedule_tasks_round_robin_heft(tasks, machines, n_wfs)

    @staticmethod
    def cpop(wf):
        critical_path, [entry_node, _] = wf.create_critical_path()
        critical_machine_id = Scheduler.pick_machine_for_critical_path(critical_path, wf.machines)
        Scheduler.schedule_tasks_cpop(wf.machines, [entry_node], (critical_path, critical_machine_id))

    def multiple_workflows_c1(self):
        all_tasks = Workflow.connect_wfs(self.workflows, self.machines)
        Scheduler.heft(all_tasks, self.machines)
        self.set_wfs_scheduled()

    def set_wfs_scheduled(self):
        for wf in self.workflows:
            if not wf.scheduled:
                wf.set_scheduled(True)

    def multiple_workflows_c2(self):
        # 1. Connect all workflows with one "BIG" entry node and one "BIG" exit node.
        all_tasks = Workflow.connect_wfs(self.workflows, self.machines)
        # 2. Get the level for each task.
        levels = Workflow.level_order(all_tasks)

        # 3. Schedule based of the order of their level
        # Maybe we should run heft based of how many levels we have.
        for level, tasks in levels.items():
            if len(tasks) > 0:
                Scheduler.heft(tasks, self.machines)
        self.set_wfs_scheduled()

    def multiple_workflows_c3(self):
        # 1. Connect all workflows with one "BIG" entry node and one "BIG" exit node.
        all_tasks = Workflow.connect_wfs(self.workflows, self.machines)
        # 2. Run HEFT in round-robin-fashion
        Scheduler.round_robin_heft(all_tasks, self.machines, len(self.workflows))
        self.set_wfs_scheduled()

    @staticmethod
    def pick_machine_for_critical_path(critical_path, machines):
        machines_costs = []
        for machine in machines:
            machine_critical_cost = sum(task.costs[machine.id] for task in critical_path)
            machines_costs.append((machine_critical_cost, machine.id))

        # Machine selected for the critical path
        return min(machines_costs, key=lambda tup: tup[0])[1]


# Running this function means we already have
# as a fact that all the parent tasks are done
# before we get in here and check for the slowest parent
def compute_execution_time(task, m_id, potensial_start_time):
    """Find the execution time of a task on a machine based on given start_time.

    Parameters
    ----------
    task : Task
        The task we want to find the execution time for.
    m_id : int
        Machine id.
    potensial_start_time : float
        This can be either the current time of a machine or the start time of a hole in a machine.

    Returns
    -------
    Tuple[float, float]
        The potential start time and end time of the task on the machine.
    """
    # If between the child and the parent the machine doesn't change
    # then the communication cost is 0.
    if task.is_entry:
        return [potensial_start_time, potensial_start_time + task.costs[m_id]]
    elif task.slowest_parent['parent_task'].machine_id == m_id:
        communication_time = 0
    else:
        # The com_time was calculated at the parsing phase.
        communication_time = task.slowest_parent['communication_time']

    #  parent_end + communication_time + cost_of_task_in_this_machine
    # We pick the one that is bigger so we can ensure the child task starts
    # after the parent.
    start = max(task.slowest_parent['parent_task'].end + communication_time, potensial_start_time)
    end = start + task.costs[m_id]
    return [start, end]


def compare_start(times):
    return times["start"]


def compare_end(times):
    return times["end"]


def get_time_type(ttype):
    if ttype.__class__ == str:
        if ttype == "EFT":
            return TimeType.EFT
        elif ttype == "EST":
            return TimeType.EST
        elif ttype == "LFT":
            return TimeType.LFT
        elif ttype == "LST":
            return TimeType.LST
    elif ttype == TimeType.EFT:
        return "EFT"
    elif ttype == TimeType.EST:
        return "EST"
    elif ttype == TimeType.LST:
        return "LST"
    elif ttype == TimeType.LFT:
        return "LFT"
    raise ValueError(f"Not supported Time Type: {ttype}")


def get_fill_method(fmethod):
    if fmethod.__class__ == str:
        if fmethod == "BEST-FIT":
            return FillMethod.BEST_FIT
        elif fmethod == "FASTEST-FIT":
            return FillMethod.FASTEST_FIT
        elif fmethod == "FIRST-FIT":
            return FillMethod.FIRST_FIT
        elif fmethod == "NO-FILL":
            return FillMethod.NO_FILL
        elif fmethod == "WORST-FIT":
            return FillMethod.WORST_FIT
    elif fmethod == FillMethod.FASTEST_FIT:
        return "FASTEST"
    elif fmethod == FillMethod.BEST_FIT:
        return "BEST"
    elif fmethod == FillMethod.FIRST_FIT:
        return "FIRST"
    elif fmethod == FillMethod.WORST_FIT:
        return "WORST"
    elif fmethod == FillMethod.NO_FILL:
        return "NO"

    raise ValueError(f"Not supported Fill Type: {fmethod}")


def get_priority_type(priority):
    if priority is None:
        return priority
    if priority == "EDF":
        return PriorityType.EDF
    elif priority == "HLF":
        return PriorityType.HLF
    elif priority == "LSTF":
        return PriorityType.LSTF
