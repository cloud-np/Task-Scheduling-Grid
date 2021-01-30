from classes.Machine import Machine
from classes.Task import Task
from typing import Set
from colorama import Fore, Back
from helpers.data_parser import get_tasks_from_json_file
from algos.example_data import *
from helpers.checker import schedule_checker
from random import choice

WF_TYPES = ['cycles', 'epigenomics', 'genome', 'montage', 'seismology', 'soykbr']
NUM_TASKS = [10, 14, 20, 30, 50, 100, 133, 200, 300, 400, 500, 1000]


# Each Workflow has each very own Tasks and Machines
# objects. This is crucial because the are not referencing
# the same objects in memory. In the case of genetic tho
# you we should either use another class or use this one
# with caution when we create the "child-workflows"
# in any CASE tho tasks and machines lists should NEVER change
# at all. I should try to make them immutable later on.
class Workflow:
    def __init__(self, id_, wf_type, machines, name=None, file_path=None, deadline=None,
                 example_data='deadline-constrain', tasks=None):
        self.id = id_
        # This should be describing the type of the workflow e.g: LIGO, Montage, etc
        self.type = wf_type
        self.name = name
        self.tasks = tasks
        self.deadline = deadline
        self.avg_comp_cost: float = -1.0
        self.avg_com_cost: float = -1.0
        self.ccr: float = -1.0
        # self.ready_tasks: Set[Task] = set()

        if tasks is None:
            if file_path is None:
                self.setup_data_example(example_data)
                self.type = "Heft paper example."
            else:
                # 1. Parse the workflow tasks
                self.tasks = get_tasks_from_json_file(file_path, id_)
                # 2. Add Dummy Nodes
                self.__add_dummy_nodes()
                # 3. Calculate the runtime cost for every machine
                Machine.assign_tasks_with_costs(tasks=self.tasks, machines=machines)

    def __str__(self):
        return f"{self.id_str()}\n" \
               f"{Fore.BLUE}Type:{Fore.RESET} {self.type} \n" \
               f"{Fore.MAGENTA}Num-tasks:{Fore.RESET} {len(self.tasks)}\n" \
               # f"{Fore.RED}Len:{Fore.RESET} {self.get_workflow_len()}" \

    def __add_dummy_nodes(self):
        self.tasks.insert(0, Task(id_=0,
                          wf_id=self.id,
                          name="Dummy-In",
                          costs=list(),
                          runtime=0,
                          files=None,
                          children_names=None,
                          parents_names=None))
        self.tasks.append(Task(id_=len(self.tasks),
                               wf_id=self.id,
                               name="Dummy-Out",
                               costs=list(),
                               runtime=0,
                               files=None,
                               children_names=None,
                               parents_names=None))

        dummy_in = self.tasks[0]
        dummy_out = self.tasks[len(self.tasks) - 1]
        for task in self.tasks:
            if task.is_entry_task:
                dummy_in.add_child(0, task)
                task.add_parent(0, dummy_in)
            if task.is_exit_task:
                dummy_out.add_parent(0, task)
                task.add_child(0, dummy_out)

    # TODO: If we end up using the same workflow for multiple workflows we should preload tasks and machines
    #       and just deepcopy these. Even that should be faster. This is not something that will effect us a lot but ok
    '''
        Generates multiple workflows randomly based on number of tasks and the workflows you need.
        It doesn't actually create them although I could do that but I found it kinda pointless atm.
        So it picks from some random pre-made ones.
    '''
    @staticmethod
    def generate_multiple_workflows(n_wfs: int, machines, user_set_tasks: int = 0, path: str = './datasets'):
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
                                          wf_type=wf_type, machines=machines))
        return workflows

    @staticmethod
    def load_example_workflows(machines, path: str = './datasets'):
        n = 10
        workflows = list()
        num_tasks = [10, 50, 20, 500, 30, 100, 14, 50, 400, 200]
        wf_types = ['cycles', 'genome', 'seismology', 'montage', 'soykbr', 'epigenomics',
                    'genome', 'cycles', 'seismology', 'montage']
        for i in range(n):
            workflows.append(Workflow(id_=i, file_path=f"{path}/{wf_types[i]}/{wf_types[i]}_{num_tasks[i]}.json",
                                      wf_type=wf_types[i], machines=machines))
        return workflows

    # Gets the starting tasks which are the entry tasks to begin with.
    def starting_ready_tasks(self):
        ready_tasks = list()
        for child in self.tasks[0].children_edges:
            # TODO: This is should be always true anyway but check it
            #       but for now just to be sure.
            if child.node.status == 1:
                ready_tasks.append(child.node)
        return ready_tasks

    def id_str(self):
        return f"{Back.RED}WORKFLOW    ID = {self.id}{Back.RESET}"

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
        self.ccr = self.avg_com_cost / self.avg_comp_cost
        return self.ccr

    # def get_machine(self, index):
    #     return self.machines[index]

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
        # for machine in self.machines:
        #     machine.reset()

        if sort_tasks is True:
            self.tasks.sort(key=lambda t: t.id)

    # TODO: Needs rework
    def setup_data_example(self, example):
        if example == 'heft':
            names = NAMES
            costs = COSTS
            task_dag = TASK_DAG
        elif example == 'deadline-constrain':
            names = NAMES_1
            costs = COSTS_1
            task_dag = TASK_DAG_1
        else:
            raise ValueError(f"There is not an example-data with the name: {example}")

        tasks = [Task(id_=i,
                      name=names[i],
                      costs=costs[i],
                      runtime=None,
                      files=None,
                      children_names=None,
                      parents_names=None
                      )
                 for i in range(0, len(task_dag))]

        for i in range(len(task_dag)):
            for j in range(len(task_dag[i])):
                if task_dag[i][j] != -1:
                    tasks[i].add_child(task_dag[i][j], tasks[j])
                    tasks[j].add_parent(task_dag[i][j], tasks[i])

        for task in tasks:
            if len(task.children_edges) == 0:
                task.is_exit_task = True

        # We just hardcode here to fix the entry/exit nodes
        if example == 'heft':
            tasks[1].is_entry_task = True
        else:
            # Entry nodes
            for i in range(1, 5):
                tasks[i].is_entry_task = True
            # Exit nodes
            for i in range(8, 12):
                tasks[i].is_exit_task = True

        # This is really important so we can start scheduling correctly the tasks
        tasks[0].status = 1

        # self.machines = [Machine(i, f'M-{i}') for i in range(len(costs[0]))]
        self.tasks = tasks


def check_workflow(workflow):
    schedule_checker(workflow.tasks, workflow.machines)
