from colorama import Fore
from random import randint
from classes.task import Task
import heapq
from typing import Set, List
from dataclasses import dataclass


# NETWORK_KBPS = 1
HAS_NETWORK = True
CORE_SPEED = 1200
MIN_GAP_SIZE = 0.1
DEBUG = True


class Hole:
    def __init__(self, start, end, gap):
        self.gap = gap
        self.start = start
        self.end = end
        self.time_saved = 0

    def __key(self):
        return tuple((self.gap, (self.start, self.end)))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Hole):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __str__(self):
        return f"gap: {round(self.gap, 3)} ({round(self.start, 2)} - {round(self.end, 2)})"

    def is_fillable(self, end):
        # Check if the parent end interfere with the child start
        return end <= self.end


@dataclass
class MachineBlueprint:
    id_: int
    name: str
    n_cpu: int
    speed: float
    network_kbps: float


class Machine:

    def __init__(self, id_, name, n_cpu, network_kbps, speed=None, memory=None, cpti=None):
        self.time_on_machine = 0
        self.id: int = id_
        self.network_kbps = network_kbps
        self.name: str = name
        self.n_cpu: int = n_cpu
        # self.memory = memory
        # self.cpti = cpti  # cost per time interval
        self.speed = speed
        self.holes: Set[Hole] = set()
        self.holes_saved_time = 0
        self.holes_filled = 0
        self.tasks: List[Task] = []

    def get_blueprint(self):
        return MachineBlueprint(self.id, self.name, self.n_cpu, self.speed, self.network_kbps)

    def contains_wf_id(self, wf_id):
        return any(t.wf_id == wf_id for t in self.tasks)

    @staticmethod
    def blueprint_to_machine(blp: MachineBlueprint):
        return Machine(id_=blp.id_, name=blp.name, n_cpu=blp.n_cpu, speed=blp.speed, network_kbps=blp.network_kbps)

    def find_holes(self):
        old_end = 0
        for t in sorted(self.tasks, key=lambda t: t.start):
            gap = t.start - old_end
            if gap >= MIN_GAP_SIZE:
                self.holes.add(Hole(start=old_end, end=t.start, gap=gap))
            old_end = t.end

    def add_task_to_hole(self, task, hole):
        self.add_task(task)
        self.holes_filled += 1
        self.holes_saved_time += task.end - task.start
        self.remove_hole(hole)

    def add_task(self, task):
        self.find_holes()
        if self.time_on_machine <= task.end:
            self.time_on_machine = task.end
        self.tasks.append(task)

    def get_busy_time(self):
        return sum(t.end - t.start for t in self.tasks)

    def get_idle_time(self):
        # t.start can't be None since the task is "inside" the
        # machine it means it also received a start time
        sorted_tasks = sorted(self.tasks, key=lambda t: t.start)
        idle_time = 0
        old_end = sorted_tasks[0].end
        for t in sorted_tasks[1:]:
            idle_time += t.start - old_end
            old_end = t.end
        return idle_time

    def get_util_perc(self, schedule_len):
        # return (self.get_util_time(schedule_len) / schedule_len) * 100
        return (self.get_busy_time() / schedule_len) * 100

    def get_idle_perc(self):
        return (self.get_idle_time() / self.time_on_machine) * 100

    @staticmethod
    def get_potential_hole_time_saved(task, hole):
        return hole.gap - (task.start - hole.start + hole.end - task.end)

    def remove_hole(self, hole):
        self.holes_filled += 1
        self.holes.remove(hole)

    @staticmethod
    def create_random_machine(id_):
        return Machine(id_=id_, name=f"M-{id_}", n_cpu=randint(1, 4), speed=CORE_SPEED)

    # If this returns false it means that the task is trying to finish or start after the gap e.g:
    # task_times = (12, 25)  gap = (10, 22)
    # def try_feeling_hole(self, task, cost, hole):
    #     # Check when if the parent end interfere with the child start
    #     # pred: predicted
    #     [pred_start, pred_end] = compute_execution_time(task, self)
    #     # TODO: Remove the first check since this gets generated from the machine itself
    #     #       there should be no way a task can try to start earlier.
    #     if (hole["times"][0] <= pred_start) and ((pred_start + cost) <= pred_end):
    #         schedule_task({'start': pred_start, 'end': pred_start + cost},
    #                       task, self)
    #         self.holes.remove(hole)
    #         return True
    #     else:
    #         raise Exception(f"{task.str_times()} {hole} {self}")
    #         return False

    def str_col_id(self):
        return f'{Fore.YELLOW}Machine{Fore.RESET} [{Fore.GREEN}{self.id}{Fore.RESET}]'

    def str_id(self):
        return f'Machine [{self.id}]'

    def str_colored(self):
        tmp_str = f'{self.str_col_id()}\n'
        for task in self.tasks:
            if task.name.startswith("Dummy"):
                tmp_str += f'{Fore.CYAN}{task.name}{Fore.RESET} {task.str_col_wf_id()}'
            else:
                tmp_str += f'{task.str_col_id()} {task.str_col_wf_id()}'
            tmp_str += f"{task.str_col_times()}\n"
        tmp_str += self.str_col_schedule_len()
        return tmp_str

    def __str__(self):
        tmp_str = f'{self.str_id()}\n'
        for task in sorted(self.tasks, key=lambda t: t.start):
            if task.name.startswith("Dummy"):
                tmp_str += f'{task.name} {task.str_wf_id()}'
            else:
                tmp_str += f'{task.str_id()} {task.str_wf_id()}'
            tmp_str += f"{task.str_times()}\n"
        tmp_str += self.str_schedule_len()
        return tmp_str

    def str_col_schedule_len(self):
        return f'{Fore.BLUE}TOTAL LEN:{Fore.RESET} {self.time_on_machine}'

    def str_schedule_len(self):
        return f'TOTAL LEN: {self.time_on_machine}'

    # def print_info(self):
    #     for task in self.tasks:
    #         print(f"{task.str_id()} {task.str_times()} ")

    # def convert_tasks_to_str(self):
    #     tmp_str = f'{self.tasks[0]}'
    #     for i in range(1, len(self.tasks)):
    #         tmp_str += '-' + str(self.tasks[i].id)
    #     return tmp_str

    def clear(self):
        self.tasks = set()
        self.time_on_machine = 0

    def update_schedule(self, task):
        self.time_on_machine = task.end if self.time_on_machine <= task.end else self.time_on_machine

    def remove_task(self, task):
        # Check if that task is the last on the schedule
        if self.time_on_machine == task.end:
            if task.slowest_parent['parent_task'].machine_id.id == task.machine_id.id:
                communication_time = 0
            else:
                communication_time = task.slowest_parent['communication_time']
            self.time_on_machine = task.start - communication_time
            # print(f"{task} changed was the last task in the list")
            self.tasks.remove(task)

    def machine_details(self):
        return f'ID[{Fore.GREEN}{self.id}{Fore.RESET}] ' \
               f'{Fore.RED}n_cpu:{Fore.RESET} {Fore.YELLOW}{self.n_cpu}{Fore.RESET} ' \
            #    f'{Fore.RED}speed:{Fore.RESET} {Fore.YELLOW}{self.speed}{Fore.RESET} '

    @staticmethod
    def generate_rand_machines(n_machines):
        return [Machine(
                    id_=i,
                    name=f'M-{i}',
                    n_cpu=randint(1, 4),
                    speed=CORE_SPEED - randint(100, 400),
                ) for i in range(n_machines)]

    @staticmethod
    def load_n_static_machines(n: int, network):
        cpus = [2, 1, 4, 2,  # 4
        # cpus = [4, 4, 4, 4,  # 4
                1, 4, 2, 3,  # 8
                2, 1, 4, 2,
                3, 4, 2, 3,  # 16
                1, 1, 3, 4,
                3, 4, 3, 4,
                2, 2, 4, 2,
                1, 4, 4, 1,  # 32
                2, 1, 4, 2,
                1, 4, 2, 3,
                2, 1, 4, 2,
                3, 4, 2, 3,
                1, 1, 3, 4,
                3, 4, 3, 4,
                2, 2, 4, 2,
                1, 4, 4, 1,  # 64
                ]
        return [Machine(id_=i, name=f"M-{i}", n_cpu=cpus[i], speed=CORE_SPEED - 100, network_kbps=network) for i in range(n)]

    # We add here a random const (1500) just so we can subtract
    # without getting a negative value. Since this const is adding
    # for every task it doesn't change our wanted outcome.
    # We can't use the ceil or floor function here because the numbers
    # are quite small and we will be missing that information.
    # ORR we can simply remove the speed and ignore
    def __generate_cost_for_task(self, runtime):
        return runtime / self.n_cpu

    def assign_tasks_with_costs(self, tasks):
        for task in tasks:
            if task.name.startswith("Dummy"):
                task.costs.append(0)
            else:
                cost = self.__generate_cost_for_task(task.runtime)
                task.costs.append(cost)

    # Atm it just returns the cost back. Maybe we may add something depending the problem.
    def calc_com_cost(self, cost):
        return cost
