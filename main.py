from algos.paper_2011_algos.paper_method import Paper2011
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
# 100_0.4_0.8_0.2_1
# %%
ss = []
n_machines = 4
network = 500

# machines, workflows = ExampleGen.load_n(m_info=[8, 125 * 50], n_wfs=n_wfs)
filename = "./data/generated_dags/100_0.4_0.8_0.2_1.dot"
machines = Machine.load_n_static_machines(n_machines, network * 125)
wf = Workflow(id_=0, file_path=filename, wf_type="random", machines=machines, add_dummies=True)

# %%
Scheduler.heft(wf.tasks, wf.machines)
wf.set_scheduled(is_scheduled=True)
print(filename)
print(int(wf.wf_len))

# %%
rr = RuinRecreate(wf, machines, ruin_method="random")

# %%
rr_wf, machines = rr.run()
perc = find_perc_diff(wf.wf_len, rr_wf.wf_len)
print(int(rr_wf.wf_len), perc)
print("----------------------------------")
# param.update({'heft': wf.wf_len, 'rr': rr_wf.wf_len, 'perc': perc})
# schedulers.append(param)
