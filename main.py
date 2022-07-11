from helpers.examples.example_data import HOLE_METHOD_VARIATIONS
from helpers.visuals.visualize import Visualizer
from classes.workflow import Workflow
from classes.machine import Machine
from helpers.examples.example_gen import ExampleGen
from helpers.simulation.simulation import Simulation, save_sims_to_excel
from classes.scheduler import FillMethod, Scheduler
from helpers.pick_best_method import find_seed_for
import random
from itertools import product
import xlsxwriter
from algos.ruin_and_recreate import RuinRecreate
from helpers.utils import find_perc_diff


random.seed(0)
# ss = []
# n_machines = 8
# network = 500
# # run_methods = [HOLE_METHOD_VARIATIONS['EFT_variations'], HOLE_METHOD_VARIATIONS['compositions'], HOLE_METHOD_VARIATIONS['criticals_unsorted'], HOLE_METHOD_VARIATIONS['holes-paper-2011']]
# run_methods = [HOLE_METHOD_VARIATIONS['EFT_variations'], HOLE_METHOD_VARIATIONS['LFT_variations']]
# run_methods = sum(run_methods, list())

# for n_machines in [8]:
#     # bold = workbook.add_format({'bold': True})
#     # wks = workbook.add_worksheet(f'Machines {n_machines}')
#     schedules = []
#     for n_workflows in [2]:

#         machines = Machine.load_n_static_machines(n_machines, network * 125)
#         workflows = Workflow.load_random_workflows(machines, n_workflows)
#         print('Number of workflows: ', n_workflows)

#         # Sim
#         sim = Simulation(run_methods, machines, workflows, visuals=True)
#         sim.run()
#         for s in sim.schedulers:
#             schedules.append({"method": s.method_used_info(concise=True), "s_len": s.schedule_len, "avg_util": s.machines_util_avg_perc, "avg_wf_len": s.avg_workflow_makespan})

#         print("----------------------------------")
# # machines, workflows = ExampleGen.load_n(m_info=[8, 125 * 50], n_wfs=n_wfs)
# # filename = "./data/generated_dags/50_0.1_0.8_0.2_2.dot"

n_machines = 4
network = 500
filename = "./data/cycles/cycles_100.json"
machines = Machine.load_n_static_machines(n_machines, network * 125)
wf = Workflow(id_=0, file_path=filename, wf_type="Random", machines=machines, add_dummies=True)

# HHeft
# Scheduler.heft_with_holes(wf.tasks, wf.machines, fill_method=FillMethod.FASTEST_FIT)
Scheduler.heft(wf.tasks, wf.machines)
wf.set_scheduled(is_scheduled=True)
print("Heft: ", int(wf.wf_len))
# Visualizer.visualize_machines(machines)

rr = RuinRecreate(wf, machines, ruin_method="order")
rr_wf, machines = rr.run()
# Visualizer.visualize_machines(machines)
rr_wf.set_scheduled(is_scheduled=True)
print("RR: ", int(rr_wf.wf_len))
