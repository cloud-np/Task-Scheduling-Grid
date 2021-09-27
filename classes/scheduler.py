from enum import Enum
from typing import List, Any
import os
from colorama import Fore, Back
from classes.workflow import Workflow
from classes.task import TaskStatus
from matplotlib.pyplot import fill
from algos.calc_task_ranks import calculate_upward_ranks
import algos.wf_compositions.c1 as c1
import algos.wf_compositions.c2 as c2
import algos.wf_compositions.c3 as c3
# from algos.wf_compositions import c2
# from algos.wf_compositions import c3
# from algos.wf_compositions import c4


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


class Scheduler:
    def __init__(self, name: str, data, time_types: List[str], fill_method: FillMethod, priority_type=None, output_path: str = "./simulation_output"):
        workflows, machines = data
        self.name: str = name
        self.n_wfs: int = len(workflows)
        self.n_machines: int = len(machines)
        self.workflows = workflows
        self.machines = machines
        self.output_path: str = output_path
        # E.g: sim_out/5.txt
        self.output_file: str = f"{self.output_path}/wf_size_{len(workflows[0].tasks)}_machines_{self.n_machines}.txt"
        self.time_types_str = time_types

        if time_types is not None:
            # Get time types e.g: EFT = earliest finish time
            self.time_types: List[TimeType] = [get_time_type(ttype) for ttype in time_types]

        self.priority_type_str = priority_type
        self.priority_type: PriorityType = get_priority_type(priority_type)

        # Get fill type e.g: FASTEST-FIT = pick the hole that has gives the best time.
        self.fill_method: FillMethod = get_fill_type(fill_method)
        # The method that we gonna run the schedule.
        self.schedule_method: Any = self.get_scheduling_method(name)

        self.is_scheduling_done: bool = False

    # This function schedules the task and returns the new
    @staticmethod
    def schedule_task(sch_time, task, machine, hole):
        task.machine_id = machine.id
        task.start = sch_time['start']
        task.end = sch_time['end']
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

    def info(self):
        print(f"\t{Back.MAGENTA}{Fore.LIGHTYELLOW_EX}{self.method_used_info()}{Fore.RESET}{Back.RESET}")
        if self.name.startswith("holes"):
            # for machine in self.machines:
            #     print(machine.holes_filled)
            print(f"Time saved = {Fore.GREEN}{sum([m.holes_saved_time for m in self.machines])}{Fore.RESET}")

        slowest_machine = self.get_slowest_machine()
        print(f'\n{slowest_machine.str_col_id()}\n{slowest_machine.str_col_schedule_len()}\n')

    def get_whole_idle_time(self):
        return sum([m.get_idle_time() for m in self.machines])

    def run(self):
        self.schedule_method()
        # if self.schedule_method.__name__.startswith("holes"):
        #     self.schedule_method()
        # else:
        #     self.schedule_method(self.workflows, self.machines)
        self.is_scheduling_done = True

    def method_used_info(self, concise=False):
        fill_method = None
        if self.name.startswith("holes"):
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
                fill_method = get_fill_type(self.fill_method)

            if self.name.startswith("holes2011"):
                return f"{fill_method} {self.priority_type_str}\n"
            else:
                ttypes = [get_time_type(t) for t in self.time_types]
                return f"{fill_method}\n{ttypes[0]}-{ttypes[1]}\n"
        else:
            return self.name

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

    def get_holes_filled(self):
        return sum([m.holes_filled for m in self.machines])

    def get_schedule_len(self):
        slowest_machine = self.get_slowest_machine()
        return slowest_machine.time_on_machine

    def get_info_for_files(self) -> List[str]:
        schedule_len = self.get_schedule_len()
        self.machines_util_avg_perc = sum(m.get_util_perc(schedule_len) for m in self.machines) / self.n_machines

        self.workflows_avg_schedule_len = sum(wf.wf_len for wf in self.workflows) / self.n_wfs

        name_info = "".join([f"-{time_type}" for time_type in self.time_types_str] if self.time_types_str is not None else "")

        return [f"{self.name}-{name_info} ", f"{schedule_len}\t", f"{self.machines_util_avg_perc}\t", f"{self.workflows_avg_schedule_len}\n"]

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
            titles: str = "Method Name\tTotal Makespan\tAvg Machine util\tAvg workflow makespan"
            lines.insert(0, titles + '\n')

        # Append to the correct file if it exists otherwise create it.
        with open(self.output_file, "a+") as f:
            f.writelines(lines)

    def get_scheduling_method(self, name):
        if name.startswith("holes2011"):
            return self.holes2011
        elif name.startswith("holes"):
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

    def holes_scheduling(self):
        """This method is used to schedule with method holes.

        This basically tries to creates as many holes it can in the schedule
        on perpuse so it can fill them later with tasks with high computation
        cost and low communication cost.

        Args:
            workflows (list(Workflow)): Contains information about the workflows.
            machines (list(Machine)): Contains information about the machines.
            time_types (list(TimeType)): Shows the time type we should use for each workflow to be schedules with. e.g: EFT - EST
        """
        # sorted_wfs = sorted(self.workflows, key=lambda wf_: wf_.ccr, reverse=True)
        # sorted_wfs = self.workflows
        sorted_wfs = sorted(self.workflows, key=lambda wf_: wf_.ccr)

        j = len(sorted_wfs) - 1
        for i in range(len(sorted_wfs) // 2):
            self.schedule_workflow(sorted_wfs[i], self.time_types[0])
            self.schedule_workflow(sorted_wfs[j], self.time_types[1])
            j -= 1

        # This is incase we have an odd number of workflows so one is left out without a pair.
        # Not the cleanest way to handle this but works for now.
        for wf in self.workflows:
            if wf.scheduled is False:
                self.schedule_workflow(wf, self.time_types[0])

    def schedule_workflow(self, wf, time_type):
        unscheduled = sorted(wf.tasks, key=lambda t: t.up_rank, reverse=True)

        i = 0
        while len(unscheduled) > 0:
            if i >= len(unscheduled):
                i = 0
            un_task = unscheduled[i]

            if un_task.status == TaskStatus.READY:
                Scheduler.schedule_task_to_best_machine(un_task, self.machines, time_type, self.fill_method)
                unscheduled.pop(i)
                i = 0
            else:
                i += 1

        wf.set_scheduled(True)

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
                for t in wf.tasks:
                    if t.wf_deadline is None:
                        raise Exception("deadline is NONE")
                unscheduled = sorted(wf.tasks, key=lambda t: t.wf_deadline)
            elif priority_type == PriorityType.LSTF:
                unscheduled = sorted(wf.tasks, key=lambda t: t.calc_lstf(time=0))

            i = 0
            while len(unscheduled) > 0:
                if i >= len(unscheduled):
                    i = 0
                task = unscheduled[i]
                if task.status == TaskStatus.READY:
                    Scheduler.schedule_task_to_best_machine(task, self.machines, TimeType.EFT, self.fill_method)
                    unscheduled.pop(i)
                i += 1
            wf.set_scheduled(True)

        for wf in self.workflows:
            __schedule_workflows(wf, self.priority_type)

    def schedule_tasks_round_robin_heft(unscheduled, machines, n_wfs):
        diff_wfs = set()

        i = 0
        wfs_remaining = n_wfs
        # Schedule the first connecting dag because its wf_id is -1
        Scheduler.schedule_task_to_best_machine(unscheduled.pop(0), machines, TimeType.EFT)
        while unscheduled:
            if len(unscheduled) == i:
                i = 0
            task = unscheduled[i]

            # Task is not ready yet go to the next one
            if task.parents_till_ready != 0 or task.wf_id in diff_wfs:
                i += 1
            else:
                Scheduler.schedule_task_to_best_machine(task, machines, TimeType.EFT)
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
            Scheduler.schedule_task_to_best_machine(task, machines, TimeType.EFT)

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
    def schedule_task_to_best_machine(task, machines, time_type, fill_method=FillMethod.NO_FILL):
        if task.status != TaskStatus.READY:
            raise Exception("Task status is not ready! ", task)
        time_and_machine = Scheduler.find_best_machine(task, machines, time_type, fill_method)

        Scheduler.schedule_task({'start': time_and_machine["start"], 'end': time_and_machine["end"]},
                                task, machine=time_and_machine["machine"], hole=time_and_machine.get('hole'))

    @staticmethod
    def find_best_machine(task, machines, time_type, fill_method=FillMethod.NO_FILL):
        holes_times = []
        task_times_on_machines = []
        best_time = None
        for machine in machines:
            # Try to find the existing holes (in the current machine) to fill.
            if fill_method != FillMethod.NO_FILL:
                for hole in machine.holes:
                    valid_hole_info = hole.is_fillable(task, machine.id)
                    if valid_hole_info is not None:
                        holes_times.append({"machine": machine, "hole": hole, **valid_hole_info})

            # If no valid holes were found try to look into the current machine
            # and find the execution time of the specific task in the machine.
            if len(holes_times) == 0:
                [start, end] = compute_execution_time(task, machine.id, machine.time_on_machine)
                task_times_on_machines.append({"machine": machine, "start": start, "end": end})

        # If there are holes to fill prioritize them.
        if len(holes_times) > 0:
            if fill_method == FillMethod.FASTEST_FIT:
                best_time = Scheduler.pick_machine_based_on_timetype(time_type, holes_times)
            elif fill_method == FillMethod.BEST_FIT:
                best_time = min(holes_times, key=lambda t: t["gap_left"])
            elif fill_method == FillMethod.FIRST_FIT:
                # We could write this to run faster but I think we will losse readility
                best_time = holes_times[0]
            elif fill_method == FillMethod.WORST_FIT:
                best_time = max(holes_times, key=lambda t: t["gap_left"])
        # If no holes were found.
        else:
            best_time = Scheduler.pick_machine_based_on_timetype(time_type, task_times_on_machines)

        if best_time is None:
            raise ValueError(
                f"No machine or hole was assigned to: {task}")
        return best_time

    @staticmethod
    def heft(tasks, machines):
        # Phase 1
        calculate_upward_ranks(tasks)
        # We sort the tasks based of their up_rank
        tasks.sort(key=lambda task: task.up_rank, reverse=True)
        # Phase 2
        Scheduler.schedule_tasks_heft(tasks, machines)
        return {'tasks': tasks, 'machines': machines}

    @staticmethod
    def round_robin_heft(tasks, machines, n_wfs):
        calculate_upward_ranks(tasks)
        tasks.sort(key=lambda task: task.up_rank, reverse=True)

        Scheduler.schedule_tasks_round_robin_heft(tasks, machines, n_wfs)

        return {'tasks': tasks, 'machines': machines}

    @staticmethod
    def cpop(wf):
        critical_path, [entry_node, _] = wf.create_critical_path()
        critical_machine_id = Scheduler.pick_machine_for_critical_path(
            critical_path, wf.machines)
        Scheduler.schedule_tasks_cpop(wf.machines, [entry_node], (critical_path, critical_machine_id))
        return {'tasks': wf.tasks, 'machines': wf.machines}

    def multiple_workflows_c1(self):
        all_tasks = Workflow.connect_wfs(self.workflows, self.machines)
        return Scheduler.heft(all_tasks, self.machines)

    def multiple_workflows_c2(self):
        all_tasks = Workflow.connect_wfs(self.workflows, self.machines)
        return Scheduler.heft(all_tasks, self.machines)
        # 1. Connect all workflows with one "BIG" entry node and one "BIG" exit node.
        all_tasks = Workflow.connect_wfs(self.workflows, self.machines)
        # 2. Get the level for each task.
        levels = Workflow.level_order(all_tasks)

        # 3. Schedule based of the order of their level
        # Maybe we should run heft based of how many levels we have.
        for level, tasks in levels.items():
            if len(tasks) > 0:
                return Scheduler.heft(tasks, self.machines)

    def multiple_workflows_c3(self):
        # 1. Connect all workflows with one "BIG" entry node and one "BIG" exit node.
        all_tasks = Workflow.connect_wfs(self.workflows, self.machines)
        # 2. Run HEFT in round-robin-fashion
        return Scheduler.round_robin_heft(all_tasks, self.machines, len(self.workflows))
    # @staticmethod
    # def pick_machine_for_critical_path(critical_path, machines):
    #     machines_costs = []
    #     for machine in machines:
    #         machine_critical_cost = 0
    #         for task in critical_path:
    #             machine_critical_cost += task.costs[machine.id]
    #         machines_costs.append((machine_critical_cost, machine.id))

    #     # Machine selected for the critical path
    #     return min(machines_costs, key=lambda tup: tup[0])[1]


# Running this function means we already have
# as a fact that all the parent tasks are done
# before we get in here and check for the slowest parent
def compute_execution_time(task, m_id, start_time):
    # TODO: Maybe can just change this to DummyIn
    #       not worth looking atm...
    if task.name.startswith('Dummy'):
        # This is only for the dummy OUT node
        if task.is_exit is True:
            return [start_time, start_time]
        # This is only for the dummy IN node
        else:
            return [0, 0]
        # If between the child and the parent the machine doesn't change
        # then the communication cost is 0.
    elif task.is_entry:
        return [start_time, start_time + task.costs[m_id]]
    elif task.slowest_parent['parent_task'].machine_id == m_id:
        communication_time = 0
    else:
        # The com_time was calculated at the parsing phase.
        communication_time = task.slowest_parent['communication_time']

    #  parent_end + communication_time + cost_of_task_in_this_machine
    # We pick the one that is bigger so we can ensure the child task starts
    # after the parent.
    start = max(task.slowest_parent['parent_task'].end + communication_time, start_time)
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
        elif ttype == "LST":
            return TimeType.LST
        elif ttype == "LFT":
            return TimeType.LFT
    else:
        if ttype == TimeType.EFT:
            return "EFT"
        elif ttype == TimeType.EST:
            return "EST"
        elif ttype == TimeType.LST:
            return "LST"
        elif ttype == TimeType.LFT:
            return "LFT"
    raise ValueError(f"Not supported Time Type: {ttype}")


def get_fill_type(ftype):
    if ftype.__class__ == str:
        if ftype == "FASTEST-FIT":
            return FillMethod.FASTEST_FIT
        elif ftype == "BEST-FIT":
            return FillMethod.BEST_FIT
        elif ftype == "FIRST-FIT":
            return FillMethod.FIRST_FIT
        elif ftype == "WORST-FIT":
            return FillMethod.WORST_FIT
        elif ftype == "NO-FILL":
            return FillMethod.NO_FILL
    else:
        if ftype == FillMethod.FASTEST_FIT:
            return "FASTEST"
        elif ftype == FillMethod.BEST_FIT:
            return "BEST"
        elif ftype == FillMethod.FIRST_FIT:
            return "FIRST"
        elif ftype == FillMethod.WORST_FIT:
            return "WORST"
        elif ftype == FillMethod.NO_FILL:
            return "NO"

    raise ValueError(f"Not supported Fill Type: {ftype}")


def get_priority_type(priority):
    if priority is None:
        return priority
    if priority == "EDF":
        return PriorityType.EDF
    elif priority == "HLF":
        return PriorityType.HLF
    elif priority == "LSTF":
        return PriorityType.LSTF
