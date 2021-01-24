import json


def create_schedule_json(schedule):
    data = create_json_from_schedule(schedule)
    with open('schedule.json', 'w') as f:
        json.dump(data, f)


def create_json_from_schedule(schedule):
    data = {'schedule': []}

    for task in schedule['tasks']:
        data['schedule'].append({
            'id': task.id,
            'name': task.name,
            'start': task.start,
            'end': task.end,
            'processor': 'Processor ' + str(task.machine_id)
        })

    return data
