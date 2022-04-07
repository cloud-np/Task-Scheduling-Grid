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


def write_to_excel(schedules, wks, bold, pos):

    if pos is None:
        pos = [2, 0]

    # The image we insert needs at least 20 rows.
    x_offset = pos[0]
    y_offset = pos[1] + 1
    # imgdata = io.BytesIO()
    # fig.savefig(imgdata, format='png')
    # wks.insert_image(s_pos[0], s_pos[1], '', {'image_data': imgdata})

    # The image we insert needs at least 20 rows.
    x_offset = 5
    y_offset = 5

    wks.set_column(0, 50, 20)

    # Headers
    wks.write(x_offset, y_offset, "Heft", bold)
    wks.write(x_offset, y_offset + 1, "RR", bold)
    wks.write(x_offset, y_offset + 2, "Pecentage", bold)
    wks.write(x_offset, y_offset + 3, "n", bold)
    wks.write(x_offset, y_offset + 4, "Fat", bold)
    wks.write(x_offset, y_offset + 5, "density", bold)
    wks.write(x_offset, y_offset + 6, "regularity", bold)
    wks.write(x_offset, y_offset + 7, "jump", bold)

    for s in schedules:
        x_offset += 1
        # Heft
        wks.write(x_offset, y_offset, s['heft'])
        # RR
        wks.write(x_offset, y_offset + 1, int(s['rr']))
        # perc
        wks.write(x_offset, y_offset + 2, s['perc'])
        # n
        wks.write(x_offset, y_offset + 3, int(s['n']))
        # fat
        wks.write(x_offset, y_offset + 4, s['fat'])
        # density
        wks.write(x_offset, y_offset + 5, s['density'])
        # regularity
        wks.write(x_offset, y_offset + 6, s['regularity'])
        # jump
        wks.write(x_offset, y_offset + 7, s['jump'])


random.seed(0)

# %%
ss = []
n_machines = 4
network = 500

# machines, workflows = ExampleGen.load_n(m_info=[8, 125 * 50], n_wfs=n_wfs)
minalpha = 20
maxalpha = 50
n = [50, 100, 200, 300, 400]
fat = [0.1, 0.4, 0.8]
density = [0.2, 0.8]
regularity = [0.2, 0.8]
jump = [1, 2, 4]

keys = ['n', 'fat', 'density', 'regularity', 'jump']
values = [n, fat, density, regularity, jump]

workbook = xlsxwriter.Workbook('heft_rr_sim.xlsx')
wks = workbook.add_worksheet('Runned Simulation Info')
bold = workbook.add_format({'bold': True})

schedulers = []
for v in product(*values):
    param = dict(zip(keys, v))
    filename = "./data/generated_dags/{}_{}_{}_{}_{}.dot".format(param['n'], param['fat'],
                                                                 param['density'],
                                                                 param['regularity'],
                                                                 param['jump'])
    param = dict(zip(keys, v))
    machines = Machine.load_n_static_machines(n_machines, network * 125)
    wf = Workflow(id_=0, file_path=filename, wf_type="random", machines=machines, add_dummies=True)
    # machines = Machine.load_n_static_machines(n_machines, network * 125)
    # wf = Workflow(id_=0, file_path="./data/generated_dags/100_0.8_0.2_0.8_2.dot", wf_type="random", machines=machines, add_dummies=True)
    # wf = Workflow(id_=0, file_path="./data/epigenomics/epigenomics_100.json", wf_type="epigenomics", machines=machines, add_dummies=True)
    # print(f"n-wfs: {n} machines: {n_machines}  network: {network}")

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
    param.update({'heft': wf.wf_len, 'rr': rr_wf.wf_len, 'perc': perc})
    schedulers.append(param)

write_to_excel(schedulers, wks, bold, [0, 0])
workbook.close()
