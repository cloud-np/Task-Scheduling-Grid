HOLE_METHOD_VARIATIONS = {

    "EFT_variations": [
        # EST - EST
        {"name": "holes FASTEST-FIT",
         "time_types": ["EST", "EST"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT",
         "time_types": ["EST", "EST"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT",
         "time_types": ["EST", "EST"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT",
         "time_types": ["EST", "EST"], "fill_type": "WORST-FIT"},
        # EFT - EST
        {"name": "holes FASTEST-FIT",
         "time_types": ["EFT", "EST"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT",
         "time_types": ["EFT", "EST"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT",
         "time_types": ["EFT", "EST"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT",
         "time_types": ["EFT", "EST"], "fill_type": "WORST-FIT"},
        # EFT - EFT
        {"name": "holes FASTEST-FIT",
         "time_types": ["EFT", "EFT"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT",
         "time_types": ["EFT", "EFT"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT",
         "time_types": ["EFT", "EFT"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT",
         "time_types": ["EFT", "EFT"], "fill_type": "WORST-FIT"},
        # EST - EFT
        {"name": "holes FASTEST-FIT",
         "time_types": ["EST", "EFT"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT",
         "time_types": ["EST", "EFT"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT",
         "time_types": ["EST", "EFT"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT", "time_types": ["EST", "EFT"], "fill_type": "WORST-FIT"}],

    "LFT_variations": [
        # LST - EFT
        {"name": "holes FASTEST-FIT",
         "time_types": ["LST", "EFT"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT",
         "time_types": ["LST", "EFT"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT",
         "time_types": ["LST", "EFT"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT",
         "time_types": ["LST", "EFT"], "fill_type": "WORST-FIT"},
        # LST - EST
        {"name": "holes FASTEST-FIT",
         "time_types": ["LST", "EST"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT",
         "time_types": ["LST", "EST"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT",
         "time_types": ["LST", "EST"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT",
         "time_types": ["LST", "EST"], "fill_type": "WORST-FIT"},
        # LFT - EST
        {"name": "holes FASTEST-FIT",
         "time_types": ["LFT", "EST"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT",
         "time_types": ["LFT", "EST"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT",
         "time_types": ["LFT", "EST"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT",
         "time_types": ["LFT", "EST"], "fill_type": "WORST-FIT"},
        # LFT - EFT
        {"name": "holes FASTEST-FIT",
         "time_types": ["LFT", "EFT"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT",
         "time_types": ["LFT", "EFT"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT",
         "time_types": ["LFT", "EFT"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT", "time_types": ["LFT", "EFT"], "fill_type": "WORST-FIT"}],

    "holes-2011-FASTEST-FIT": [
        {"name": "holes2011 FASTEST-EDF", "fill_type": "FASTEST-FIT", "priority_type": "EDF"},
        {"name": "holes2011 FASTEST-LSTF", "fill_type": "FASTEST-FIT", "priority_type": "LSTF"},
        {"name": "holes2011 FASTEST-HLF", "fill_type": "FASTEST-FIT", "priority_type": "HLF"},
    ],
    "holes-2011-BEST-FIT": [
        {"name": "holes2011 BEST-EDF", "fill_type": "BEST-FIT", "priority_type": "EDF"},
        {"name": "holes2011 BEST-LSTF", "fill_type": "BEST-FIT", "priority_type": "LSTF"},
        {"name": "holes2011 BEST-HLF", "fill_type": "BEST-FIT", "priority_type": "HLF"},
    ],
    "holes-2011-WORST-FIT": [
        {"name": "holes2011 WORST-EDF", "fill_type": "WORST-FIT", "priority_type": "EDF"},
        {"name": "holes2011 WORST-LSTF", "fill_type": "WORST-FIT", "priority_type": "LSTF"},
        {"name": "holes2011 WORST-HLF", "fill_type": "WORST-FIT", "priority_type": "HLF"},
    ],
    "holes-2011-FIRST-FIT": [
        {"name": "holes2011 FIRST-EDF", "fill_type": "FIRST-FIT", "priority_type": "EDF"},
        {"name": "holes2011 FIRST-LSTF", "fill_type": "FIRST-FIT", "priority_type": "LSTF"},
        {"name": "holes2011 FIRST-HLF", "fill_type": "FIRST-FIT", "priority_type": "HLF"},
    ]
}


# MUTLIPLE WORKFLOW PAPER

RANKS_A = [50, 42, 36, 20, 6]

RANKS_B = [200, 152, 122, 140, 45, 63, 13]

NAMES_A = ["A1", "A2", "A3", "A4", "A5"]

NAMES_B = ["B1", "B2", "B3", "B4", "B5", "B6", "B7"]

PARENTS_DAG_A = [
    [],
    [{"name": "A1", "weight": 4}],
    [{"name": "A1", "weight": 2}],
    [{"name": "A1", "weight": 2}],
    [{"name": "A2", "weight": 10}, {"name": "A3",
                                    "weight": 5}, {"name": "A4", "weight": 3}],
]

TASK_DAG_A = [
    [{"name": "A2", "weight": 4}, {"name": "A3",
                                   "weight": 2}, {"name": "A4", "weight": 2}],
    [{"name": "A5", "weight": 10}],
    [{"name": "A5", "weight": 5}],
    [{"name": "A5", "weight": 3}],
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
    [{"name": "B1", "weight": 3}],
    [{"name": "B1", "weight": 5}],
    [{"name": "B1", "weight": 1}],
    [{"name": "B2", "weight": 10}, {"name": "B4", "weight": 9}],
    [{"name": "B3", "weight": 3}, {"name": "B4", "weight": 8}],
    [{"name": "B5", "weight": 4}, {"name": "B6", "weight": 2}]
]

TASK_DAG_B = [
    [{"name": "B2", "weight": 3}, {"name": "B3",
                                   "weight": 5}, {"name": "B4", "weight": 1}],
    [{"name": "B5", "weight": 10}],
    [{"name": "B6", "weight": 3}],
    [{"name": "B5", "weight": 9}, {"name": "B6", "weight": 8}],
    [{"name": "B7", "weight": 4}],
    [{"name": "B7", "weight": 2}],
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
    [-1, -1, -1, -1, -1, 2, 3, -1, 2, -1, -1, -1, -1],
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
