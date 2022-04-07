import classes.task as ta
from algos.calc_task_ranks import calculate_upward_ranks
from colorama import Fore, Back
from helpers.checker import workflow_checker
from typing import Optional, List
from helpers.data_parser import get_tasks_from_json_file
from helpers.examples.example_data import NAMES_A, NAMES_B, COSTS_A, COSTS_B, \
    TASK_DAG_A, TASK_DAG_B, PARENTS_DAG_A, PARENTS_DAG_B
from random import choice
import networkx as nx

# 'montage' not working properly
# 'soykbr' wfcommons 0.7 not working properly
WF_TYPES = ['cycles', 'epigenomics', 'genome',
            'seismology', 'soykbr', 'blast', 'sra']
NUM_TASKS = [50, 100, 200, 300, 400, 500, 1000]
CACHED_WFS = dict()


# Each Workflow has each very own Tasks and Machines
# objects. This is crucial because the are not referencing
# the same objects in memory. In the case of genetic tho
# you we should either use another class or use this one
# with caution when we create the "child-workflows"
# in any CASE tho tasks and machines lists should NEVER change
# at all. I should try to make them immutable later on.
class Workflow:
    def __init__(self, id_, wf_type, machines, add_dummies, file_path: str = "", name: str = None, tasks: Optional[List[ta.Task]] = None):
        self.id: int = id_
        self.type = wf_type  # type of the workflow e.g: LIGO, Montage, etc
        self.name: str = name
        self.wf_len: float = 0
        self.tasks: Optional[List[ta.Task]] = tasks
        self.scheduled: bool = False
        self.finishing_time: float = -1.0
        self.avg_comp_cost: float = -1.0
        self.machines = machines
        self.file_path: str = file_path
        self.avg_com_cost: float = -1.0
        self.ccr: float = -1.0

        if tasks is None:
            # 1. Parse the workflow tasks
            if file_path.endswith(".dot"):
                self.tasks = self.read_dag()
            else:
                self.tasks = get_tasks_from_json_file(file_path, id_, self.machines[0].network_kbps)

            # 2. add dummy nodes
            if add_dummies:
                self.__add_dummy_nodes()

        # 3. Calculate the runtime cost for every machine
        for m in machines:
            m.assign_tasks_with_costs(tasks=self.tasks)

        # 4. Generate critical path, up_rank and down_rank
        self.cp_info = {"critical_path": set(), "entry": None, "exit": None}

        # Calculate downward and upward ranks
        calculate_upward_ranks(self.tasks)
        # calculate_downward_ranks(self.tasks)
        # self.create_critical_path()

        # Calc ccr which means also the avg_comp and avg_com costs
        self.ccr = self.calc_ccr()

        # From the avg comp cost of the tasks add them all together * some number and get the deadline
        self.deadline = self.avg_comp_cost * 10

        # Assign to all the tasks the wf_deadline
        for t in self.tasks:
            t.wf_deadline = self.deadline

    def set_scheduled(self, is_scheduled: bool):
        if is_scheduled:
            # Since we have to check for the tasks to be scheduled
            # I don't want to use max() just to be a bit faster even
            # though by theory it would still be O(n)
            for t in self.tasks:
                if t.status != ta.TaskStatus.SCHEDULED:
                    raise Exception(
                        "Workflow can't be scheduled if all of his tasks haven't ended.")
                elif t.end > self.wf_len:
                    self.wf_len = t.end
            self.scheduled = True
            # workflow_checker(self)
        else:
            self.scheduled = False

    @staticmethod
    def blueprint_to_workflow(id_, tasks, machines):
        for t in tasks:
            t.create_edges(tasks)
        return Workflow(id_=id_, machines=machines, tasks=tasks, wf_type="Random", add_dummies=False)

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
        self.tasks.insert(0, ta.Task.make_dummy_node(0, self.id, "Dummy-In"))
        self.tasks.append(ta.Task.make_dummy_node(
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
        dummy_in.status = ta.TaskStatus.READY
        dummy_out.is_exit = True

    @staticmethod
    def connect_wfs(workflows, machines):
        dummy_in: ta.Task = ta.Task.make_dummy_node(
            id_=-1, wf_id=-1, name="Dummy-In-BIG")
        # To find the dummy_out.id we need to calc all the tasks in all workflows
        dummy_out: ta.Task = ta.Task.make_dummy_node(
            id_=sum(len(wf.tasks) for wf in workflows), wf_id=-1, name="Dummy-Out-BIG")
        all_tasks: List[ta.Task] = [dummy_in]
        dummy_in.costs: List[int] = [0 for _ in machines]

        for wf in workflows:
            for task in wf.tasks:
                if task.is_entry:
                    dummy_in.add_child(0, task)
                    task.add_parent(0, dummy_in)
                    task.is_entry = False
                    task.status = ta.TaskStatus.UNSCHEDULED
                if task.is_exit:
                    dummy_out.add_parent(0, task)
                    task.add_child(0, dummy_out)
                    task.is_exit = False
                all_tasks.append(task)

        dummy_in.is_entry = True

        all_tasks.append(dummy_out)
        dummy_out.costs = [0 for _ in machines]
        dummy_in.status = ta.TaskStatus.READY
        dummy_out.is_exit = True
        return all_tasks

    def create_critical_path(self):
        for task in self.tasks:
            if task.down_rank is None:
                print(task)
            task.set_priority(task.down_rank + task.up_rank)

        critical_path, [entry_task, exit_task] = self.construct_critical_path()
        self.cp_info = {"critical_path": critical_path,
                        "entry": entry_task, "exit": exit_task}
        return critical_path, [entry_task, exit_task]

    def show_task_and_edges(self):
        for t in self.tasks:
            print(t)
            for e in t.children_edges:
                print(f"\t{e}")

    def find_an_entry_task(self):
        for task in self.tasks:
            if task.is_entry:
                return task
        raise Exception("NO entry task found!")

    def construct_critical_path(self):
        critical_path = []

        # Find an entry task
        entry_task = self.find_an_entry_task()

        entry_priority = round(entry_task.priority, 5)
        temp_task = entry_task
        critical_path.append(temp_task)

        # Start from an entry task and run until you find an exit task.
        # Then the critical path would be ready.
        while temp_task.is_exit is False:
            for child_edge in temp_task.children_edges:
                diff: float = entry_priority - child_edge.node.priority
                if abs(diff) < 0.90:
                    temp_task = child_edge.node
                    critical_path.append(child_edge.node)
                    break
        exit_task = temp_task
        # The second return is supposed to be the initialised
        return critical_path, [entry_task, exit_task]

    @staticmethod
    def load_paper_example_workflows(machines):
        names = [NAMES_A, NAMES_B]
        # ranks = [RANKS_A, RANKS_B]
        costs = [COSTS_A, COSTS_B]
        children_dags = [TASK_DAG_A, TASK_DAG_B]
        parents_dags = [PARENTS_DAG_A, PARENTS_DAG_B]
        tasks = [[], []]
        for wf_id in range(2):
            # We do +1 because we usally add an entry node with id = 0
            tasks[wf_id] = [ta.Task(id_=i + 1,
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
                children_edges = [ta.Edge(
                    weight=children_dags[wf_id][task.id - 1][i]["w"], node=child) for i, child in enumerate(children)]
                parents_edges = [ta.Edge(weight=parents_dags[wf_id][task.id - 1]
                                         [i]["w"], node=parent) for i, parent in enumerate(parents)]
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
                                    user_set_tasks: int = 0, path: str = './data'):
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
    def load_all_types_wfs(machines, n, n_tasks, path: str = './data'):
        workflows = [Workflow(id_=i + (n * len(WF_TYPES)), file_path=f"{path}/{wft}/{wft}_{n_tasks}_{n}.json",
                     wf_type=wft, machines=machines, add_dummies=True) for i, wft in enumerate(WF_TYPES)]
        return workflows

    @staticmethod
    def load_heft_wfs(machines, n, n_tasks):
        import os
        workflows = []
        for entry in os.scandir('./data/generated_dags/'):
            if len(workflows) >= n:
                break
            if entry.is_dir() or entry.is_file():
                # print(entry.name, entry.name.split('-')[0])
                if '.dot' in entry.name and int(entry.name.split('_')[0]) == n_tasks:
                    workflows.append(Workflow(id_=len(workflows), wf_type="random",
                                     file_path=f"./data/generated_dags/{entry.name}", machines=machines, add_dummies=True))

        for wf in workflows:
            print(wf)

    @staticmethod
    def load_random_workflows(machines, n, path: str = './data'):
        num_tasks = [
            100, 100, 200, 200, 500, 50,
            200, 300, 400, 100, 500, 100, 50,
            50, 100, 200, 1000, 50, 300, 200,
            500, 50, 400, 100, 1000, 400,
            1000, 500, 1000, 200, 300, 400, 50,
            50, 100, 50, 300, 500, 50, 1000,
            300, 500, 400, 200, 500, 300, 50,
            200, 500, 1000
        ]
        wf_types = [
            'cycles', 'genome', 'seismology', 'cycles', 'soykbr', 'epigenomics',
            'genome', 'cycles', 'seismology', 'genome', 'cycles', 'genome', 'epigenomics',
            'blast', 'genome', 'blast', 'blast', 'sra', 'soykbr', 'blast',
            'cycles', 'sra', 'blast', 'epigenomics', 'soykbr', 'genome',
            'genome', 'cycles', 'seismology', 'blast', 'sra', 'genome', 'epigenomics',
            'blast', 'genome', 'epigenomics', 'seismology', 'genome', 'sra', 'soykbr',
            'cycles', 'genome', 'sra', 'blast', 'genome', 'soykbr', 'blast',
            'soykbr', 'epigenomics', 'cycles'
        ]

        workflows = [Workflow(id_=i, file_path=f"{path}/{wf_types[i]}/{wf_types[i]}_{num_tasks[i]}.json",
                     wf_type=wf_types[i], machines=machines, add_dummies=True) for i in range(n)]
        return workflows

    def get_ready_tasks(self):
        return [t for t in self.tasks if t.status == ta.TaskStatus.READY]

    def starting_ready_tasks(self) -> List[ta.Task]:
        return [child.node for child in self.tasks[0].children_edges if child.node.status == ta.TaskStatus.READY]

    def str_id(self):
        return f"WORKFLOW    ID = {self.id}"

    def str_col_id(self):
        return f"{Back.RED}WORKFLOW    ID = {self.id}{Back.RESET}"

    def calc_avg_comp_cost(self):
        self.avg_comp_cost = sum(task.avg_cost()
                                 for task in self.tasks) / len(self.tasks)
        return self.avg_comp_cost

    def get_ready_unscheduled_tasks(self):
        return [t for t in self.tasks if t.status in (ta.TaskStatus.READY, ta.TaskStatus.UNSCHEDULED)]

    def calc_avg_com_cost(self):
        # Get all the edges and remove the duplicates
        all_edges = [task.children_edges for task in self.tasks]
        all_edges = set(sum(all_edges, []))

        self.avg_com_cost = sum(e.weight for e in all_edges) / len(self.tasks)
        return self.avg_com_cost

    # ccr = Communication to computation ratio.
    def calc_ccr(self):
        if self.avg_comp_cost == -1:
            self.calc_avg_comp_cost()
        if self.avg_com_cost == -1:
            self.calc_avg_com_cost()
        return self.avg_com_cost / self.avg_comp_cost

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
        filtered_levels = {level: [] for level in levels.keys()}
        for task in tasks:
            if task not in visited:
                # print(task.level)
                filtered_levels[task.level].append(task)
                visited.add(task)
            # print(task.str_colored(), task.level)

        return filtered_levels

    def get_task_by_id(self, id_):
        return [t for t in self.tasks if t.id == id_][0]

    def recipe(self):
        return [{"id": task,
                 "start": task.start,
                 "end": task.end,
                 "machine_id": task.machine_id} for task in self.tasks]

    def read_dag(self, ccr=0.5):
        import pydot
        import numpy as np
        from random import randint, gauss

        graph = pydot.graph_from_dot_file(self.file_path)[0]

        tasks = []
        task_counter = 1
        for n in graph.get_node_list():
            runtime = float(n.obj_dict['attributes']['alpha'].split('\"')[1])
            tasks.append(ta.Task(id_=task_counter,
                                 wf_id=self.id,
                                 costs=[],
                                 runtime=runtime,
                                 name=f"{self.file_path}-{self.id}-{task_counter}"))
            task_counter += 1

        comp_total = sum(sum(m.generate_cost_for_task(t.runtime)
                         for m in self.machines) for t in tasks)
        mu = ccr * comp_total / len(graph.get_edge_list())
        for e in graph.get_edge_list():
            s_task, d_task = tasks[int(e.get_source()) - 1], tasks[int(e.get_destination()) - 1]
            edge_w = abs(gauss(mu, mu / 4))
            s_task.add_child(edge_w, d_task)
            d_task.add_parent(edge_w, s_task)

        # Find entry and exit nodes
        for t in tasks:
            if len(t.children_edges) == 0:
                t.is_exit = True
            if len(t.parents_edges) == 0:
                t.is_entry = True

        return tasks
