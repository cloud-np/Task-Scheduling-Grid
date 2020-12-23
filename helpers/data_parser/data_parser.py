import csv
from helpers.helpers import get_id_from_name


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
