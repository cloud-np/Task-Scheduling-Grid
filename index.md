## Overview
This project tries to solve the problem of task scheduling of multiple workflows in a grid. Which is a NP-Problem.
Below we gonna look into details some of the algorithms used to solve this problem. (later on we gonna describe the problem better as well)

## Single Workflow Scheduling

Below we see some popular single workflow scheduling algorithms.

### HEFT
Heterogeneous-Earliest-Finish-Time (HEFT).

The HEFT algorithm has 2 major phases: 
1. Task prioritizing
2. Processor selection

With that in mind we calculate the **task.up_rank** property of the tasks and we sort them based of that value.
Then we pick the machine for each task that give the best **earliest finish time**.


```python
def heft(tasks: List[Task], machines: List[Machine]):
  # Phase 1
  calculate_upward_ranks(tasks)
  
  # Sort the tasks based of the up_rank
  tasks.sort(key=lambda task: task.up_rank, reverse=True)
  
  # Phase 2
  schedule_tasks_with_EFT(tasks, machines)
```
instead of using simple the **task.up_rank** property. It uses the following:
```python
task.priority = task.up_rank + task.down_rank
```
### CPOP
Critical-Path-on-a-Processor (CPOP).

Here the CPOP algorithm we need to find the critical path.

• First we need to calculate the priority of each task. Which means we need to 
calculate both **up_rank** and **down_rank** of each task before we procceed.
```python
def create_critical_path(workflow):
        # Calculate downward and upward ranks
        calculate_upward_ranks(workflow.tasks)
        calculate_downward_ranks(workflow.tasks)

        for task in workflow.tasks:
            task.set_priority(task.down_rank + task.up_rank)
      ...
      
```
• Then we start from an entry task and we try to find the task with the same
priority as the entry task we added in the path. We do that until we hit an **exit task**. When
that happens our critical path is ready.
```python
def construct_critical_path(tasks):
      ...
      
    temp_task = entry_task
    critical_path.append(temp_task)

    # Start from an entry task and run until you find an exit task.
    # Then the critical path would be ready.
    while temp_task.is_exit is False:
        for child_edge in temp_task.children_edges:
            if round(child_edge.node.priority, 5) == entry_priority:
                temp_task = child_edge.node
                critical_path.append(child_edge.node)
                break
      ...
```

## Multiple Workflow Scheduling

Below we see some workflow scheduling algorithms for multiple workflows.

### Connect Workflows

With this approach we connect all the workflows together and we create one **BIG** workflow with **one entry task**
and one **one exit task**. One of the methods suggested here is a round robin heft approach. Which suggests:

1. Calculate the up_rank
2. Sort based the up_rank
3. Schedule the task based the up_rank but also pick a task from each workflow at the time until you loop through all workflows.

### Holes Scheduling

With this method we takes advantage of the holes that are getting created 
from long data transfer times of the files to between the machines. We try
to take advantage of this and we do the following:

• Calculate the property **workflow.ccr**.
```python
def calc_ccr(self):
    """ccr = Communication to computation ratio."""
    if self.avg_comp_cost == -1:
        self.calc_avg_comp_cost()
    if self.avg_com_cost == -1:
        self.calc_avg_com_cost()
    ccr = self.avg_com_cost / self.avg_comp_cost
    return ccr
```
• We sort the workflows based of their ccr.
```python
    sorted_wfs = sorted(workflows, key=lambda wf_: wf_.ccr, reverse=True)
```
• We try to create as many holes as possible. To do this we try to schedule on perpuse one workflow with high computation cost so it can 
create big holes between the machines and then we 'fit' inside these holes a low communication cost workflow.
```python
    j = len(sorted_wfs) - 1
    for i in range(len(sorted_wfs) // 2):
        scheduler.schedule_workflow(
            sorted_wfs[i], machines, time_types[0], hole_filling_type)
        scheduler.schedule_workflow(
            sorted_wfs[j], machines, time_types[1], hole_filling_type)
        j -= 1
```

### Time types
About the **time_types** variable. We schedule our workflows in pairs. This array (time_types) holds two values one that corrisponds on how the first workflow is going to be scheduled and the second on how the second workflow is getting scheduled. We can change this array and try many ways to schedule our workflows. e.g:


######EFT
Pick the machine that gives the **earliest finish time** for our task. e.g: if *T2* in *M1* gives schedule-len = 10 and *T2* in *M2* gives 
schedule-len = 12 we pick M1.
######EST
Pick the machine that gives the **earliest start time** for our task.
######LST
Pick the machine that gives the **latest start time** for our task.
######LFT
Pick the machine that gives the **latest finish time** for our task.

### Hole Filling Types
Now about the **hole_filling_type** variable. We can change this variable and try many ways to put a task in a hole. e.g:

######BEST FIT (B)
Pick the hole that **fills** the most space possible.
######WORST FIT (W)
Pick the hole that **leaves** the most space possible.
######FIRST FIT (FR)
Pick the first hole that fits our task.
######FASTEST FIT (FST)
Pick the **machine** that gives the best time based on our time types regardless if we fill a hole or not.

