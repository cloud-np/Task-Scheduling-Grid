from classes.machine import Machine
from colorama import Fore, Back
from algos.paper_2011_algos.paper_method import Paper2011
from classes.workflow import Workflow
from classes.scheduler import Scheduler

if __name__ == "__main__":

    machines = Machine.load_4_machines()
    workflows = Workflow.load_example_workflows(machines=machines, n=10)
    Paper2011(workflows, machines)
