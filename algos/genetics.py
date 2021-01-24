from algos.schedule_tasks import schedule_genetic_wf
from copy import deepcopy
from colorama import Fore, Back
from random import randint, choices
from classes.Workflow import Workflow

POPULATION = 10
DEADLINE = 22


# Maybe a bit slower to return a bool instead of doing the one
# line here but its more readable this way and maybe maintainable.
# def try_adding_task(task, machines):
#     # Shall we skip this check? Is it correct? Not sure from looking into the paper..
#     if task.status == TaskStatus.READY:
#         machine, times = pick_machine_for_task(task, machines)
#         schedule_task({'start': times[0], 'end': times[1]}, task, machine)
#         return True
#     return False


# This works only if we use a specific fitness function
# This should work only because we want every workflow to have
# at least below 1 value the reason being we have a deadline constrain
def select_parents_with_specific_fitness_function(workflows):
    return choices(workflows, weights=[1 - fitness_function(wf) for wf in workflows], k=10)


# b-level = upwards rank
# t-level = downwards rank
def bga():
    wf = Workflow(id_=0, deadline=DEADLINE, example_data='deadline-constrain')
    initial_population = list()
    initial_population.append(wf)
    # copied_machines = deepcopy(wf.machines)

    # TODO: Because we are sorting the tasks we actually change
    #       their position. Maybe implement a dictionary e.g:
    #       sorted_task = { main_table_id: 12, upward_rank: 109.12 }
    #       also how do you add randomly the tasks later on...
    # Calc the b-level of all tasks.
    # Instead of making a copy of the Task class we simply use a dict to keep track some values
    copied_tasks = [{"t_id": task.id,
                     "start": -1,
                     "end": -1,
                     "up_rank": task.up_rank,
                     "machine_id": -1,
                     "slowest_parent": {"com_time": -1, "parent_id": -1}} for task in wf.tasks]
    copied_tasks.sort(reverse=True, key=lambda s_task: s_task["up_rank"])
    # Create the initial population and the first individual based his tasks b-level.
    # schedule_genetic_wf(copied_tasks, wf.tasks, copied_machines, "random")
    # schedule_genetic_wf(wf.tasks, wf.machines, "random")
    # schedule_b_level_wf(sorted_tasks, wf.machines)

    # Initial Population created
    # for i in range(1, population):
    #     initial_population.append(workflow(id_=i, deadline=deadline, machines=copy(copied_machines)))
    #     schedule_random_wf(initial_population[i].tasks, initial_population[i].machines)

    population = initial_population
    i = 0
    while i < 1:
        # More clean/readable way for sure
        # if fitness_function(wf) < 1:
        #     next_population.append(wf)
        # ...
        parents = select_parents_with_specific_fitness_function(population)
#        for wf in parents:
        single_point_crossover(parents[0], parents[1])

        i += 1
#        population = list()

    # Debugging
    # select_parents(initial_population)
    # for wf in initial_population:
    #     print(f"w[{wf.id}] fitness: {wf.fitness} ")
    # for i in range(20):
    #     ep = select_parents(initial_population)
    #     included = [0 for _ in range(10)]
    #     for wf in ep:
    #         included[wf.id] += 1
    #     for x in range(0, len(included)):
    #         print(f"w[{x}] - {Fore.MAGENTA}{included[x]}{Fore.RESET}", end=" ")
    #     print()
    return initial_population


def single_point_crossover(wf, wf2):

    wf_map = wf.get_machines_mapping()
    wf2_map = wf2.get_machines_mapping()
    if len(wf_map) == 0 or len(wf2_map) == 0:
        print("empty wf")

    # Make the actual crossover
    point = randint(1, len(wf_map))
    machine_map = wf_map[0:point] + wf2_map[point:]

    new_tasks = deepcopy(wf.tasks)
    new_machines = deepcopy(wf.machines)

    # TODO: This probably can get better with if you
    #       change the i to start from "point" which
    #       would make sense.
    for i in range(len(machine_map)):
        # # Get machines from indexes/ids
        # machine = wf.get_machine_from_index(machine_map[i])
        # old_machine = wf.get_machine_from_index(new_tasks[i].machine_id)
        # Update the schedule basically by changing the machine for a task
        new_tasks[i].change_machine(machine_map[i])

    for task in new_tasks:
        print(task)
    # Make the new workflow with what we made above


def fitness_function(wf):
    if wf.deadline is None:
        raise Exception(f"Please set a deadline for the given workflow! id = {wf.id}")
    wf.fitness = wf.get_workflow_len() / wf.deadline
    return wf.fitness


