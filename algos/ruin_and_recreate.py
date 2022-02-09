from classes.workflow import Workflow
from typing import List
from classes.machine import Machine


class Solution:
    def __init__(self, workflow):
        self.workflow = workflow
        # In this case the id of a task is unique since we don't have other
        # workflows. So its enough to use the id of the task as the key.
        self.tasks_order: List[int] = [t.id for t in sorted(self.workflow.tasks, key=lambda x: x.start)]


class RuinRecreate:

    def __init__(self, og_workflow: Workflow, og_machines: List[Machine], ruin_method="random"):
        self.og_solution = Solution(og_workflow)
        self.og_workflow: Workflow = og_workflow
        self.og_machines: List[Machine] = og_machines
        self.ruin_method: str = ruin_method

        # Find the part you want to ruin

        # Ruin the part
        # self.__ruin()

    def run(self):
        self.__ruin()
        # self.__recreate()
        ...

    def __copy_workflow_and_machines(self):
        machines_copy = [Machine.blueprint_to_machine(m.get_blueprint()) for m in self.og_machines]
        tasks = [Task.blueprint_to_task(t.get_blueprint()) for t in self.og_workflow.tasks]
        workflow_copy = Workflow.blueprint_to_workflow(self.og_workflow.id, self.og_workflow.tasks, self.og_workflow.machines)

    def __ruin(self):
        time_interval = (10, 30)
        ...

    def __recreate(self):
        ...
