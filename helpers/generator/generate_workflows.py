from wfcommons import WorkflowGenerator
from os.path import isfile
from wfcommons.wfchef.recipes import BlastRecipe, SrasearchRecipe, SeismologyRecipe, MontageRecipe, EpigenomicsRecipe, CyclesRecipe, GenomeRecipe, SoykbRecipe
# To create a folder as well
# import os
# from time import gmtime, strftime
# file_path = f'{path}/{wf_type} {strftime("%Y-%m-%d %H_%M_%S", gmtime())}' if unique_file else f'{path}/{wf_type}'
# os.makedirs(file_path)
WF_TYPES = ['cycles', 'epigenomics', 'genome', 'montage', 'seismology', 'soykbr', 'blast', 'sra']
NUM_TASKS = [10, 50, 100, 200, 500, 1000]
# NUM_TASKS = [300, 400]


def create_wfs(wf_type: str, i: int, path: str = './data', num_tasks: int = 200):

    if wf_type not in WF_TYPES:
        raise Exception('Not a valid name for a recipe!')

    file_name = f'{path}/{wf_type}/{wf_type}_{num_tasks}_{i}'

    # If the file exists already just return.
    if isfile(f'{file_name}.json'):
        return

    try:
        if wf_type == 'cycles':
            recipe = CyclesRecipe.from_num_tasks(num_tasks=num_tasks)
        elif wf_type == 'epigenomics':
            recipe = EpigenomicsRecipe.from_num_tasks(num_tasks=num_tasks)
        elif wf_type == 'genome':
            recipe = GenomeRecipe.from_num_tasks(num_tasks=num_tasks)
        elif wf_type == 'montage':
            recipe = MontageRecipe.from_num_tasks(num_tasks=num_tasks)
        elif wf_type == 'seismology':
            recipe = SeismologyRecipe.from_num_tasks(num_tasks=num_tasks)
        elif wf_type == 'soykbr':
            recipe = SoykbRecipe.from_num_tasks(num_tasks=num_tasks)
        elif wf_type == 'blast':
            recipe = BlastRecipe.from_num_tasks(num_tasks=num_tasks)
        elif wf_type == 'sra':
            recipe = SrasearchRecipe.from_num_tasks(num_tasks=num_tasks)
        else:
            raise Exception('Not a valid name for a recipe!')
        generator = WorkflowGenerator(recipe)
        workflow = generator.build_workflow()
        workflow.write_json(f'{file_name}.json')
        workflow.write_dot(f'{file_name}.dot')
        print(f"Created -> {file_name}.dot")
        print(f"Created -> {file_name}.json")
    except ValueError:
        print(f"Low tasks for {wf_type}. (n >= 133 for montage and n >= 14 for soykbr)")


def create_all_wfs():
    # for n_tasks in NUM_TASKS:
    #     for w_type in WF_TYPES:
    #         create_wfs(wf_type=w_type, num_tasks=n_tasks)
    for i in [0, 1, 2]:
        for n_tasks in [100]:
            for w_type in WF_TYPES:
                create_wfs(wf_type=w_type, i=i, num_tasks=n_tasks)


create_all_wfs()
# file_name = 'data/epigenomics-wf.json'
# creating a Seismology workflow recipe based on the number
# of pair of signals to estimate earthquake STFs
# recipe = MontageRecipe.from_num_tasks(num_tasks=10)
# recipe = SeismologyRecipe.from_num_pairs(num_pairs=5)
# recipe = EpigenomicsRecipe.from_num_tasks(num_tasks=50)

# recipe = MontageRecipe.from_num_pairs(num_pairs=10)

# creating an instance of the workflow generator with the
# Seismology workflow recipe
# generator = WorkflowGenerator(recipe)

# generating a synthetic workflow trace of the Seismology workflow
# workflow = generator.build_workflow()

# writing the synthetic workflow trace into a JSON file
# workflow.write_json(file_name)

#########################################################################
# TRACES
# obtaining list of trace in the folder
# TRACES_PATH = 'pegasus-traces-master/seismology/chameleon-cloud/'
# trace_files = [f for f in listdir(TRACES_PATH) if isfile(join(TRACES_PATH, f))]
#
#
# # creating the trace analyzer object
# analyzer = TraceAnalyzer()
#
# # appending trace files to the trace analyzer
# for trace_file in trace_files:
#     trace = Trace(input_trace=TRACES_PATH + trace_file)
#     analyzer.append_trace(trace)
#
# # list of workflow task name prefixes to be analyzed in each trace
# workflow_tasks = ['sG1IterDecon', 'wrapper_siftSTFByMisfit']
#
# # building the trace summary
# traces_summary = analyzer.build_summary(workflow_tasks, include_raw_data=True)
#
# # generating all fir plots (runtime, and input and output files)
# analyzer.generate_all_fit_plots(outfile_prefix='fits/seismology')
