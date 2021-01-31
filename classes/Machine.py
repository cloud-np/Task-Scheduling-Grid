from colorama import Fore, Back, Style
from algos.schedule_wfs_and_tasks import schedule_task
from algos.calc_ex_time import compute_execution_time
from classes.Task import Task
from random import randint
from typing import Set, List

NETWORK_KBPS = 20000
CORE_SPEED = 1200
MIN_GAP_SIZE = 300
DEBUG = True
# 3, 200, 2000


class Hole:
    def __init__(self, gap, start, end):
        self.gap = gap
        self.start = start
        self.end = end

    def __key(self):
        return tuple((self.gap, (self.start, self.end)))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Hole):
            return self.__key() == other.__key()
        else:
            return NotImplemented


class Machine:

    def __init__(self, id_, name, n_cpu=None, speed=None, memory=None, cpti=None):
        self.schedule_len = 0
        self.id: int = id_
        self.name: str = name
        self.n_cpu: int = n_cpu
        self.memory = memory
        self.cpti = cpti  # cost per time interval
        self.speed = speed
        self.holes: Set = set()
        # self.network_speed = network_speed
        self.tasks: Set = set()

    def add_task(self, task):
        if DEBUG and (task in self.tasks):
            raise Exception(f"The task is already added. In machine {self.id}\n {task}")
        self.tasks.add(task)
        if self.schedule_len <= task.end:
            self.schedule_len = task.end

    def add_task_to_hole(self, task, hole):
        before_start_gap = task.start - hole.start
        after_end_gap = hole.end - task.end

        if before_start_gap >= MIN_GAP_SIZE:
            self.holes.add(Hole(start=hole.start, end=task.start, gap=before_start_gap))
        elif after_end_gap >= MIN_GAP_SIZE:
            self.holes.add(Hole(start=task.end, end=hole.end, gap=after_end_gap))

        self.remove_hole(hole)

    def remove_hole(self, hole):
        self.holes.remove(hole)

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

    def str_id(self):
        return f'{Fore.YELLOW}Machine{Fore.RESET} [{Fore.GREEN}{self.id}{Fore.RESET}]'

    def __str__(self):
        tmp_str = f'{self.str_id()}\n'
        for task in self.tasks:
            if task.name.startswith("Dummy"):
                tmp_str += f'{Fore.CYAN}{task.name}{Fore.RESET} {task.str_wf_id()}'
            else:
                tmp_str += f'{task.str_id()} {task.str_wf_id()}'
            tmp_str += f"{task.str_times()}\n"
        tmp_str += self.str_schedule_len()
        return tmp_str

    def str_schedule_len(self):
        return f'{Fore.BLUE}TOTAL LEN:{Fore.RESET} {self.schedule_len}'

    # def print_info(self):
    #     for task in self.tasks:
    #         print(f"{task.str_id()} {task.str_times()} ")

    # def convert_tasks_to_str(self):
    #     tmp_str = f'{self.tasks[0]}'
    #     for i in range(1, len(self.tasks)):
    #         tmp_str += '-' + str(self.tasks[i].id)
    #     return tmp_str

    def clear(self):
        self.tasks = list()
        self.schedule_len = 0

    def update_schedule(self, task):
        self.schedule_len = task.end if self.schedule_len <= task.end else self.schedule_len

    def remove_task(self, task):
        # Check if that task is the last on the schedule
        if self.schedule_len == task.end:
            if task.slowest_parent['parent_task'].machine_id.id == task.machine_id.id:
                communication_time = 0
            else:
                communication_time = task.slowest_parent['communication_time']
            self.schedule_len = task.start - communication_time
            print(f"{task} changed was the last task in the list")
            self.tasks.remove(task)

    def machine_details(self):
        return f'ID[{Fore.GREEN}{self.id}{Fore.RESET}] ' \
               f'{Fore.RED}n_cpu:{Fore.RESET} {Fore.YELLOW}{self.n_cpu}{Fore.RESET} ' \
               f'{Fore.RED}speed:{Fore.RESET} {Fore.YELLOW}{self.speed}{Fore.RESET} '

    @staticmethod
    def generate_rand_machines(n_machines):
        machines = list()
        for i in range(n_machines):
            machines.append(
                Machine(
                    id_=i,
                    name=f'M-{i}',
                    n_cpu=randint(1, 4),
                    speed=CORE_SPEED - randint(100, 400),
                )
            )
        return machines

    @staticmethod
    def get_4_machines():
        machines = [
            Machine(id_=0, name="M-0", n_cpu=2, speed=CORE_SPEED - 200),
            Machine(id_=1, name="M-1", n_cpu=1, speed=CORE_SPEED - 100),
            Machine(id_=2, name="M-2", n_cpu=4, speed=CORE_SPEED - 300),
            Machine(id_=3, name="M-3", n_cpu=2, speed=CORE_SPEED - 400)
        ]
        return machines

    # We add here a random const (1500) just so we can subtract
    # without getting a negative value. Since this const is adding
    # for every task it doesn't change our wanted outcome.
    # We can't use the ceil or floor function here because the numbers
    # are quite small and we will be missing that information.
    def __generate_cost_for_task(self, runtime):
        return runtime + 1500 - self.speed / self.n_cpu

    @staticmethod
    def assign_tasks_with_costs(machines, tasks):
        for machine in machines:
            for task in tasks:
                if task.name.startswith("Dummy"):
                    task.costs.append(0)
                else:
                    cost = machine.__generate_cost_for_task(task.runtime)
                    task.costs.append(cost)

    # Atm it just returns the cost back. Maybe we may add something depending the problem.
    def calc_com_cost(self, cost):
        return cost
