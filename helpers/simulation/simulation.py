from matplotlib.pyplot import savefig
from typing import List
from classes.machine import Machine
from colorama import Fore, Back
from classes.workflow import Workflow
from classes.scheduler import Scheduler
from helpers.checker import schedule_checker
from helpers.visuals.visualize import Visualizer
import xlsxwriter
import numpy as np
import matplotlib.pyplot as plt
import io


# TODO One idea is to pass schedule functions to the
# run() method of the Schedule obj. This sounds a bit cleaner.
# than making it pick a the correct function as init time.
def run_sim(n, run_methods, visuals=False, save_fig=False, show_fig=True, save_sim=False):
    workflows = []
    slowest_machines = []
    schedules = []
    fig = None
    for method in run_methods:
        machines = Machine.load_4_machines()
        workflows = Workflow.load_example_workflows(machines=machines, n=n)
        schedule = Scheduler(name=method['name'], workflows=workflows, machines=machines, time_types=method.get(
            "time_types"), fill_type=method["fill_type"], priority_type=method.get("priority_type"))

        schedule.run()
        schedule.info()

        slowest_machines.append({"machine": schedule.get_slowest_machine(), "method_used": schedule.method_used_info(concise=True)})

        schedules.append(schedule)

    if visuals is True:
        fig = Visualizer.compare_schedule_len(slowest_machines, len(
            workflows), save_fig=save_fig, show_fig=show_fig)
        if save_sim:
            for s in schedules:
                s.save_output_to_file()
    return schedules, fig


def run_n_sims(ns, run_methods, visuals=False, save_fig=False, show_fig=False, save_sim=False):
    for n in ns:
        schedules, fig = run_sim(n, run_methods, visuals, save_fig, show_fig, save_sim)
        print("Finished simulating for n = ", n)


def run_save_n_sims_to_excel(ns, run_methods):
    workbook = xlsxwriter.Workbook('simulation_info.xlsx')
    wks = workbook.add_worksheet('Runned Simulation Info')
    bold = workbook.add_format({'bold': True})
    for i, n in enumerate(ns):
        schedules, fig = run_sim(n, run_methods, visuals=True, save_fig=False, show_fig=False, save_sim=False)
        print("Finished simulating for n = ", n)

        write_to_excel(schedules, fig, wks, bold, s_pos=[2 + i * 40, 0])
    workbook.close()


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
