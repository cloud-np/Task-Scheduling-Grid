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
1. First we need to calculate the priority of each task. Which means we need to 
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
2. Then we construct the critical path
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

```python
def heft(tasks: List[Task], machines: List[Machine]):
  # Phase 1
  calculate_upward_ranks(tasks)
  
  # Sort the tasks based of the up_rank
  tasks.sort(key=lambda task: task.up_rank, reverse=True)
  
  # Phase 2
  schedule_tasks_with_EFT(tasks, machines)
```


### Holes Scheduling

With this method we takes advantage of the holes that are 
getting created from long data transfer times of the files to between the machines.

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```
