from matplotlib.pyplot import savefig
from collections import defaultdict
from typing import List
from classes.machine import Machine, Hole
from classes.task import TaskBlueprint
from colorama import Fore, Back
from classes.workflow import Workflow
from classes.scheduler import Scheduler, get_fill_method, FillMethod
from helpers.checker import schedule_checker
from helpers.visuals.visualize import Visualizer
from random import randint
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

    @staticmethod
    def load_paper_example(count):
        machines, workflows = Example.load_small_random()
        run_methods = [
            {"name": "holes FASTEST-FIT", "time_types": ["EFT", "EFT"], "fill_type": "FASTEST-FIT"},
            {"name": "holes BEST-FIT", "time_types": ["EFT", "EFT"], "fill_type": "BEST-FIT"},
            {"name": "holes FIRST-FIT", "time_types": ["EFT", "EFT"], "fill_type": "FIRST-FIT"},
            {"name": "holes WORST-FIT", "time_types": ["EFT", "EFT"], "fill_type": "WORST-FIT"},
        ]
        schedulers: List[Scheduler] = [Scheduler(method['name'], data=Example.re_create_example(workflows, machines), time_types=method.get("time_types"), fill_method=method["fill_type"], priority_type=method.get("priority_type")) for method in run_methods]
        for s in schedulers:
            Simulation.fake_schedule_fist_workflow(s.machines, s.workflows)
            s.example()
            avg_makespan = sum(wf.wf_len for wf in s.workflows) / s.n_wfs
            print(f"{s.fill_method} {avg_makespan}")
            for t in s.workflows[1].tasks:
                print(t)
        print(f" iter: {count}")

        min_s = min(schedulers, key=lambda s: s.avg_workflow_makespan)
        for s in schedulers:
            if s.fill_method == FillMethod.FIRST_FIT:
                fs = s
            if s.fill_method == FillMethod.FASTEST_FIT:
                frs = s
            if s.fill_method == FillMethod.BEST_FIT:
                bs = s
            if s.fill_method == FillMethod.WORST_FIT:
                ws = s

        if min_s.fill_method == FillMethod.WORST_FIT:
            all_avg = (fs.avg_workflow_makespan, bs.avg_workflow_makespan, frs.avg_workflow_makespan)
            for m in min_s.machines:
                ok = False
                for t in m.tasks:
                    if t.wf_id == 1:
                        ok = True
                if ok is False:
                    return False
            if min_s.avg_workflow_makespan not in all_avg:
                print(min_s.fill_method)
                Visualizer.visualize_machines(min_s.machines)
                return True
            else:
                return False
        else:
            return False
        # if min_s.fill_method == FillMethod.WORST_FIT:
        Visualizer.visualize_machines(min_s.machines)
        #     return True
        # return False
        # if self.visuals is True:
        #     Visualizer.compare_data([s.get_slowest_machine().time_on_machine for s in self.schedulers], [s.method_used_info(concise=True) for s in self.schedulers], len(self.workflows), save_fig=self.save_fig, show_fig=self.show_fig)

    @staticmethod
    def fake_schedule_fist_workflow(machines, workflows):
        wf = workflows[0]

        t_0 = wf.tasks[0]
        t_1 = wf.tasks[1]
        t_2 = wf.tasks[2]
        t_3 = wf.tasks[3]
        t_4 = wf.tasks[4]
        t_5 = wf.tasks[5]
        t_6 = wf.tasks[6]
        t_7 = wf.tasks[7]

        m_0 = machines[0]
        m_1 = machines[1]

        t_2.set_times(37.5, 87.5)
        t_6.set_times(156.5, 176.5)
        m_0.holes.add(Hole(0, t_2.start, t_6.start - 0))
        m_0.holes.add(Hole(t_2.end, t_6.start, t_6.start - t_2.end))

        t_7.set_times(270, 300)
        m_0.holes.add(Hole(t_6.end, t_7.start, t_7.start - t_6.end))
        m_0.time_on_machine = t_7.end

        t_0.set_times(0, 34.5)
        t_1.set_times(34.5, 80.5)
        t_3.set_times(119.5, 131.5)
        m_1.holes.add(Hole(t_1.end, t_3.start, t_3.start - t_1.end))

        t_4.set_times(150, 152)
        m_1.holes.add(Hole(t_3.end, t_4.start, t_4.start - t_3.end))

        t_5.set_times(174.5, 219)
        m_1.holes.add(Hole(t_4.end, t_5.start, t_5.start - t_4.end))
        m_1.time_on_machine = t_5.end

        for t in [t_2, t_6, t_7]:
            machines[0].tasks.append(t)
            t.machine_id = 0
        for t in [t_0, t_1, t_3, t_4, t_5]:
            machines[1].tasks.append(t)
            t.machine_id = 1

        # make a wf_len for the workflow
        workflows.wf_len = t_7.end

    def run(self):
        # slowest_machines = []
        for s in self.schedulers:
            s.run()
            # print(s.get_holes_filled())
            if self.save_sim:
                s.save_output_to_file()
            # if s.fill_method == FillMethod.WORST_FIT:
            #     ss = s

        min_s = min(self.schedulers, key=lambda s: s.workflows_avg_schedule_len)
        min_s.info()

        if self.show_machines:
            Visualizer.visualize_machines(min_s.machines)
        if self.visuals is True:
            Visualizer.compare_data([s.get_slowest_machine().time_on_machine for s in self.schedulers], [s.method_used_info(concise=True) for s in self.schedulers], len(self.workflows), save_fig=self.save_fig, show_fig=self.show_fig)
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
