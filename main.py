from heft_paper.heuristic import heft
from heft_paper.heuristic import heft, cpop
from classes.Task import Task
from classes.Machine import Machine
from helpers.checker.checker import schedule_checker
from classes.Workflow import Workflow


# # 4. Add the dummy nodes properly
# Task.add_dummy_nodes(tasks, machines)

# # 5. Get the schedule from preferred algorithm.
# schedule = heft(tasks, machines)
# schedule = example_heft()
# wf = Workflow(id_=0, file_data='dataset/epigenomics-workflow.json')
wf = Workflow(id_=1)
cpop(wf.tasks, wf.machines)
wf.print_workflow()
wf.check_workflow()

# create_schedule_json(schedule)
# for task in tasks:
#     print(task)
