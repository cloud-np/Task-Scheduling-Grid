from algos.heuristic import heft, cpop
from algos.genetics import bga

if __name__ == "__main__":
    # # 4. Add the dummy nodes properly
    # Task.add_dummy_nodes(tasks, machines)

    # # 5. Get the schedule from preferred algorithm.
    # schedule = heft(tasks, machines)
    # schedule = example_heft()
    # wf = Workflow(id_=0, file_data='dataset/epigenomics-workflow.json')

    workflows = bga()
    # cpop(wf.tasks, wf.machines)
    # for wf in workflows:
    #     wf.print_info(True)
    #     check_workflow(wf)
    # check_workflow(wf)
