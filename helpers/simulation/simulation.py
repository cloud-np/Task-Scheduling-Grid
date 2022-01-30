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
from helpers.examples.example_gen import ExampleGen
from algos.optimizer import optimize_schedule
from helpers.utils import find_perc_diff
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
                                                      data=ExampleGen.re_create_example(workflows, machines),
                                                      time_types=method.get("time_types"),
                                                      fill_method=method["fill_type"], priority_type=method.get("priority_type")) for method in run_methods]

    def run_paper_example(self, count):
        for s in self.schedulers:
            Simulation.fake_schedule_fist_workflow(s.machines, s.workflows)
            s.run_example()
        return self.schedulers

    def run(self):
        for s in self.schedulers:
            s.run()
            # if self.save_sim:
            #     s.save_output_to_file()

        # print("-------TOTAL MAKESPAN-------")
        # their_min_s = min(self.get_their_schedulers(), key=lambda s: s.schedule_len)
        # print(their_min_s)
        our_min_s = min(self.get_our_schedulers(), key=lambda s: s.schedule_len)
        # # our_min_s.view_machine_holes()
        # ordered_our_min_s, is_better = optimize_schedule(self.workflows, self.machines, our_min_s)
        # if self.save_sim:
        #     our_min_s.save_output_to_file()
        # their_min_s.save_output_to_file()
        # print(our_min_s)
        # print(f"DIFF: {their_min_s.schedule_len - our_min_s.schedule_len} \n\n")
        # if is_better:
        #     self.schedulers.append(our_min_s)
        # print(min_s)
        if self.save_sim:
            # min_s = min(self.schedulers, key=lambda s: s.schedule_len)

            our_min_s = min(self.get_our_schedulers(), key=lambda s: s.schedule_len)
            return self.get_our_schedulers()
            # their_min_s = min(self.get_their_schedulers(), key=lambda s: s.schedule_len)
            # c1 = self.get_c1()
            # return [our_min_s, ordered_our_min_s, their_min_s, c1]
            # self.save_sim_stats(min_s)
        if self.show_machines:
            Visualizer.visualize_machines(our_min_s.machines)
            # Visualizer.visualize_machines(their_min_s.machines)
            # print(their_min_s)
            # if min_s is our_min_s:
            #     Visualizer.visualize_machines(our_min_s.machines)
            #     Visualizer.visualize_machines(their_min_s.machines)
            # print("-------AVG MAKESPAN-------")
            # our_min_s = min(self.get_our_schedulers(), key=lambda s: s.avg_workflow_makespan)
            # print(our_min_s)
            # their_min_s = min(self.get_their_schedulers(), key=lambda s: s.avg_workflow_makespan)
            # print(their_min_s)
        if self.visuals is True:
            # Schedule len
            Visualizer.compare_data([s.get_slowest_machine().time_on_machine for s in self.schedulers], [s.method_used_info(concise=True) for s in self.schedulers], len(self.workflows), save_fig=self.save_fig, show_fig=self.show_fig)
            # Holes filled
            # Visualizer.compare_data([s.get_holes_filled() for s in self.schedulers], [s.method_used_info(concise=True) for s in self.schedulers], len(self.workflows), save_fig=self.save_fig, show_fig=self.show_fig)
            # Avg wf makespan
            # Visualizer.compare_data([s.avg_workflow_makespan for s in self.schedulers], [s.method_used_info(concise=True) for s in self.schedulers], len(self.workflows), save_fig=self.save_fig, show_fig=self.show_fig)
        return self.schedulers

    def get_our_schedulers(self):
        return [s for s in self.schedulers if (s.name.startswith("crit") or s.name.startswith("holes "))]

    def get_their_schedulers(self):
        return [s for s in self.schedulers if (s.name.startswith("holes2011"))]

    def get_c1(self):
        return [s for s in self.schedulers if (s.name.startswith("c1"))][0]

    def save_sim_stats(self, min_s):
        out_f = f'sim/bw_{int(self.machines[0].network_kbps / 125)}_wfs_{len(self.workflows)}_machines_{len(self.machines)}_best.txt'
        lines = []
        our_min_s = min(self.get_our_schedulers(), key=lambda s: s.schedule_len)
        their_min_s = min(self.get_their_schedulers(), key=lambda s: s.schedule_len)
        c1 = self.get_c1()
        for s in [our_min_s, their_min_s, c1]:
            info = [f"{s.name}\t", f"{int(s.schedule_len)}\t", f"{s.machines_util_avg_perc}\t", f"{int(s.avg_workflow_makespan)}\t", f"{s.get_holes_filled()}\t", f"{int(s.get_holes_time_saved())}\t", f"{int(s.machines[0].network_kbps / 125)}\t", f"{len(s.workflows)}\t", f"{len(s.machines)}\n"]
            lines.append(info)
        # lines.append([f"{our_min_s.name} vs c1 perc diff: {find_perc_diff(our_min_s.schedule_len, c1.schedule_len)}\n"])
        # lines.append([f"Best Schedule: {min_s.name}\n"])
        lines = sum(lines, [])
        with open(out_f, "+a") as f:
            f.writelines(lines)

    def save_sim_info(self, min_s):
        # out_f = f'{len(self.workflows)}_.txt'
        lines = []
        for s in self.schedulers:
            info = [f"{s.name}\t", f"{int(s.schedule_len)}\t", f"{s.machines_util_avg_perc}\t", f"{int(s.avg_workflow_makespan)}\t", f"{s.get_holes_filled()}\t", f"{int(s.get_holes_time_saved())}\t", f"{int(s.machines[0].network_kbps / 125)}\t", f"{len(s.workflows)}\t", f"{len(s.machines)}\n"]
            lines.append(info)
        lines = sum(lines, [])
        # with open(out_f, "+a") as f:
        #     f.writelines(lines)
        return lines

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


