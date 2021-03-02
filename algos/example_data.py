# MUTLIPLE WORKFLOW PAPER

RANKS_A = [ 50, 42, 36, 20, 6 ] 

RANKS_B = [ 200, 152, 122, 140, 45, 63, 13 ] 

NAMES_A = ["A1", "A2", "A3", "A4", "A5"]

NAMES_B = ["B1", "B2", "B3", "B4", "B5", "B6", "B7"]

PARENTS_DAG_A = [
    [],
    ["A1"],
    ["A1"],
    ["A1"],
    ["A2", "A3", "A4"],
]

TASK_DAG_A = [
    ["A2", "A3", "A4"],
    ["A5"],
    ["A5"],
    ["A5"],
    []
]

COSTS_A = [
    [3, 5, 9, 2],
    [2, 3, 7, 4],
    [3, 5, 8, 4],
    [2, 3, 5, 3],
    [2, 3, 3, 5]
]

COSTS_B = [
    [14, 16, 9, 10],
    [5, 11, 14, 14],
    [18, 12, 20, 20],
    [21, 7, 16, 9],
    [12, 13, 10, 10],
    [13, 16, 9, 13],
    [7, 15, 11, 11],
]

PARENTS_DAG_B = [
    [],
    ["B1"],
    ["B1"],
    ["B1"],
    ["B2", "B4"],
    ["B3", "B4"],
    ["B5", "B6"]
]

TASK_DAG_B = [
    ["B2", "B3", "B4"],
    ["B5"],
    ["B6"],
    ["B5", "B6"],
    ["B7"],
    ["B7"],
    []
]

# EXAMPLE HEFT PAPER
COSTS = [
    [0, 0, 0],
    [14, 16, 9],
    [13, 19, 18],
    [11, 13, 19],
    [13, 8, 17],
    [12, 13, 10],
    [13, 16, 9],
    [7, 15, 11],
    [5, 11, 14],
    [18, 12, 20],
    [21, 7, 16]
]

NAMES = [
    'DummyIn',
    'NoName',
    'NoName',
    'NoName',
    'NoName',
    'NoName',
    'NoName',
    'NoName',
    'NoName',
    'NoName',
    'NoName'
]
TASK_DAG = [
    # 0 Dummy In
    [-1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    # 1   2   3  4   5   6   7   8   9  10
    [-1, -1, 18, 12, 9, 11, 14, -1, -1, -1, -1],
    # 2
    [-1, -1, -1, -1, -1, -1, -1, -1, 19, 16, -1],
    # 3
    [-1, -1, -1, -1, -1, -1, -1, 23, -1, -1, -1],
    # 4
    [-1, -1, -1, -1, -1, -1, -1, -1, 27, 23, -1],
    # 5
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 13, -1],
    # 6
    [-1, -1, -1, -1, -1, -1, -1, -1, 15, -1, -1],
    # 7
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 17],
    # 8
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 11],
    # 9
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 13],
    # 10
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
]
# #################################################
# Deadline constraint
COSTS_1 = [
    [0, 0, 0],
    [3, 5, 1],
    [2, 3, 1],
    [3, 5, 1],
    [2, 3, 1],
    [2, 3, 1],
    [2, 3, 1],
    [2, 3, 1],
    [4, 6, 2],
    [3, 5, 1],
    [2, 3, 1],
    [5, 7, 3],
    [0, 0, 0]
]

NAMES_1 = [
    'DummyIn',
    'NoName',
    'NoName',
    'NoName',
    'NoName',
    'NoName',
    'NoName',
    'NoName',
    'NoName',
    'NoName',
    'NoName',
    'NoName',
    'DummyOut'
]

TASK_DAG_1 = [
    # 0 Dummy In
    [-1, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1],
    # 1   1   2   3   4   5   6   7   8   9  10  11
    [-1, -1, -1, -1, -1,  2,  3, -1,  2, -1, -1, -1, -1],
    # 2
    [-1, -1, -1, -1, -1, -1, -1, 5, -1, 1, -1, -1, -1],
    # 3
    [-1, -1, -1, -1, -1, -1, 3, 1, -1, -1, -1, -1, -1],
    # 4
    [-1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1],
    # 5
    [-1, -1, -1, -1, -1, -1, -1, -1, 5, -1, -1, -1, -1],
    # 6
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 3, 2, -1, -1],
    # 7
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 3, -1],
    # 8
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0],
    # 9
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0],
    # 10
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0],
    # 11
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0],
    # Dummy OUT
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
]
