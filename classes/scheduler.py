from enum import Enum
from typing import List, Any
import os
from colorama import Fore, Back
from matplotlib.pyplot import fill
import algos.schedule_wfs as algos
from algos.wf_compositions import c1
from algos.wf_compositions import c2
from algos.wf_compositions import c3
from algos.wf_compositions import c4


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
    def __init__(self, name: str, workflows, machines, time_types: List[str], fill_type: FillMethod, priority_type=None, output_path: str = "./simulation_output"):
        self.name: str = name
        self.n_wfs: int = len(workflows)
        self.n_machines: int = len(machines)
        self.workflows = workflows
        self.machines = machines
        self.output_path: str = output_path
        # E.g: sim_out/5.txt
        self.output_file: str = f"{self.output_path}/wf_size_{len(workflows[0].tasks)}_machines_{self.n_machines}.txt"

        if time_types is not None:
            # Get time types e.g: EFT = earliest finish time
            self.time_types: List[TimeType] = [self.get_time_type(ttype) for ttype in time_types]

        if priority_type is not None:
            self.priority_type: PriorityType = self.get_priority_type(priority_type)

        # Get fill type e.g: FASTEST-FIT = pick the hole that has gives the best time.
        # NOTE change this to fill_method
        self.fill_type: FillMethod = self.get_fill_type(fill_type)
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
            return max(self.machines, key=lambda m: m.schedule_len)
        else:
            raise Exception("You should run the scheduling method first.")

    def info(self):
        print(f"\t{Back.MAGENTA}{Fore.LIGHTYELLOW_EX}{self.method_used_info()}{Fore.RESET}{Back.RESET}")
        if self.name.startswith("holes"):
            # for machine in self.machines:
            #     print(machine.holes_filled)
            print(
                f"Time saved = {Fore.GREEN}{sum([m.holes_saved_time for m in self.machines])}{Fore.RESET}")

        slowest_machine = self.get_slowest_machine()
        print(
            f'\n{slowest_machine.str_col_id()}\n{slowest_machine.str_col_schedule_len()}\n')

    @staticmethod
    def get_priority_type(priority):
        if priority == "EDF":
            return PriorityType.EDF
        elif priority == "HLF":
            return PriorityType.HLF
        elif priority == "LSTF":
            return PriorityType.LSTF

    def run(self):
        if self.schedule_method.__name__.startswith("schedule_workflow_2011_paper"):
            if self.priority_type is None:
                raise Exception("Please give a priority type!")
            self.schedule_method(self.workflows, self.machines, self.priority_type, self.fill_type)
        elif self.schedule_method.__name__.startswith("holes"):
            self.schedule_method(self.workflows, self.machines, self.time_types, self.fill_type)
        else:
            self.schedule_method(self.workflows, self.machines)
        self.is_scheduling_done = True

    def method_used_info(self, concise=False):
        fill_type = None
        if self.name.startswith("holes"):
            if concise:
                if self.fill_type == FillMethod.FASTEST_FIT:
                    fill_type = "FST"
                elif self.fill_type == FillMethod.BEST_FIT:
                    fill_type = "B"
                elif self.fill_type == FillMethod.FIRST_FIT:
                    fill_type = "FR"
                elif self.fill_type == FillMethod.WORST_FIT:
                    fill_type = "W"
            else:
                fill_type = self.get_fill_type(self.fill_type)

            if self.name.startswith("holes2011"):
                return f"{fill_type} {self.priority_type}\n"
            else:
                ttypes = [Scheduler.get_time_type(t) for t in self.time_types]
                return f"{fill_type}\n{ttypes[0]}-{ttypes[1]}\n"
        else:
            return self.name

    def get_scheduled_info(self):
        def add_nl(_str):
            return f"{_str}\n"
        method_info = self.method_used_info()
        holes_filled: int = 0
        time_saved = None
        if self.name.startswith("holes"):
            for machine in self.machines:
                holes_filled += machine.holes_filled
            time_saved = sum([m.holes_saved_time for m in self.machines])

        slowest_machine = self.get_slowest_machine()
        m_id = slowest_machine.str_id()
        schedule_len = slowest_machine.str_schedule_len()

        return [method_info, f"Holes Filled {holes_filled}", add_nl(time_saved), add_nl(m_id), add_nl(schedule_len)]

    def get_schedule_len(self):
        slowest_machine = self.get_slowest_machine()
        return slowest_machine.schedule_len

    def get_info_for_files(self) -> List[str]:
        schedule_len = self.get_schedule_len()
        machines_util_avg_perc = sum(m.get_util_perc() for m in self.machines) / self.n_machines

        workflows_avg_schedule_len = sum(wf.schedule_len for wf in self.workflows) / self.n_wfs

        return [f"{self.name},", f"{round(schedule_len)},", f"{round(machines_util_avg_perc)},", f"{round(workflows_avg_schedule_len)}\n"]

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
            titles: str = "Method Name,Total Makespan,Avg Machine util,Avg workflow makespan"
            lines.insert(0, titles + '\n')

        # Append to the correct file if it exists otherwise create it.
        with open(self.output_file, "a+") as f:
            f.writelines(lines)

    @staticmethod
    def get_scheduling_method(name):
        if name.startswith("holes2011"):
            return algos.schedule_workflow_2011_paper
        elif name.startswith("holes"):
            return algos.holes_scheduling
        elif name == "c1":
            return c1.multiple_workflows_c1
        elif name == "c2":
            return c2.multiple_workflows_c2
        elif name == "c3":
            return c3.multiple_workflows_c3
        elif name == "c4":
            raise Exception("c4 composition is not implemented yet!")
            # return c4.multiple_workflows_c4
        else:
            raise ValueError(f"Not a valid method option: {name}")

    @staticmethod
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

    @staticmethod
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
