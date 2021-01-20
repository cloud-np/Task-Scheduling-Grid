from algos.heuristic import heft, cpop
from algos.genetics import bga
from classes.Workflow import Workflow

if __name__ == "__main__":
    # # 4. Add the dummy nodes properly
    # Task.add_dummy_nodes(tasks, machines)

    # # 5. Get the schedule from preferred algorithm.
    # schedule = heft(tasks, machines)
    # schedule = example_heft()
    workflows = Workflow.generate_multiple_workflows(n_wfs=10, n_tasks=20)
    for wf in workflows:
        print(wf)
    # wf = Workflow(id_=0, file_data='datasets/epigenomics-workflow.json')

    workflows = bga()
    # cpop(wf.tasks, wf.machines)
    # for wf in workflows:
    #     wf.print_info(True)
    #     check_workflow(wf)
    # check_workflow(wf)
