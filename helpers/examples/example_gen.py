from classes.workflow import Workflow
from random import randint
from helpers.examples.example_data import SMALL_EXAMPLE
from classes.machine import Machine, MachineBlueprint, CORE_SPEED
from classes.task import Task, TaskStatus, Edge

N_WORKFLOWS = 3


class Example:
    # @staticmethod
    # def find_best_small_example(run_methods):
    #     best_example = None
    #     while 10000:
    #         schedules, workflows, machines = run_sim(run_methods=run_methods, load_example=True, visuals=False, save_fig=False, show_fig=False)
    #         lowest_shc = min(schedules, key=lambda s: s.get_schedule_len())

    #         if lowest_shc.name.startswith('holes '):
    #             schedules = [s for s in schedules if not s.name.startswith('holes ')]
    #             their_best = min(schedules, key=lambda s: s.get_schedule_len())
    #             for s in schedules:
    #                 diff = abs(lowest_shc.get_schedule_len() - their_best.get_schedule_len())
    #                 if best_example is not None:
    #                     if diff > best_example['diff']:
    #                         best_example = {'workflows': workflows, 'machines': machines, 'schedules': schedules, 'diff': diff}
    #                         lines = [f"Diff = {best_example['diff']}\nOur Method = {lowest_shc.name} len = {lowest_shc.get_schedule_len()}\nTheirs = {their_best.name} len = {their_best.get_schedule_len()}\n"]
    #                         for m in machines:
    #                             lines.append(f'{m.get_blueprint()}\n')
    #                         for wf in workflows:
    #                             lines.append(f'\n========= WORKFLOW-{wf.id} ========= \n')
    #                             for t in wf.tasks:
    #                                 lines.append(f'\t{t.get_blueprint()}\n')
    #                                 for e in t.children_edges:
    #                                     lines.append(f'\t\tEdge({e.weight}, {e.node.id})\n')
    #                                 lines.append('\n')
    #                                 for e in t.parents_edges:
    #                                     lines.append(f'\t\tEdge({e.weight}, {e.node.id})\n')

    #                         with open('find_best_example.txt', "w+") as f:
    #                             f.writelines(lines)
    #                 else:
    #                     best_example = {'workflows': workflows, 'machines': machines, 'schedules': schedules, 'diff': diff}

    #         print(f"{lowest_shc.name} = {lowest_shc.get_schedule_len()}")
    @staticmethod
    def load_all_types(m_info, n_tasks):
        machines = Machine.load_n_static_machines(m_info[0], m_info[1])
        workflows = Workflow.load_all_types_wfs(machines, n=n_tasks)
        return machines, workflows

    @staticmethod
    def load_big_example():
        machines = Machine.load_n_static_machines(4)
        workflows = Workflow.load_random_workflows(machines, n=30)
        return machines, workflows

    @staticmethod
    def load_medium_example():
        machines = Machine.load_n_static_machines(4)
        workflows = Workflow.load_random_workflows(machines, n=10)
        return machines, workflows

    @staticmethod
    def load_small_example():
        machines = [Machine.blueprint_to_machine(MachineBlueprint(m_info[0], m_info[1], m_info[2], CORE_SPEED)) for m_info in SMALL_EXAMPLE['machines']]
        return machines, [
            Workflow.blueprint_to_workflow(
                id_=i,
                tasks=[Task.blueprint_to_task(blp_t) for blp_t in blp_tasks],
                machines=machines
            ) for i, blp_tasks in enumerate(SMALL_EXAMPLE['workflows'])]

    @staticmethod
    def create_random_small_example():
        machines = [Machine.create_random_machine(i) for i in range(2)]
        workflows = []

        for wf_id in range(N_WORKFLOWS):
            tasks = [Task.create_random_task(t_id, wf_id) for t_id in range(3)]
            tasks[0].is_entry = True
            tasks[0].status = TaskStatus.READY
            tasks[2].is_exit = True
            # Task obj is mutable no need to return something
            Example.create_edges_for_example(tasks)
            workflows.append(Workflow(id_=wf_id, machines=machines,
                             tasks=tasks, wf_type="Random", add_dummies=False))
        return workflows, machines

    @staticmethod
    def blueprint_example(workflows, machines):
        return [[t.get_blueprint() for t in wf.tasks] for wf in workflows], [m.get_blueprint() for m in machines]

    @staticmethod
    def re_create_example(workflows, machines):
        blp_tasks, blp_machines = Example.blueprint_example(workflows, machines)
        # Flatten tasks
        blp_tasks = sum(blp_tasks, [])
        machines = [Machine.blueprint_to_machine(blp_m) for blp_m in blp_machines]
        new_workflows = []

        for wf_id in range(len(workflows)):
            tasks = [Task.blueprint_to_task(blp_t) for blp_t in blp_tasks if blp_t.wf_id == wf_id]
            new_workflows.append(Workflow.blueprint_to_workflow(wf_id, tasks, machines))
        return new_workflows, machines

    @staticmethod
    def create_edges_for_example(tasks):
        made_edges = []
        for t in tasks:
            for t2 in tasks:
                if t is t2:
                    continue
                # probap = randint(0, 100)
                if (t.id, t2.id) not in made_edges:
                    weight = randint(1, 20)
                    if t.id < t2.id:
                        t.add_child(weight, t2)
                        t2.add_parent(weight, t)
                    else:
                        t2.add_child(weight, t)
                        t.add_parent(weight, t2)
                    made_edges.append((t.id, t2.id))
