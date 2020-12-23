from colorama import Fore, Back, Style
from random import randint
from math import floor, ceil

NETWORK_KBPS = 12000
CORE_SPEED = 1200


class Machine:

    def __init__(self, id_, name, n_cpu=None, speed=None, network_speed=None):
        self.schedule_len = 0
        self.id = id_
        self.name = name
        self.n_cpu = n_cpu
        self.speed = speed
        self.network_speed = network_speed
        self.tasks = list()

    def add_task(self, task):
        self.tasks.append(task)
        self.schedule_len = task.end

    def __str__(self):
        tmp_str = f'Machine [{Fore.GREEN}{self.id}{Fore.RESET}]\n'
        for task in self.tasks:
            if task.id == -1:
                continue
            tmp_str += f'T[{Fore.GREEN}{task.id}{Fore.RESET}] ' \
                       f'{task.start_str()} ' \
                       f'{task.end_str()}\n'

        tmp_str += f'TOTAL LEN: {self.schedule_len}'
        return tmp_str

    def machine_details(self):
        return f'ID[{Fore.GREEN}{self.id}{Fore.RESET}] ' \
               f'{Fore.RED}n_cpu:{Fore.RESET} {Fore.YELLOW}{self.n_cpu}{Fore.RESET} ' \
               f'{Fore.RED}speed:{Fore.RESET} {Fore.YELLOW}{self.speed}{Fore.RESET} ' \
               f'{Fore.RED}network_speed:{Fore.RESET} {Fore.YELLOW}{self.network_speed}{Fore.RESET}'

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
                    network_speed=NETWORK_KBPS - randint(0, 3500)
                )
            )
        return machines

    @staticmethod
    def get_4_machines():
        machines = [
            Machine(id_=0, name="M-0", n_cpu=2, speed=CORE_SPEED - 200, network_speed=NETWORK_KBPS),
            Machine(id_=1, name="M-1", n_cpu=1, speed=CORE_SPEED - 100, network_speed=NETWORK_KBPS),
            Machine(id_=2, name="M-2", n_cpu=4, speed=CORE_SPEED - 300, network_speed=NETWORK_KBPS),
            Machine(id_=3, name="M-3", n_cpu=2, speed=CORE_SPEED - 400, network_speed=NETWORK_KBPS)
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
                cost = machine.__generate_cost_for_task(task.runtime)
                task.costs.append(cost)

    def calc_communication_cost(self, cost):
        return cost / self.network_speed
