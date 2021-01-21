from classes.Machine import Machine
from classes.Task import Task
from colorama import Fore, Back, Style
from helpers.data_parser.data_parser import get_tasks_from_json_file
from algos.example_data import *
from helpers.checker.checker import schedule_checker
from random import choice

WF_TYPES = ['cycles', 'epigenomics', 'genome', 'montage', 'seismology', 'soykbr']


# Each Workflow has each very own Tasks and Machines
# objects. This is crucial because the are not referencing
# the same objects in memory. In the case of genetic tho
# you we should either use another class or use this one
# with caution when we create the "child-workflows"
# in any CASE tho tasks and machines lists should NEVER change
# at all. I should try to make them immutable later on.
class Workflow:
    def __init__(self, id_, wf_type, name=None, file_path=None, deadline=None, example_data='deadline-constrain',
                 tasks=None, machines=None):
        self.id = id_
        # This should be describing the type of the workflow e.g: LIGO, Montage, etc
        self.type = wf_type
        self.name = name
        self.tasks = tasks
        self.machines = machines
        self.deadline = deadline
        # This var actually shows how the workflow is going to get executed

        if tasks is None or machines is None:
            if file_path is None:
                self.setup_data_example(example_data)
                self.type = "Heft paper example."
            else:
                # 1. Generate machines
                self.machines = Machine.get_4_machines()
                # # 2. Parse the workflow tasks
                self.tasks = get_tasks_from_json_file(file_path)
                # # 3. Calculate the runtime cost for every machine
                Machine.assign_tasks_with_costs(self.machines, self.tasks)

    def __str__(self):
        return f"{self.id_str()}\n" \
               f"{Fore.BLUE}Type:{Fore.RESET} {self.type} \n" \
               f"{Fore.MAGENTA}Num-tasks:{Fore.RESET} {len(self.tasks)}\n" \
               f"{Fore.RED}Len:{Fore.RESET} {self.get_workflow_len()}" \


    @staticmethod
    def generate_multiple_workflows(n_wfs: int, n_tasks: int, path: str = './datasets'):
        workflows = list()
        for i in range(n_wfs):
            wf_type = choice(WF_TYPES)
            # We can't have these type of workflows with less than that tasks.
            if (wf_type == 'montage' and n_tasks < 133) or (wf_type == 'soykbr' and n_tasks < 14):
                i -= 1
                continue
            workflows.append(Workflow(id_=i, file_path=f'{path}/{wf_type}/{wf_type}_{n_tasks}.json', wf_type=wf_type))
        return workflows

    def get_workflow_len(self):
        return max(self.machines, key=lambda m: m.schedule_len).schedule_len

    def id_str(self):
        return f"{Back.RED}WORKFLOW    ID = {self.id}{Back.RESET}"

    def print_info(self, show_tasks=False):
        print(f"\t\t\t{self.id_str()}")

        if show_tasks:
            for machine in self.machines:
                print(f"{machine.convert_tasks_to_str()}")

        print(f"{Fore.BLUE}WK-LEN:{Fore.RESET} {self.get_workflow_len()}")

    def get_machine(self, index):
        return self.machines[index]

    def get_task(self, index):
        return self.tasks[index]

    def recipe(self):
        return [{"id": task,
                 "start": task.start,
                 "end": task.end,
                 "machine_id": task.machine_id} for task in self.tasks]

    # This method is needed to "clean" the workflow to prepare it most likely for next
    # workflow recipe to take in place. This is a must in our method to use in genetic algos.
    def clear_workflow(self, sort_tasks: bool = False):
        for task in self.tasks:
            task.clear()
        for machine in self.machines:
            machine.clear()

        if sort_tasks is True:
            self.tasks.sort(key=lambda t: t.id)

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

        self.machines = [Machine(i, f'M-{i}', network_speed=1) for i in range(len(costs[0]))]
        self.tasks = tasks


def check_workflow(workflow):
    schedule_checker(workflow.tasks, workflow.machines)
