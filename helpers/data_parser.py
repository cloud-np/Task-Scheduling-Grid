import csv
import json
from classes.task import Task, Edge
import classes.machine as Machines
from typing import List
from helpers.utils import get_id_from_name


def get_tasks_from_json_file(file_name, wf_id, network_kbps):
    with open(file_name) as f:
        data = json.load(f)

    # Visualize the graph to check it.
    # create_csv_file_to_visualize_graph(data['workflow']['jobs'])
    tasks = []

    # n_tasks = len(data['workflow']['jobs'])
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
                costs=[],
                runtime=job['runtime'],
                files=job['files'],
                children_names=job['children'],
                parents_names=job['parents']
            )
        )
    for t in tasks:
        t.create_edges(tasks, network_kbps)
    return tasks


def create_csv_file_to_visualize_graph(jobs):
    nodes = []
    edges = []
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
