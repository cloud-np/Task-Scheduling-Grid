from enum import Enum
from typing import List
from colorama import Fore, Back
from algos.holes_scheduling import holes_scheduling
from compositions import c1
from compositions import c2
from compositions import c3
from compositions import c4


class TimeType(Enum):
    EST = 0
    EFT = 1
    LST = 2
    LFT = 3


class FillMethod(Enum):
    NO_FILL = -1
    FASTEST_FIT = 0
    BEST_FIT = 1
    FIRST_FIT = 2
    WORST_FIT = 3


class Schedule:

    def __init__(self, name, workflows, machines, time_types: List[str], fill_type):
        self.name = name
        self.workflows = workflows
        self.machines = machines

        # Get time types e.g: EFT = earliest finish time
        if len(time_types) != 1 and len(time_types) != 2:
            raise ValueError(f"Time types should not be more than 2 or less than 1 you entered: {time_types}")

        self.time_types = [self.get_time_type(ttype) for ttype in time_types]

        # Get fill type e.g: FASTEST-FIT = pick the hole that has gives the best time.
        self.fill_type = self.get_fill_type(fill_type)

        # The method that we gonna run the schedule.
        self.schedule_function = self.get_scheduling_method(name)

        self.is_scheduling_done = False

    def get_slowest_machine(self):
        if self.is_scheduling_done is True:
            return max(self.machines, key=lambda m: m.schedule_len)
        else:
            raise Exception("You should run the scheduling method first.")

    def info(self):
        print(f"\t{Back.MAGENTA}METHOD USED: {Fore.LIGHTYELLOW_EX}{self.name}{Fore.RESET}{Back.RESET}")
        if self.name.startswith("holes"):
            for machine in self.machines:
                print(machine.holes_filled)
            print(f"Time saved = {Fore.GREEN}{sum([m.holes_saved_time for m in self.machines])}{Fore.RESET}")

        slowest_machine = self.get_slowest_machine()
        print(f'\n{slowest_machine.str_col_id()}\n{slowest_machine.str_col_schedule_len()}\n')

    def run(self):
        if self.schedule_function.__name__.startswith("holes"):
            self.schedule_function(self.workflows, self.machines, self.time_types, self.fill_type)
        else:
            self.schedule_function(self.workflows, self.machines)
        self.is_scheduling_done = True

    def method_used_info(self):
        if self.name.startswith("holes"):
            # return f"{''.join([Schedule.get_time_type(t) + '-' for t in self.time_types])} {self.fill_type}"
            ttypes = [Schedule.get_time_type(t) for t in self.time_types]
            return f"{ttypes[0]}-{ttypes[1]} {self.get_fill_type(self.fill_type)}"
        else:
            return f"{self.name}"

    @staticmethod
    def get_scheduling_method(name):
        if name.startswith("holes"):
            return holes_scheduling
        elif name == "c1":
            return c1.multiple_workflows_c1
        elif name == "c2":
            return c2.multiple_workflows_c2
        elif name == "c3":
            return c3.multiple_workflows_c3
        elif name == "c4":
            return c4.multiple_workflows_c4
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