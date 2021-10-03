from classes.workflow import Workflow
from random import randint
from helpers.examples.example_data import SMALL_EXAMPLE
from classes.machine import Machine, MachineBlueprint, CORE_SPEED
from classes.task import Task, TaskStatus, Edge, TaskBlueprint
from random import randint, seed

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
    def load_small_random():
        machines = [Machine.blueprint_to_machine(MachineBlueprint(m_info[0], m_info[1], m_info[2], CORE_SPEED, m_info[3])) for m_info in SMALL_EXAMPLE['machines']]

        a_b = randint(1, 100)
        a_c = randint(1, 100)
        a_d = randint(1, 100)
        b_e = randint(1, 100)
        c_e = randint(1, 100)
        d_e = randint(1, 100)
        e_f = randint(1, 100)
        e_g = randint(1, 100)
        f_h = randint(1, 100)
        g_h = randint(1, 100)
        blp_worklows = [
            [
                TaskBlueprint(0, 0, 'T-A', randint(1, 100), [{"weight": a_b, "name": 'T-B'}, {"weight": a_c, "name": 'T-C'}, {"weight": a_d, "name": 'T-D'}], [], TaskStatus.READY, True, False),
                TaskBlueprint(1, 0, 'T-B', randint(1, 100), [{"weight": b_e, "name": 'T-E'}], [{"weight": a_b, "name": 'T-A'}], TaskStatus.UNSCHEDULED, False, False),
                TaskBlueprint(2, 0, 'T-C', randint(1, 100), [{"weight": c_e, "name": 'T-E'}], [{"weight": a_c, "name": 'T-A'}], TaskStatus.UNSCHEDULED, False, False),
                TaskBlueprint(3, 0, 'T-D', randint(1, 100), [{"weight": d_e, "name": 'T-E'}], [{"weight": a_d, "name": 'T-A'}], TaskStatus.UNSCHEDULED, False, False),
                TaskBlueprint(4, 0, 'T-E', randint(1, 100), [{"weight": e_f, "name": 'T-F'}, {"weight": e_g, "name": 'T-G'}], [{"weight": b_e, "name": 'T-B'}, {"weight": c_e, "name": 'T-C'}, {"weight": d_e, "name": 'T-D'}], TaskStatus.UNSCHEDULED, False, False),
                TaskBlueprint(5, 0, 'T-F', randint(1, 100), [{"weight": f_h, "name": 'T-H'}], [{"weight": e_f, "name": 'T-E'}], TaskStatus.UNSCHEDULED, False, False),
                TaskBlueprint(6, 0, 'T-G', randint(1, 100), [{"weight": g_h, "name": 'T-H'}], [{"weight": e_g, "name": 'T-E'}], TaskStatus.UNSCHEDULED, False, False),
                TaskBlueprint(7, 0, 'T-H', randint(1, 100), [], [{"weight": f_h, "name": 'T-F'}, {"weight": g_h, "name": 'T-G'}], TaskStatus.UNSCHEDULED, False, True),
            ]
        ]

        _a_t_b = randint(1, 100)
        _b_t_c = randint(1, 100)
        _c_t_d = randint(1, 100)
        blp_worklows.append([
            TaskBlueprint(0, 1, 'T-A', randint(1, 100), [{"weight": _a_t_b, "name": 'T-B'}], [], TaskStatus.READY, True, False),
            TaskBlueprint(1, 1, 'T-B', randint(1, 100), [{"weight": _b_t_c, "name": 'T-C'}], [{"weight": _a_t_b, "name": 'T-A'}], TaskStatus.UNSCHEDULED, False, False),
            TaskBlueprint(2, 1, 'T-C', randint(1, 100), [{"weight": _c_t_d, "name": 'T-D'}], [{"weight": _b_t_c, "name": 'T-B'}], TaskStatus.UNSCHEDULED, False, False),
            TaskBlueprint(3, 1, 'T-D', randint(1, 100), [], [{"weight": _c_t_d, "name": 'T-C'}], TaskStatus.UNSCHEDULED, False, True),
        ])
        return machines, [Workflow.blueprint_to_workflow(
            id_=i,
            tasks=[Task.blueprint_to_task(blp_t) for blp_t in blp_tasks],
            machines=machines
        ) for i, blp_tasks in enumerate(blp_worklows)]

    @staticmethod
    def load_small_example(best_of='workflows'):
        machines = [Machine.blueprint_to_machine(MachineBlueprint(m_info[0], m_info[1], m_info[2], CORE_SPEED, m_info[3])) for m_info in SMALL_EXAMPLE['machines']]
        ab = randint(1, 100)
        ac = randint(1, 100)
        bd = randint(1, 100)
        cd = randint(1, 100)
        # SMALL_EXAMPLE[best_of].append([
        #     # TaskBlueprint(0, 1, "T-A", randint(1, 100), [{'weight': ab, 'name': 'T-B'}, {'weight': ac, 'name': 'T-C'}], [], 1, True, False),
        #     # TaskBlueprint(1, 1, "T-B", randint(1, 100), [{'weight': bd, 'name': 'T-D'}], [{'weight': ab, 'name': 'T-A'}], 0, False, False),
        #     # TaskBlueprint(2, 1, "T-C", randint(1, 100), [{'weight': cd, 'name': 'T-D'}], [{'weight': ac, 'name': 'T-A'}], 0, False, False),
        #     # TaskBlueprint(3, 1, "T-D", randint(1, 100), [], [{'weight': bd, 'name': 'T-B'}, {'weight': cd, 'name': 'T-C'}], 0, False, True),
        # ])
        return machines, [
            Workflow.blueprint_to_workflow(
                id_=i,
                tasks=[Task.blueprint_to_task(blp_t) for blp_t in blp_tasks],
                machines=machines
            ) for i, blp_tasks in enumerate(SMALL_EXAMPLE[best_of])]

    @staticmethod
    def load_small_example1(best_of='workflows'):
        machines = [Machine.blueprint_to_machine(MachineBlueprint(m_info[0], m_info[1], m_info[2], CORE_SPEED, m_info[3])) for m_info in SMALL_EXAMPLE['machines']]
        return machines, [
            Workflow.blueprint_to_workflow(
                id_=i,
                tasks=[Task.blueprint_to_task(blp_t) for blp_t in blp_tasks],
                machines=machines
            ) for i, blp_tasks in enumerate(SMALL_EXAMPLE[best_of])]

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
