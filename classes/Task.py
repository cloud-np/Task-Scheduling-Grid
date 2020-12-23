from colorama import Fore
from helpers.helpers import get_id_from_name
import json
DEBUG = False
ROUND_DIGIT = 2


def get_process_time_for_task(power, cost):
    # num = random.randint(0, 10)
    num = 0
    time = cost - power

    if (cost - power) < 0:
        time = num
    else:
        time += num
    return time


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

    def __str__(self):
        return f'--- {Fore.YELLOW}{self.weight}{Fore.RESET} --> {self.node.id_str()}'
    # Can't use this yet because Task __eq__ checks based the
    # rank attribute. It should be changed to name or id_
    # def __eq__(self, other):
    #     if isinstance(other, Edge):
    #         return self.node == other.node
    #     else:
    #         return NotImplemented


class Task:
    def __init__(self, id_, name, costs, runtime, files, children_names, parents_names):
        self.costs = costs
        self.id = id_
        self.name = name
        self.start = None
        self.end = None
        self.machine_id = None
        self.up_rank = None
        self.down_rank = None
        self.priority = None
        self.runtime = runtime
        self.files = files
        self.status = TaskStatus.UNSCHEDULED
        self.children_names = children_names
        self.children_till_ready = 0
        self.parents_names = parents_names
        self.parents_till_ready = 0
        self.children_edges = list()
        self.parents_edges = list()

        # This should be updated by the slowest parent.
        # This isn't needed but it should make it a bit faster if used
        self.slowest_parent = {'parent_task': None, 'communication_time': 0}

        # This if should be removed this serves as a "protection" from
        # the example_heft..
        self.is_exit_task = False
        self.is_entry_task = False

        # Empty lists evaluate to False
        if children_names is not None:
            self.children_till_ready = len(children_names)
            if len(children_names) == 0:
                self.is_exit_task = True

        # Empty lists evaluate to False
        if parents_names is not None:
            self.parents_till_ready = len(parents_names)
            if len(parents_names) == 0:
                self.is_entry_task = True
                self.status = TaskStatus.READY

        if self.is_entry_task == self.is_exit_task is True:
            raise Exception(f'Node[ {self.id} ] is not connected in the dag!')

        if name.startswith('Dummy') is True:
            self.up_rank = self.down_rank = 0
            self.end = 0
            self.start = 0

    def set_priority(self, priority_value):
        self.priority = priority_value

    def __str__(self):
        up_rank = self.up_rank if self.up_rank is not None else 0
        down_rank = self.down_rank if self.down_rank is not None else 0
        return f'{self.id_str()} cost: {Fore.RED}{[round(cost, ROUND_DIGIT) for cost in self.costs]}{Fore.RESET} ' \
               f'up-rank: {Fore.YELLOW}{round(up_rank, ROUND_DIGIT)}{Fore.RESET} ' \
               f'down_rank: {Fore.YELLOW}{round(down_rank, ROUND_DIGIT)}{Fore.RESET} process: {self.machine_id}'

    def start_str(self):
        return f'{Fore.RED}start:{Fore.RESET} {Fore.YELLOW}{round(self.start, ROUND_DIGIT)}{Fore.RESET}'

    def end_str(self):
        return f'{Fore.RED}end:{Fore.RESET} {Fore.YELLOW}{round(self.end, ROUND_DIGIT)}{Fore.RESET}'

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.id == other.id
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

    @staticmethod
    def find_task_by_name(tasks, name):
        for task in tasks:
            if task.name == name:
                return task
        return None

    def __get_tasks_from_names(self, tasks, is_child_tasks: bool):
        adj_tasks = list()
        names = self.children_names if is_child_tasks else self.parents_names
        for name in names:
            tmp = Task.find_task_by_name(tasks, name)
            if tmp is None:
                return ValueError
            else:
                adj_tasks.append(tmp)
        return adj_tasks

    def id_str(self):
        return f'T[{Fore.GREEN}{self.id}{Fore.RESET}]'

    def set_edges(self, children_edges, parents_edges):
        # Check if everything went fine in parsing.
        if DEBUG is True:
            if self.name.startswith('Dummy') is False:
                for i in range(len(children_edges)):
                    if children_edges[i].weight == 0 or parents_edges[i].weight == 0:
                        raise Exception("\nError when parsing edges an Edge weight is 0\n")
            print(f'Edges Parsed correctly {self.id_str()}')
        self.children_edges = children_edges
        self.parents_edges = parents_edges

    # This function runs once the task gets scheduled
    def update_children_and_self_status(self):
        if self.status == TaskStatus.SCHEDULED:
            raise Exception(f"\nError this task is already scheduled it should not run this function again! {self}\n")
        else:
            self.status = TaskStatus.SCHEDULED

        for child_edge in self.children_edges:
            # If dummy node do not update right away since the child has one parent only (the dummy)
            if self.name.startswith('Dummy'):
                child_edge.node.status = TaskStatus.READY
                continue
            # Update the child parent only if you are the slowest parent atm.
            if child_edge.node.slowest_parent['parent_task'] is None or \
                    child_edge.node.slowest_parent['parent_task'].end < self.end:
                child_edge.node.slowest_parent = {'parent_task': self, 'communication_time': child_edge.weight}
            # Update the child's counter for parents once that value
            # goes to 0 the child can start the schedule process itself
            # be careful the same parents should run this function once!
            if child_edge.node.parents_till_ready <= 0:
                raise Exception(f"\nThe child: {child_edge.node} is already ready! "
                                f"Task that tried to update it: {self}\n")
            else:
                child_edge.node.parents_till_ready -= 1
                if child_edge.node.parents_till_ready == 0:
                    child_edge.node.status = TaskStatus.READY

    def print_children(self):
        tmp_str = self.id_str()
        for child in self.children_edges:
            tmp_str += f' --> weight: {child.weight}  child: {child.node}  '
        return tmp_str

    def hello(self):
        pass

    def is_file_in_task(self, search_file):
        for file in self.files:
            if file['name'] == search_file['name']:
                return True
        return False

    # This should be in the Machine class
    # def create_costs(self, n_processors):
    #     new_costs = list()
    #     avg_cost = self.costs[0]
    #     for _ in range(n_processors):
    #         percentage = randint(1, 20)
    #         if randint(0, 1) == 1:
    #             percentage = -1 * percentage
    #         cost = floor(avg_cost + (avg_cost * percentage / 100))
    #         new_costs.append(cost)
    #     self.costs = new_costs

    # TODO:
    # These two should be swapped or deleted since we
    # should use the same logic for everything
    def add_parent(self, cost, task):
        # if self.name.startswith('Dummy'):
        #     self.is_entry_node = False
        self.parents_edges.append(Edge(cost, task))
        self.parents_till_ready += 1

    def add_child(self, cost, task):
        # self.is_exit_node = False
        self.children_edges.append(Edge(cost, task))
        self.children_till_ready += 1

    @staticmethod
    def get_tasks_from_json_file(file_name):
        with open(file_name) as f:
            data = json.load(f)

        # Visualize the graph to check it.
        # create_csv_file_to_visualize_graph(data['workflow']['jobs'])
        tasks = list()

        n_tasks = len(data['workflow']['jobs'])

        # 1) Parse first the machines you have to do the workflow. ( we create our machines )
        # 2) Parse the data for the tasks in the: data['workflow']['jobs'] ---> job['files']
        #       For the above dictionary you should sum the file sizes together
        #       to get the overall communication cost.
        for job in data['workflow']['jobs']:
            # Name & id
            # job['name'] <- This can and should be used as an id right away
            job_id = get_id_from_name(job['name'])
            ####################################

            # 3) Create the Task class based on the data you parsed.
            tasks.append(
                Task(
                    id_=job_id,
                    name=job['name'],
                    costs=list(),
                    runtime=job['runtime'],
                    files=job['files'],
                    children_names=job['children'],
                    parents_names=job['parents']
                )
            )

        for task in tasks:
            # Calculate the the edges between the nodes and their weights in KBS.
            # NOTE: not sure why but without the type notation this code below won't work..
            # ( I mean accessing stuff from the Task class)
            children: list = task.__get_tasks_from_names(tasks, is_child_tasks=True)
            parents: list = task.__get_tasks_from_names(tasks, is_child_tasks=False)
            # We need at least -> len(Edges) == len(children)
            children_edges = [Edge(weight=0, node=child) for child in children]
            parents_edges = [Edge(weight=0, node=parent) for parent in parents]

            for file in task.files:
                if file['link'] == 'output':
                    for i in range(len(children)):
                        if children[i].is_file_in_task(file):
                            children_edges[i].weight += file['size']
                elif file['link'] == 'input':
                    for i in range(len(parents)):
                        if parents[i].is_file_in_task(file):
                            parents_edges[i].weight += file['size']
            # We use this function to check if everything went smoothly in the parsing
            task.set_edges(children_edges, parents_edges)

        return tasks

    @staticmethod
    def add_dummy_nodes(tasks, machines):
        exit_nodes = list()
        entry_nodes = list()
        for task in tasks:
            if task.is_exit_task:
                exit_nodes.append(task)
            if task.is_entry_task:
                entry_nodes.append(task)

        dummy_in = Task(
            id_=0,
            name='Dummy-in_0',
            costs=[0 for _ in machines],
            runtime=0,
            files=None,
            parents_names=None,
            children_names=None
        )
        for entry_node in entry_nodes:
            dummy_in.children_edges.append(Edge(0, entry_node))
        tasks.insert(0, dummy_in)

        # Maybe we do not need a dummy_out.
        dummy_out = Task(
            id_=len(tasks),
            name=f'Dummy-out_{len(tasks)}',
            costs=[0 for _ in machines],
            runtime=0,
            files=None,
            parents_names=None,
            children_names=None
        )
        for exit_node in exit_nodes:
            dummy_out.parents_edges.append(Edge(0, exit_node))
        tasks.append(dummy_out)

    # TODO: Needs refactoring because we changed the Task class
    # this is a method to get data from .txt file
    # @staticmethod
    # def get_tasks_from_file(file_name):
    #     network_mbs = 20000
    #     tasks = list()
    #     with open(file_name, 'r') as f:
    #         # The first line is always the number of nodes we have
    #         # So we make a weight graph based on that
    #         # n_nodes = int(f.readline())
    #
    #         for line in f:
    #
    #             # print(line, end='')
    #             separated_line = line.split()
    #             if len(separated_line) > 1:
    #
    #                 # Edges
    #                 # This happens after the Tasks gets created
    #                 # So its safe to assume they exist already
    #                 # when we come in here. The prerequisite for this
    #                 # is that the in the all the files are constructed
    #                 # exactly the same way!
    #                 if separated_line[1].isdigit():
    #                     parent = int(separated_line[0])
    #                     child = int(separated_line[1])
    #                     communication_cost = floor(int(separated_line[2]) / network_mbs)
    #                     tasks[parent].add_child(Edge(communication_cost, tasks[child]))
    #                     tasks[child].add_parent(Edge(communication_cost, tasks[parent]))
    #                 # Tasks
    #                 else:
    #                     tasks.append(
    #                         Task(
    #                             id_=int(separated_line[0]),
    #                             name=separated_line[2],
    #                             costs=[float(separated_line[3])]
    #                         )
    #                     )
    #     return tasks
