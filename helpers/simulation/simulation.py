from matplotlib.pyplot import savefig
from typing import List
from classes.machine import Machine
from colorama import Fore, Back
from classes.workflow import Workflow
from classes.scheduler import Scheduler
from helpers.checker import schedule_checker
from helpers.visuals.visualize import Visualizer
from helpers.examples.example_gen import Example
import xlsxwriter
import numpy as np
import matplotlib.pyplot as plt
import io


class Simulation:
    def __init__(self, run_methods, machines, workflows, visuals=False, save_fig=False, show_fig=True, save_sim=False, show_machines=False):
        self.run_methods: List[dict] = run_methods
        self.machines: List[Machine] = machines
        self.workflows: List[Workflow] = workflows
        self.visuals: bool = visuals
        self.save_fig: bool = save_fig
        self.show_machines: bool = show_machines
        self.show_fig: bool = show_fig
        self.save_sim: bool = save_sim
        self.schedulers: List[Scheduler] = [Scheduler(method['name'],
                                                      data=Example.re_create_example(workflows, machines),
                                                      time_types=method.get("time_types"),
                                                      fill_method=method["fill_type"], priority_type=method.get("priority_type")) for method in run_methods]

    def run(self):
        slowest_machines = []
        for s in self.schedulers:
            s.run()
            s.info()
            # print(s.get_holes_filled())
            slowest_machines.append({
                "machine": s.get_slowest_machine(),
                "method_used": s.method_used_info(concise=True)})
            if self.save_sim:
                s.save_output_to_file()
            if self.show_machines:
                Visualizer.visualize_machines(s.machines)

        if self.visuals is True:
            Visualizer.compare_data([sm['machine'].time_on_machine for sm in slowest_machines], [sm['method_used'] for sm in slowest_machines], len(self.workflows), save_fig=self.save_fig, show_fig=self.show_fig)
            # Visualizer.compare_data([s.get_whole_idle_time() for s in self.schedulers], [sm['method_used'] for sm in slowest_machines], len(self.workflows), save_fig=self.save_fig, show_fig=self.show_fig)

# def run_save_n_sims_to_excel(ns, run_methods):
#     workbook = xlsxwriter.Workbook('simulation_info.xlsx')
#     wks = workbook.add_worksheet('Runned Simulation Info')
#     bold = workbook.add_format({'bold': True})
#     for i, n in enumerate(ns):
#         schedules, fig = run_sim(
#             n, run_methods, visuals=True, save_fig=False, show_fig=False, save_sim=False)
#         print("Finished simulating for n = ", n)

#         write_to_excel(schedules, fig, wks, bold, s_pos=[2 + i * 40, 0])
#     workbook.close()


def write_to_excel(schedules: List[Scheduler], fig, wks, bold, s_pos: List[int] = [2, 0]):

    infos = [s.get_scheduled_info() for s in schedules]
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format='png')
    wks.insert_image(s_pos[0], s_pos[1], '', {'image_data': imgdata})

    # The image we insert needs at least 20 rows.
    x_offset = s_pos[0] + 20
    y_offset = s_pos[1] + 1

    wks.set_column(0, 50, 20)

    # Headers
    wks.write(x_offset, y_offset, "Method Name", bold)
    wks.write(x_offset, y_offset + 1, "Holes Filled", bold)
    wks.write(x_offset, y_offset + 2, "Time Saved", bold)
    wks.write(x_offset, y_offset + 3, "Length", bold)

    for i, info in enumerate(infos):
        # name
        x_offset += 1
        name = info[0].split()
        wks.write(x_offset, y_offset, f"{name[0]} {name[1]}")

        # holes filled
        wks.write(x_offset, y_offset + 1, info[1].split("Holes Filled ")[1])

        # time saved
        wks.write(x_offset, y_offset + 2, int(float(info[2])))

        # schedule_len
        wks.write(x_offset, y_offset + 3,
                  int(float(info[4].split("TOTAL LEN: ")[1])))
