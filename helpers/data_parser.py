import csv
import json
from classes.Task import *
from helpers.helpers import get_id_from_name


def get_tasks_from_json_file(file_name, wf_id):
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
                wf_id=wf_id,
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
        children: list = task.get_tasks_from_names(tasks, is_child_tasks=True)
        parents: list = task.get_tasks_from_names(tasks, is_child_tasks=False)
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


def create_csv_file_to_visualize_graph(jobs):
    nodes = list()
    edges = list()
    for job in jobs:
        name = job['name']
        job_id = get_id_from_name(name)
        #             id      label
        nodes.append((job_id, name))

        for child in job['children']:
            child_name = get_id_from_name(child)
            edges.append(
                # source  target     type        weight
                (job_id, child_name, 'Directed')
            )

    with open('nodes.csv', 'w', newline='') as f:
        the_writer = csv.writer(f)

        the_writer.writerow(['id', 'Label'])
        for node in nodes:
            the_writer.writerow(node)

    with open('edges.csv', 'w', newline='') as f:
        the_writer = csv.writer(f)
        the_writer.writerow(['source', 'target', 'type'])
        for edge in edges:
            the_writer.writerow(edge)
