import json


def create_schedule_json(schedule):
    data = create_json_from_schedule(schedule)
    with open('schedule.json', 'w') as f:
        json.dump(data, f)


def create_json_from_schedule(schedule):
    data = {"workflow": {"makespan": 0.0, "machines": [], "jobs": []}}

    for task in schedule["tasks"]:
        data["workflow"]["jobs"].append({
            'id': task.id,
            'name': task.name,
            'start': task.start,
            "children": [child_edge.node.name for child_edge in task.children_edges],
            "parents": [parent_edge.node.name for parent_edge in task.parents_edges],
            'end': task.end,
            'processor': 'Processor ' + str(task.machine_id)
        })

    return data
