from colorama import Fore
from typing import List, Union

DEBUG = True
ROUND_DIGIT = 2


class TaskStatus:
    FAILED = -1
    UNSCHEDULED = 0
    READY = 1
    SCHEDULED = 2
    FINISHED = 3
    SUSPENDED = 4
    STOPPED = 5


# TODO:
# Should be using a dictionary maybe instead look it further.
# Swap when you can!
class Edge:
    def __init__(self, weight, node):
        self.weight = weight
        self.node = node

    def str_colored(self):
        return f'--- {self.weight} --> {self.node.str_col_id()}'

    def __str__(self):
        return f'--- {self.weight} --> {self.node.str_id()}'


class Task:
    def __init__(self, id_, wf_id, name, costs, runtime, files, children_names, parents_names) -> None:
        self.costs = costs
        self.id = id_
        self.name = name
        self.start = None
        self.end = None
        self.machine_id: int = -1
        self.up_rank = None
        self.level = None
        self.down_rank = None
        self.priority = None
        self.runtime = runtime
        self.files = files
        self.wf_id = wf_id
        self.wf_deadline: Union[int, None] = None
        self.status = TaskStatus.UNSCHEDULED
        self.children_names = children_names
        self.children_till_ready = 0
        self.parents_names = parents_names
        self.parents_till_ready = 0
        self.children_edges: List[Edge] = list()
        self.parents_edges: List[Edge] = list()

        # This should be updated by the slowest parent.
        # This isn't needed but it should make it a bit faster if used
        self.slowest_parent: dict = {'parent_task': None, 'communication_time': 0}

        self.is_exit = False
        self.is_entry = False

        # Empty lists evaluate to False
        if children_names is not None:
            self.children_till_ready = len(children_names)
            if len(children_names) == 0:
                self.is_exit = True

        # Empty lists evaluate to False
        if parents_names is not None:
            self.parents_till_ready = len(parents_names)
            if len(parents_names) == 0:
                self.is_entry = True

        if self.is_entry == self.is_exit is True:
            raise Exception(f"Node[ {self.id} ] is not connected in the dag!")

    def set_wf_deadline(self, deadline):
        self.wf_deadline = deadline

    @staticmethod
    def make_dummy_node(id_, wf_id, name):
        return Task(id_=id_,
                    wf_id=wf_id,
                    name=name,
                    costs=list(),
                    runtime=0,
                    files=None,
                    children_names=None,
                    parents_names=None)

    def reset(self):
        self.start = None
        self.end = None
        self.machine_id = -1

    def set_priority(self, priority_value):
        self.priority = priority_value

    def str_colored(self):
        format_str = ''
        times = f"{self.str_col_times()}" \
            if self.start is not None and self.end is not None else ''
        up_rank = f'up-rank: {Fore.YELLOW}{round(self.up_rank, ROUND_DIGIT)}{Fore.RESET}' \
            if self.up_rank is not None else ''
        down_rank = f'down_rank: {Fore.YELLOW}{round(self.down_rank, ROUND_DIGIT)}{Fore.RESET} ' \
            if self.down_rank is not None else ''

        format_str += f'{Fore.CYAN}{self.name}{Fore.RESET} ' if self.name.startswith("Dummy") \
            else f'{self.str_col_id()} '
        # format_str += f'cost: {Fore.RED}{[round(cost, ROUND_DIGIT) for cost in self.costs]}{Fore.RESET} '

        format_str += self.str_col_wf_id()
        format_str += f'{times} {up_rank} {down_rank} '
        format_str += f'M[{self.machine_id}]' if self.machine_id != -1 else ''
        return format_str

    def __str__(self):
        format_str = ''
        times = f" times --> {self.str_times()}" \
            if self.start is not None and self.end is not None else ''
        up_rank = f'up-rank: {round(self.up_rank, ROUND_DIGIT)}' \
            if self.up_rank is not None else ''
        down_rank = f'down_rank: {round(self.down_rank, ROUND_DIGIT)} ' \
            if self.down_rank is not None else ''

        format_str += f'{self.name} ' if self.name.startswith("Dummy") else f'{self.str_id()} '
        # format_str += f'cost: {Fore.RED}{[round(cost, ROUND_DIGIT) for cost in self.costs]}{Fore.RESET} '

        format_str += self.str_wf_id()
        format_str += f'{times} {up_rank} {down_rank} '
        format_str += f'M[{self.machine_id}]' if self.machine_id != -1 else ''
        return format_str

    def str_col_wf_id(self):
        return f'WF[{Fore.GREEN}{self.wf_id}{Fore.RESET}] '

    def str_wf_id(self):
        return f'WF[{self.wf_id}] '

    def get_key(self):
        return tuple([self.id, self.wf_id])

    def __key(self):
        return tuple([self.id, self.wf_id])

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Task):
            return self.id < other.id
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Task):
            return self.id > other.id
        else:
            return NotImplemented

    def avg_com_cost(self):
        size = 1 if len(self.children_edges) == 0 else len(self.children_edges)
        return sum([child.weight for child in self.children_edges]) / size

    def avg_cost(self):
        # len(self.costs) cannot be 0 or it least it shouldn't
        return sum(self.costs) / len(self.costs)

    @staticmethod
    def find_task_by_name(tasks, name):
        for task in tasks:
            if task.name == name:
                return task
        return None

    def str_col_times(self):
        return f"{Fore.MAGENTA}[{round(self.start, ROUND_DIGIT)} - {round(self.end, ROUND_DIGIT)}]{Fore.RESET}"

    def str_times(self):
        return f"[{round(self.start, ROUND_DIGIT)} - {round(self.end, ROUND_DIGIT)}]"

    # TODO You can write this better (list comp).
    def get_tasks_from_names(self, tasks, is_child_tasks: bool):
        adj_tasks = list()
        names = self.children_names if is_child_tasks else self.parents_names
        for name in names:
            tmp = Task.find_task_by_name(tasks, name)
            if tmp is None:
                raise ValueError(f"Can't find task name in given tasks: {name}")
            else:
                adj_tasks.append(tmp)
        return adj_tasks

    def str_col_id(self):
        return f"{Fore.MAGENTA}T[{Fore.RESET}{Fore.GREEN}{self.id}{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}"

    def str_id(self):
        return f'T[{self.id}]'

    def set_edges(self, children_edges, parents_edges):
        # TODO Check if everything went fine in parsing.
        self.children_edges = children_edges
        self.parents_edges = parents_edges

    def is_slowest_parent(self, child):
        if child.slowest_parent['parent_task'] is None or \
                child.slowest_parent['parent_task'].end < self.end:
            return True
        return False

    # This function runs once the task gets scheduled
    def update_children_and_self_status(self):
        if self.status == TaskStatus.SCHEDULED:
            raise Exception(
                f"\nError this task is already scheduled it should not run this function again!\n\tTASK: {self}\n")
        else:
            self.status = TaskStatus.SCHEDULED

        for child_edge in self.children_edges:
            if self.is_slowest_parent(child_edge.node):
                # Update the child parent only if you are the slowest parent atm.
                child_edge.node.slowest_parent = {
                    'parent_task': self, 'communication_time': child_edge.weight}

            # Update the child's counter for parents once that value
            # goes to 0 the child can start the schedule machine itself
            # be careful the same parents should run this function once!
            if child_edge.node.parents_till_ready <= 0:
                raise Exception(f"\nThe child: {child_edge.node} is already ready! "
                                f"Task that tried to update it: {self}\n")
            else:
                child_edge.node.parents_till_ready -= 1
                if child_edge.node.parents_till_ready == 0:
                    child_edge.node.status = TaskStatus.READY

    def print_children(self):
        tmp_str = self.str_id()
        for child in self.children_edges:
            tmp_str += f' --> weight: {child.weight}  child: {child.node}  '
        return tmp_str

    def is_file_in_task(self, search_file):
        for file in self.files:
            if file['name'] == search_file['name']:
                return True
        return False

    def add_parent(self, cost, task):
        # if self.name.startswith('Dummy'):
        #     self.is_entry_node = False
        self.parents_edges.append(Edge(cost, task))
        self.parents_till_ready += 1

    def add_child(self, cost, task):
        # self.is_exit_node = False
        self.children_edges.append(Edge(cost, task))
        self.children_till_ready += 1
