from classes.Machine import Machine
from classes.Task import Task
from heft_paper.example_data import COSTS, NAMES, TASK_DAG
from helpers.checker.checker import schedule_checker


class Workflow:
    def __init__(self, id_, wf_type=None, file_data=None):
        self.id = id_
        # This should be describing the type of the workflow e.g: LIGO, Montage, etc
        self.type = wf_type

        if file_data is None:
            self.setup_data_example()
            self.type = "Heft paper example."
        else:
            # 1. Generate machines
            self.machines = Machine.get_4_machines()
            # # 2. Parse the workflow tasks
            self.tasks = Task.get_tasks_from_json_file(file_data)
            # # 3. Calculate the runtime cost for every machine
            Machine.assign_tasks_with_costs(self.machines, self.tasks)

    def print_workflow(self):
        for task in self.tasks:
            if task.priority is not None:
                print(f"p: {task.priority} {task}")
            else:
                print(task)
        for machine in self.machines:
            print(machine)

    def setup_data_example(self):
        tasks = [Task(id_=i,
                      name=NAMES[i],
                      costs=COSTS[i],
                      runtime=None,
                      files=None,
                      children_names=None,
                      parents_names=None
                      )
                 for i in range(0, len(TASK_DAG))]

        for i in range(len(TASK_DAG)):
            for j in range(len(TASK_DAG[i])):
                if TASK_DAG[i][j] != -1:
                    tasks[i].add_child(TASK_DAG[i][j], tasks[j])
                    tasks[j].add_parent(TASK_DAG[i][j], tasks[i])

        for task in tasks:
            if len(task.children_edges) == 0:
                task.is_exit_task = True

        # Just hard code this for the example ffs
        tasks[1].is_entry_task = True

        self.machines = [Machine(i, f'M-{i}', network_speed=1) for i in range(len(COSTS[0]))]
        self.tasks = tasks

    def check_workflow(self):
        schedule_checker(self.tasks, self.machines)
