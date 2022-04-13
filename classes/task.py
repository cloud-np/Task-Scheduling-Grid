from colorama import Fore
from random import randint
from typing import List, Optional
from dataclasses import dataclass

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
        return f'--- {round(self.weight, 3)} --> {self.node.str_id()}'


@dataclass
class TaskBlueprint:
    id_: int
    wf_id: int
    name: str
    runtime: float
    level: int
    children_names: Optional[dict]
    parents_names: Optional[dict]
    status: TaskStatus
    is_entry: bool
    is_exit: bool


class Task:
    def __init__(self, id_, wf_id, name, costs, runtime, children_names=None, parents_names=None, files=None, status=TaskStatus.UNSCHEDULED, level=None) -> None:
        self.costs = costs
        self.id = id_
        self.name = name
        self.runtime = runtime
        self.files = files
        self.wf_id = wf_id
        self.status: TaskStatus = status
        self.children_names = children_names
        self.parents_names = parents_names
        self.start = None
        self.end = None
        self.machine_id: int = -1
        self.up_rank = None
        self.level = level
        self.down_rank = None
        self.priority = None
        self.wf_deadline: Optional[int] = None
        self.children_till_ready: int = 0
        self.parents_till_ready: int = 0
        self.is_critical: bool = False
        self.added_to_hole: bool = False
        self.children_edges: List[Edge] = []
        self.parents_edges: List[Edge] = []

        # This should be updated by the slowest parent.
        # This isn't needed but it should make it a bit faster if used
        self.slowest_parent: dict = {'parent_task': None, 'communication_time': 0}

        self.is_exit: bool = False
        self.is_entry: bool = False

    def get_blueprint(self):
        return TaskBlueprint(self.id, self.wf_id, self.name, self.runtime, self.level, [{"w": e.weight, "n": e.node.name} for e in self.children_edges], [{"w": e.weight, "n": e.node.name} for e in self.parents_edges], self.status, self.is_entry, self.is_exit)

    def has_child(self, child_task):
        return any(e.node is child_task for e in self.children_edges)

    def create_edges(self, tasks: List['Task'], network_kbps: Optional[float] = None):
        if network_kbps is not None:
            children: List[Task] = self.get_tasks_from_names(tasks, is_child_tasks=True)
            parents: List[Task] = self.get_tasks_from_names(tasks, is_child_tasks=False)
            # We need at least -> len(Edges) == len(children)
            children_edges: List[Edge] = [Edge(weight=0, node=child) for child in children]
            parents_edges: List[Edge] = [Edge(weight=0, node=parent) for parent in parents]

            for file in self.files:
                if file['link'] == 'output':
                    for i, child in enumerate(children):
                        if child.is_file_in_task(file):
                            children_edges[i].weight += file['size']
                elif file['link'] == 'input':
                    for i, parent in enumerate(parents):
                        if parent.is_file_in_task(file):
                            parents_edges[i].weight += file['size']

            for child_edge in children_edges:
                child_edge.weight /= network_kbps
            for parent_edge in parents_edges:
                parent_edge.weight /= network_kbps
            # We use this function to check if everything went smoothly in the parsing
            self.set_edges(children_edges, parents_edges)
        else:
            self.set_edges([Edge(e['w'], Task.find_task_by_name(tasks, e['n'])) for e in self.children_names],
                           [Edge(e['w'], Task.find_task_by_name(tasks, e['n'])) for e in self.parents_names])

    @staticmethod
    def blueprint_to_task(blp: TaskBlueprint):
        return Task(
            id_=blp.id_,
            wf_id=blp.wf_id,
            name=blp.name,
            costs=[],
            runtime=blp.runtime,
            status=blp.status,
            level=blp.level,
            files=None,
            children_names=blp.children_names,
            parents_names=blp.parents_names)

    @staticmethod
    def make_dummy_node(id_, wf_id, name):
        return Task(id_=id_,
                    wf_id=wf_id,
                    name=name,
                    costs=[],
                    runtime=0,
                    files=None,
                    children_names=None,
                    parents_names=None)

    def calc_lstf(self, time):
        if self.wf_deadline is None:
            raise Exception("Wf deadline is None!")
        return self.wf_deadline - time - self.up_rank

    def set_times(self, start, end):
        self.start = start
        self.end = end

    def set_priority(self, priority_value):
        self.priority = priority_value

    def str_colored(self):
        format_str = ''
        times = f"{self.str_col_times()}" \
            if self.start is not None and self.end is not None else ''
        # up_rank = f'up-rank: {Fore.YELLOW}{round(self.up_rank, ROUND_DIGIT)}{Fore.RESET}' \
        #     if self.up_rank is not None else ''
        # down_rank = f'level: {Fore.YELLOW}{round(self.down_rank, ROUND_DIGIT)}{Fore.RESET} ' \
        #     if self.down_rank is not None else ''
        runtime = f'runtime: {Fore.YELLOW}{round(self.runtime, ROUND_DIGIT)}{Fore.RESET} ' \
            if self.down_rank is not None else ''

        format_str += f'{Fore.CYAN}{self.name}{Fore.RESET} ' if self.name.startswith("Dummy") \
            else f'{self.str_col_id()} '
        # format_str += f'cost: {Fore.RED}{[round(cost, ROUND_DIGIT) for cost in self.costs]}{Fore.RESET} '

        format_str += self.str_col_wf_id()
        format_str += f'{times} {runtime} '
        format_str += f'M[{self.machine_id}]' if self.machine_id != -1 else ''
        return format_str

    def __str__(self):
        format_str = ''
        times = f"--> {self.str_times()}" \
            if self.start is not None and self.end is not None else ''
        # up_rank = f'up-rank: {round(self.up_rank, ROUND_DIGIT)}' \
        #     if self.up_rank is not None else ''
        # down_rank = f'down_rank: {round(self.down_rank, ROUND_DIGIT)} ' \
        #     if self.down_rank is not None else ''
        runtime = f'cost: {Fore.YELLOW}{round(self.runtime, ROUND_DIGIT)}{Fore.RESET} ' \
            if self.down_rank is not None else ''

        format_str += f'{Fore.CYAN}{self.name}{Fore.RESET} ' if self.name.startswith("Dummy") \
            else f'{self.str_col_id()} '

        # format_str += self.str_col_wf_id()
        format_str += f'{times} {runtime} '
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
        return self.id < other.id if isinstance(other, Task) else NotImplemented

    def __gt__(self, other):
        return self.id > other.id if isinstance(other, Task) else NotImplemented

    def avg_com_cost(self):
        size = 1 if len(self.children_edges) == 0 else len(self.children_edges)
        return sum(child.weight for child in self.children_edges) / size

    def avg_cost(self):
        # len(self.costs) cannot be 0 or at least it shouldn't
        return sum(self.costs) / len(self.costs)

    @staticmethod
    def find_task_by_name(tasks, name) -> Optional['Task']:
        return next((task for task in tasks if task.name == name), None)

    def str_col_times(self):
        return f"{Fore.MAGENTA}[{round(self.start, ROUND_DIGIT)} - {round(self.end, ROUND_DIGIT)}]{Fore.RESET}"

    def str_times(self):
        return f"[{round(self.start, ROUND_DIGIT)} - {round(self.end, ROUND_DIGIT)}]"

    # TODO You can write this better (list comp).
    def get_tasks_from_names(self, tasks, is_child_tasks: bool) -> List['Task']:
        adj_tasks: List['Task'] = []
        names = self.children_names if is_child_tasks else self.parents_names
        for name in names:
            tmp = Task.find_task_by_name(tasks, name)
            if tmp is None:
                raise ValueError(
                    f"Can't find task name in given tasks: {name}")
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
        self.children_till_ready = len(self.children_edges)
        if len(self.children_edges) == 0:
            self.is_exit = True

        self.parents_edges = parents_edges
        self.parents_till_ready = len(self.parents_edges)
        if len(self.parents_edges) == 0:
            self.is_entry = True

    def is_slowest_parent(self, child):
        return child.slowest_parent['parent_task'] is None or child.slowest_parent['parent_task'].end < self.end

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

            if child_edge.node.parents_till_ready <= 0:
                raise Exception(f"\nThe child: {child_edge.node} is already ready! "
                                f"Task that tried to update it: {self}\n")
            child_edge.node.parents_till_ready -= 1
            if child_edge.node.parents_till_ready == 0:
                child_edge.node.status = TaskStatus.READY

    @staticmethod
    def create_random_task(id_, wf_id):
        return Task(id_=id_, wf_id=wf_id, name=f"task-{id_}", costs=[], runtime=randint(2, 15), files=None, children_names=None, parents_names=None)

    def print_children(self):
        tmp_str = self.str_id()
        for child in self.children_edges:
            tmp_str += f' --> weight: {child.weight}  child: {child.node}  '
        return tmp_str

    def is_file_in_task(self, search_file):
        return any(file['name'] == search_file['name'] for file in self.files)

    def add_parent(self, cost, task):
        # if self.name.startswith('Dummy'):
        #     self.is_entry_node = False
        self.parents_edges.append(Edge(cost, task))
        self.parents_till_ready += 1

    def add_child(self, cost, task):
        # self.is_exit_node = False
        self.children_edges.append(Edge(cost, task))
        self.children_till_ready += 1
