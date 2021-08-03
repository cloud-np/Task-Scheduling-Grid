## Overview

This project tries to solve the problem of task scheduling of multiple workflows in a grid. Which is a NP-Problem.
Below we gonna look into details some of the algorithms used to solve this problem. (later on we gonna describe the problem better as well)

## Single Workflow Scheduling

Below we see some popular single workflow scheduling algorithms.

### HEFT
Heterogeneous-Earliest-Finish-Time (HEFT).

**Info**
The HEFT algorithm has 2 major phases: 
1. Task prioritizing
      With that in mind we calculate the **task.up_rank** property 
      of the tasks and we sort them based of that value.
2. Processor selection
      We pick the machine for each task that give the best **earliest finish time**.



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
