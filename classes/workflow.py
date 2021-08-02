from classes.task import Task, TaskStatus, Edge
from algos.calc_task_ranks import calculate_downward_ranks, calculate_upward_ranks
import algos.schedule_wfs as algos
from colorama import Fore, Back
from typing import Union, Any
from helpers.data_parser import get_tasks_from_json_file
from example_data import NAMES_A, NAMES_B, COSTS_A, COSTS_B, \
    TASK_DAG_A, TASK_DAG_B, PARENTS_DAG_A, PARENTS_DAG_B
from helpers.checker import schedule_checker
from random import choice

WF_TYPES = ['cycles', 'epigenomics', 'genome',
            'montage', 'seismology', 'soykbr']
NUM_TASKS = [10, 14, 20, 30, 50, 100, 133, 200, 300, 400, 500, 1000]
CACHED_WFS = dict()


# Each Workflow has each very own Tasks and Machines
# objects. This is crucial because the are not referencing
# the same objects in memory. In the case of genetic tho
# you we should either use another class or use this one
# with caution when we create the "child-workflows"
# in any CASE tho tasks and machines lists should NEVER change
# at all. I should try to make them immutable later on.
class Workflow:
    def __init__(self, id_, wf_type, machines, add_dummies, file_path, name=None, tasks: Union[list, None] = None):
        self.id = id_
        self.type = wf_type  # type of the workflow e.g: LIGO, Montage, etc
        self.name = name
        self.tasks: Any = tasks
        self.scheduled = False
        self.avg_comp_cost: float = -1.0
        self.avg_com_cost: float = -1.0
        self.ccr: float = -1.0

        if tasks is None:
            # 1. Parse the workflow tasks
            self.tasks = get_tasks_from_json_file(file_path, id_)

            # 2. add dummy nodes
            if add_dummies:
                self.__add_dummy_nodes()

            # 3. Calculate the runtime cost for every machine
            for m in machines:
                m.assign_tasks_with_costs(tasks=self.tasks)

        # 4. Generate critical path, up_rank and down_rank
        self.cp_info = {"critical_path": set(), "entry": None, "exit": None}
        self.create_critical_path()

        # Calc ccr which means also the avg_comp and avg_com costs
        self.ccr = self.calc_ccr()

        # From the avg comp cost of the tasks add them all together * some number and get the deadline
        self.deadline = self.avg_comp_cost * 10

        # Assign to all the tasks the wf_deadline
        for t in self.tasks:
            t.set_wf_deadline(self.deadline)

    def str_colored(self):
        return f"{self.str_col_id()}\n" \
               f"{Fore.BLUE}Type:{Fore.RESET} {self.type} \n" \
               f"{Fore.MAGENTA}Num-tasks:{Fore.RESET} {len(self.tasks)}\n" \
            # f"{Fore.RED}Len:{Fore.RESET} {self.get_workflow_len()}" \

    def __str__(self):
        return f"{self.str_col_id()}\n" \
               f"Type: {self.type} \n" \
               f"Num-tasks: {len(self.tasks)}\n" \
               # f"Len: {self.get_workflow_len()}" \

    # FIXME
    # DO NOT CHANGE THE NAMING
    def __add_dummy_nodes(self):
        self.tasks.insert(0, Task.make_dummy_node(0, self.id, "Dummy-In"))
        self.tasks.append(Task.make_dummy_node(
            len(self.tasks), self.id, "Dummy-Out"))

        dummy_in = self.tasks[0]
        dummy_out = self.tasks[len(self.tasks) - 1]
        for task in self.tasks:
            if task.is_entry:
                dummy_in.add_child(0, task)
                task.add_parent(0, dummy_in)
                task.is_entry = False
            if task.is_exit:
                dummy_out.add_parent(0, task)
                task.add_child(0, dummy_out)
                task.is_exit = False
        dummy_in.is_entry = True
        dummy_in.status = TaskStatus.READY
        dummy_out.is_exit = True

    # TODO: If we end up using the same workflow for multiple workflows we should preload tasks and machines
    #       and just deepcopy these. Even that should be faster. This is not something that will effect us a lot but ok
    '''
        Generates multiple workflows randomly based on number of tasks and the workflows you need.
        It doesn't actually create them although I could do that but I found it kinda pointless atm.
        So it picks from some random pre-made ones.
    '''
    @staticmethod
    def connect_wfs(workflows, machines):
        dummy_in = Task.make_dummy_node(id_=-1, wf_id=-1, name="Dummy-In-BIG")
        # To find the dummy_out.id we need to calc all the tasks in all workflows
        dummy_out = Task.make_dummy_node(
            id_=sum([len(wf.tasks) for wf in workflows]), wf_id=-1, name="Dummy-Out-BIG")
        all_tasks = [dummy_in]
        dummy_in.costs = [0 for _ in machines]

        for wf in workflows:
            for task in wf.tasks:
                if task.is_entry:
                    dummy_in.add_child(0, task)
                    task.add_parent(0, dummy_in)
                    task.is_entry = False
                    task.status = TaskStatus.UNSCHEDULED
                if task.is_exit:
                    dummy_out.add_parent(0, task)
                    task.add_child(0, dummy_out)
                    task.is_exit = False
                all_tasks.append(task)

        dummy_in.is_entry = True

        all_tasks.append(dummy_out)
        dummy_out.costs = [0 for _ in machines]
        dummy_in.status = TaskStatus.READY
        dummy_out.is_exit = True
        return all_tasks

    def create_critical_path(self):
        # Calculate downward and upward ranks
        calculate_upward_ranks(self.tasks)
        calculate_downward_ranks(self.tasks)

        for task in self.tasks:
            if task.down_rank is None:
                print(task)
            task.set_priority(task.down_rank + task.up_rank)

        critical_path, [entry_task,
                        exit_task] = algos.construct_critical_path(self.tasks)
        self.cp_info = {"critical_path": critical_path,
                        "entry": entry_task, "exit": exit_task}
        return critical_path, [entry_task, exit_task]

    @staticmethod
    def load_paper_example_workflows(machines):
        names = [NAMES_A, NAMES_B]
        # ranks = [RANKS_A, RANKS_B]
        costs = [COSTS_A, COSTS_B]
        children_dags = [TASK_DAG_A, TASK_DAG_B]
        parents_dags = [PARENTS_DAG_A, PARENTS_DAG_B]
        tasks = [list(), list()]
        for wf_id in range(2):
            # We do +1 because we usally add an entry node with id = 0
            tasks[wf_id] = [Task(id_=i + 1,
                                 wf_id=wf_id,
                                 name=names[wf_id][i],
                                 costs=costs[wf_id][i],
                                 runtime=None,
                                 files=None,
                                 children_names=[c['name']
                                                 for c in children_dags[wf_id][i]],
                                 parents_names=[p['name'] for p in parents_dags[wf_id][i]]) for i in range(0, len(children_dags[wf_id]))]

            for task in tasks[wf_id]:
                children: list = task.get_tasks_from_names(
                    tasks[wf_id], is_child_tasks=True)
                parents: list = task.get_tasks_from_names(
                    tasks[wf_id], is_child_tasks=False)
                # We need at least -> len(Edges) == len(children)
                children_edges = [Edge(weight=children_dags[wf_id][task.id - 1]
                                       [i]["weight"], node=child) for i, child in enumerate(children)]
                parents_edges = [Edge(weight=parents_dags[wf_id][task.id - 1][i]
                                      ["weight"], node=parent) for i, parent in enumerate(parents)]
                # We use this function to check if everything went smoothly in the parsing
                task.set_edges(children_edges, parents_edges)

        a_tasks = tasks[0]
        b_tasks = tasks[1]
        A = Workflow(0, "example", machines, add_dummies=True,
                     file_path=None, name="A", tasks=a_tasks)
        B = Workflow(1, "example", machines, add_dummies=True,
                     file_path=None, name="B", tasks=b_tasks)

        return [A, B]

    @staticmethod
    def generate_multiple_workflows(n_wfs: int, machines, is_our_method: bool,
                                    user_set_tasks: int = 0, path: str = './datasets'):
        workflows = list()
        i = 0
        while len(workflows) < n_wfs:
            wf_type = choice(WF_TYPES)
            if user_set_tasks < 1:
                n_tasks = choice(NUM_TASKS)
            else:
                n_tasks = user_set_tasks

            # We can't have these type of workflows with less than that tasks.
            if not ((wf_type == 'montage' and n_tasks < 133) or (wf_type == 'soykbr' and n_tasks < 14)):
                i += 1
                workflows.append(Workflow(id_=i, file_path=f'{path}/{wf_type}/{wf_type}_{n_tasks}.json',
                                          wf_type=wf_type, machines=machines, add_dummies=is_our_method))
        return workflows

    @staticmethod
    def load_example_workflows(machines, n, path: str = './datasets'):
        num_tasks = [
            10, 50, 20, 500, 30, 100, 14, 50, 400, 200,
            500, 1000, 300, 500, 100, 50, 200, 300, 1000, 1000,
            10, 50, 20, 500, 30, 100, 14, 50, 400, 200,
            500, 1000, 300, 500, 100, 50, 200, 300, 1000, 1000,
            500, 1000, 300, 500, 100, 50, 200, 300, 1000, 1000,
            300, 50, 200
        ]
        wf_types = [
            'cycles', 'genome', 'seismology', 'cycles', 'soykbr', 'epigenomics',
            'genome', 'cycles', 'seismology', 'genome', 'cycles', 'genome', 'epigenomics',
            'cycles', 'genome', 'epigenomics', 'seismology', 'genome', 'soykbr', 'soykbr',
            'cycles', 'genome', 'seismology', 'cycles', 'soykbr', 'epigenomics',
            'genome', 'cycles', 'seismology', 'genome', 'cycles', 'genome', 'epigenomics',
            'cycles', 'genome', 'epigenomics', 'seismology', 'genome', 'soykbr', 'soykbr',
            'cycles', 'genome', 'epigenomics', 'seismology', 'genome', 'soykbr', 'soykbr',
            'soykbr', 'epigenomics', 'cycles'
        ]

        workflows = [Workflow(id_=i, file_path=f"{path}/{wf_types[i]}/{wf_types[i]}_{num_tasks[i]}.json",
                     wf_type=wf_types[i], machines=machines, add_dummies=True) for i in range(n)]
        return workflows

    def get_ready_tasks(self):
        return [t for t in self.tasks if t.status == TaskStatus.READY]

    # NOTE: This can be written in one line.
    # Gets the starting tasks which are the entry tasks to begin with.

    def starting_ready_tasks(self):
        ready_tasks = list()
        for child in self.tasks[0].children_edges:
            if child.node.status == TaskStatus.READY:
                ready_tasks.append(child.node)
        return ready_tasks

    def str_id(self):
        return f"WORKFLOW    ID = {self.id}"

    def str_col_id(self):
        return f"{Back.RED}WORKFLOW    ID = {self.id}{Back.RESET}"

    # FIXME: THIS IS NOT AVG check later!!
    def calc_avg_comp_cost(self):
        self.avg_comp_cost = sum([task.avg_cost() for task in self.tasks])
        return self.avg_comp_cost

    def calc_avg_com_cost(self):
        self.avg_com_cost = sum([task.avg_com_cost() for task in self.tasks])
        return self.avg_com_cost

    # ccr = Communication to computation ratio.
    def calc_ccr(self):
        if self.avg_comp_cost == -1:
            self.calc_avg_comp_cost()
        if self.avg_com_cost == -1:
            self.calc_avg_com_cost()
        ccr = self.avg_com_cost / self.avg_comp_cost
        return ccr

    @staticmethod
    def level_order(tasks):
        levels = dict()
        level: int = 0

        # Level 0
        levels[level] = [tasks[0]]
        tasks[0].level = 0

        while levels[level]:
            current_level = level
            for task in levels[current_level]:
                # Check if we are on the first task
                if task is levels[current_level][0]:
                    level += 1
                    # Set the next level
                    levels[level] = list()

                for child_edge in task.children_edges:
                    child = child_edge.node
                    if child not in levels[level]:
                        levels[level].append(child)
                        child.level = level
                        # print(f'T[{child.id + 1}] {"A" if child.wf_id == 0 else "B"} --- level: {child.level}')
        # Remove the "wrongly" placed tasks from higher levels.

        visited = set()
        filtered_levels = {level: list() for level in levels.keys()}
        for task in tasks:
            if task not in visited:
                # print(task.level)
                filtered_levels[task.level].append(task)
                visited.add(task)
            # print(task.str_colored(), task.level)

        return filtered_levels

    def get_task(self, index):
        return self.tasks[index]

    def recipe(self):
        return [{"id": task,
                 "start": task.start,
                 "end": task.end,
                 "machine_id": task.machine_id} for task in self.tasks]

    # This method is needed to "clean" the workflow to prepare it most likely for next
    # workflow recipe to take in place. This is a must in our method to use in genetic algos.
    def reset_workflow(self, sort_tasks: bool = False):
        for task in self.tasks:
            task.reset()

        if sort_tasks is True:
            self.tasks.sort(key=lambda t: t.id)


def check_workflow(workflow):
    schedule_checker(workflow.tasks, workflow.machines)