def save_sims_to_excel(schedulers, num_wfs):
    workbook = xlsxwriter.Workbook(f'sim-{num_wfs}_EST-EFT.xlsx')
    wks = workbook.add_worksheet('Runned Simulation Info')
    bold = workbook.add_format({'bold': True})
    write_to_excel(schedulers, wks, bold, s_pos=[2, 0])
    # for i, n in enumerate(ns):
    #     schedules = run_sim(n, run_methods, visuals=True, save_fig=False, show_fig=False, save_sim=False)
    #     print("Finished simulating for n = ", n)

    #     write_to_excel(schedules, wks, bold, s_pos=[2 + i * 40, 0])
    workbook.close()


def write_excel(schedules: List[Scheduler], wks, bold, s_pos: List[int] = [2, 0]):

    # imgdata = io.BytesIO()
    # fig.savefig(imgdata, format='png')
    # wks.insert_image(s_pos[0], s_pos[1], '', {'image_data': imgdata})

    # The image we insert needs at least 20 rows.
    x_offset = s_pos[0]
    y_offset = s_pos[1] + 1

    wks.set_column(0, 50, 20)

    # Headers
    wks.write(x_offset, y_offset, "Method Name", bold)
    wks.write(x_offset, y_offset + 1, "Total Makespan", bold)
    wks.write(x_offset, y_offset + 2, "Avg Machine Util", bold)
    wks.write(x_offset, y_offset + 3, "Avg Wf Makespan", bold)
    wks.write(x_offset, y_offset + 4, "Holes Filled", bold)
    wks.write(x_offset, y_offset + 5, "Hole Saved Time", bold)
    wks.write(x_offset, y_offset + 6, "Bandwidth", bold)
    wks.write(x_offset, y_offset + 7, "Workflows", bold)
    wks.write(x_offset, y_offset + 8, "Machines", bold)

    for s in schedules:
        x_offset += 1
        # name
        wks.write(x_offset, y_offset, f"{s.method_used_info()}")

        # schedule len
        wks.write(x_offset, y_offset + 1, int(s.schedule_len))

        # avg machine util
        wks.write(x_offset, y_offset + 2, s.machines_util_avg_perc)

        # avg workflow makespan
        wks.write(x_offset, y_offset + 3, int(s.avg_workflow_makespan))

        # holes filled
        wks.write(x_offset, y_offset + 4, s.get_holes_filled())

        # time saved by holes
        wks.write(x_offset, y_offset + 5, int(s.get_holes_time_saved()))

        # bandwidth
        wks.write(x_offset, y_offset + 6, int(s.machines[0].network_kbps / 125))

        # workflows
        wks.write(x_offset, y_offset + 7, len(s.workflows))

        # machines
        wks.write(x_offset, y_offset + 8, len(s.machines))


def write_to_excel(schedules: List[Scheduler], wks, bold, s_pos: List[int] = [2, 0]):

    # imgdata = io.BytesIO()
    # fig.savefig(imgdata, format='png')
    # wks.insert_image(s_pos[0], s_pos[1], '', {'image_data': imgdata})

    # The image we insert needs at least 20 rows.
    x_offset = s_pos[0]
    y_offset = s_pos[1] + 1

    wks.set_column(0, 50, 20)

    # Headers
    wks.write(x_offset, y_offset, "Method Name", bold)
    wks.write(x_offset, y_offset + 1, "Total Makespan", bold)
    wks.write(x_offset, y_offset + 2, "Avg Machine Util", bold)
    wks.write(x_offset, y_offset + 3, "Avg Wf Makespan", bold)
    wks.write(x_offset, y_offset + 4, "Holes Filled", bold)
    wks.write(x_offset, y_offset + 5, "Hole Saved Time", bold)
    wks.write(x_offset, y_offset + 6, "Bandwidth", bold)
    wks.write(x_offset, y_offset + 7, "Workflows", bold)
    wks.write(x_offset, y_offset + 8, "Machines", bold)

    for s in schedules:
        x_offset += 1
        # name
        wks.write(x_offset, y_offset, f"{s.method_used_info()}")

        # schedule len
        wks.write(x_offset, y_offset + 1, int(s.schedule_len))

        # avg machine util
        wks.write(x_offset, y_offset + 2, s.machines_util_avg_perc)

        # avg workflow makespan
        wks.write(x_offset, y_offset + 3, int(s.avg_workflow_makespan))

        # holes filled
        wks.write(x_offset, y_offset + 4, s.get_holes_filled())

        # time saved by holes
        wks.write(x_offset, y_offset + 5, int(s.get_holes_time_saved()))

        # bandwidth
        wks.write(x_offset, y_offset + 6, int(s.machines[0].network_kbps / 125))

        # workflows
        wks.write(x_offset, y_offset + 7, len(s.workflows))

        # machines
        wks.write(x_offset, y_offset + 8, len(s.machines))
