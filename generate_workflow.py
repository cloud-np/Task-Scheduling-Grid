from workflowhub import Trace, TraceAnalyzer, WorkflowGenerator
from workflowhub.generator import SeismologyRecipe, MontageRecipe, EpigenomicsRecipe
from classes.Task import Task
import json
from os import listdir
from os.path import isfile, join
file_name = 'dataset/epigenomics-workflow.json'
# creating a Seismology workflow recipe based on the number
# of pair of signals to estimate earthquake STFs
# recipe = MontageRecipe.from_num_tasks(num_tasks=10)
# recipe = SeismologyRecipe.from_num_pairs(num_pairs=5)
recipe = EpigenomicsRecipe.from_num_tasks(num_tasks=50)

# recipe = MontageRecipe.from_num_pairs(num_pairs=10)

# creating an instance of the workflow generator with the
# Seismology workflow recipe
generator = WorkflowGenerator(recipe)

# generating a synthetic workflow trace of the Seismology workflow
workflow = generator.build_workflow()

# writing the synthetic workflow trace into a JSON file
workflow.write_json(file_name)

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
