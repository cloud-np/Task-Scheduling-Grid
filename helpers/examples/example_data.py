from classes.task import TaskBlueprint, Edge, TaskStatus

HOLE_METHOD_VARIATIONS = {
    "criticals_unsorted": [
        {"name": "crit_u BEST-FIT", "fill_type": "BEST-FIT"},
        {"name": "crit_u FASTEST-FIT", "fill_type": "FASTEST-FIT"},
        {"name": "crit_u FIRST-FIT", "fill_type": "FIRST-FIT"},
        {"name": "crit_u WORST-FIT", "fill_type": "WORST-FIT"},
    ],
    "criticals_sorted": [
        {"name": "crit BEST-FIT", "fill_type": "BEST-FIT"},
        {"name": "crit FASTEST-FIT", "fill_type": "FASTEST-FIT"},
        {"name": "crit FIRST-FIT", "fill_type": "FIRST-FIT"},
        {"name": "crit WORST-FIT", "fill_type": "WORST-FIT"},
    ],

    "EFT_variations": [
        # EST - EST
        {"name": "holes BEST-FIT",
         "time_types": ["EST", "EST"], "fill_type": "BEST-FIT"},
        {"name": "holes FASTEST-FIT",
         "time_types": ["EST", "EST"], "fill_type": "FASTEST-FIT"},
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

    "holes-paper-2011": [
        # "holes-2011-FASTEST-FIT": [
        {"name": "holes2011 FASTEST-EDF", "fill_type": "FASTEST-FIT", "priority_type": "EDF"},
        {"name": "holes2011 FASTEST-LSTF", "fill_type": "FASTEST-FIT", "priority_type": "LSTF"},
        {"name": "holes2011 FASTEST-HLF", "fill_type": "FASTEST-FIT", "priority_type": "HLF"},
        # "holes-2011-BEST-FIT": [
        {"name": "holes2011 BEST-EDF", "fill_type": "BEST-FIT", "priority_type": "EDF"},
        {"name": "holes2011 BEST-LSTF", "fill_type": "BEST-FIT", "priority_type": "LSTF"},
        {"name": "holes2011 BEST-HLF", "fill_type": "BEST-FIT", "priority_type": "HLF"},
        # "holes-2011-WORST-FIT": [
        {"name": "holes2011 WORST-EDF", "fill_type": "WORST-FIT", "priority_type": "EDF"},
        {"name": "holes2011 WORST-LSTF", "fill_type": "WORST-FIT", "priority_type": "LSTF"},
        {"name": "holes2011 WORST-HLF", "fill_type": "WORST-FIT", "priority_type": "HLF"},
        # "holes-2011-FIRST-FIT": [
        {"name": "holes2011 FIRST-EDF", "fill_type": "FIRST-FIT", "priority_type": "EDF"},
        {"name": "holes2011 FIRST-LSTF", "fill_type": "FIRST-FIT", "priority_type": "LSTF"},
        {"name": "holes2011 FIRST-HLF", "fill_type": "FIRST-FIT", "priority_type": "HLF"},
    ],

    "compositions": [
        {"name": "c1", "time_types": ["EST"], "fill_type": "NO-FILL"},
        # {"name": "c2", "time_types": ["EST"], "fill_type": "NO-FILL"},
        {"name": "c3", "time_types": ["EST"], "fill_type": "NO-FILL"},
    ]

}

SMALL_EXAMPLE = {
    "machines": [
        (0, 'M-0', 1, 1),
        (1, 'M-1', 2, 1),
        # (2, 'M-2', 4, 1)
    ],

    "first-fit":
    [
        [
            TaskBlueprint(0, 0, "T-A", 1, [{'weight': 15, 'name': 'T-B'}, {'weight': 13, 'name': 'T-C'}, {'weight': 1, 'name': 'T-D'}], [], 1, True, False),
            TaskBlueprint(1, 0, "T-B", 74, [{'weight': 38, 'name': 'T-E'}], [{'weight': 15, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 0, "T-C", 34, [{'weight': 27, 'name': 'T-E'}], [{'weight': 13, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(3, 0, "T-D", 2, [{'weight': 56, 'name': 'T-E'}], [{'weight': 1, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(4, 0, "T-E", 73, [{'weight': 16, 'name': 'T-F'}, {'weight': 97, 'name': 'T-G'}], [{'weight': 38, 'name': 'T-B'}, {'weight': 27, 'name': 'T-C'}, {'weight': 56, 'name': 'T-D'}], 0, False, False),
            TaskBlueprint(5, 0, "T-F", 23, [{'weight': 34, 'name': 'T-H'}], [{'weight': 16, 'name': 'T-E'}], 0, False, False),
            TaskBlueprint(6, 0, "T-G", 79, [{'weight': 53, 'name': 'T-H'}], [{'weight': 97, 'name': 'T-E'}], 0, False, False),
            TaskBlueprint(7, 0, "T-H", 100, [], [{'weight': 34, 'name': 'T-F'}, {'weight': 53, 'name': 'T-G'}], 0, False, True),
        ],
        [
            TaskBlueprint(0, 1, "T-A", 14, [{'weight': 46, 'name': 'T-B'}], [], 1, True, False),
            TaskBlueprint(1, 1, "T-B", 65, [{'weight': 48, 'name': 'T-C'}], [{'weight': 46, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 1, "T-C", 79, [{'weight': 77, 'name': 'T-D'}], [{'weight': 48, 'name': 'T-B'}], 0, False, False),
            TaskBlueprint(3, 1, "T-D", 30, [], [{'weight': 77, 'name': 'T-C'}], 0, False, True),
        ]
    ],
    "fastest-fit":
    [
        [
            TaskBlueprint(0, 0, "T-A", 76, [{'weight': 86, 'name': 'T-B'}, {'weight': 9, 'name': 'T-C'}, {'weight': 70, 'name': 'T-D'}], [], 1, True, False),
            TaskBlueprint(1, 0, "T-B", 79, [{'weight': 55, 'name': 'T-E'}], [{'weight': 86, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 0, "T-C", 50, [{'weight': 50, 'name': 'T-E'}], [{'weight': 9, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(3, 0, "T-D", 61, [{'weight': 77, 'name': 'T-E'}], [{'weight': 70, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(4, 0, "T-E", 76, [{'weight': 26, 'name': 'T-F'}, {'weight': 21, 'name': 'T-G'}], [{'weight': 55, 'name': 'T-B'}, {'weight': 50, 'name': 'T-C'}, {'weight': 77, 'name': 'T-D'}], 0, False, False),
            TaskBlueprint(5, 0, "T-F", 38, [{'weight': 67, 'name': 'T-H'}], [{'weight': 26, 'name': 'T-E'}], 0, False, False),
            TaskBlueprint(6, 0, "T-G", 94, [{'weight': 92, 'name': 'T-H'}], [{'weight': 21, 'name': 'T-E'}], 0, False, False),
            TaskBlueprint(7, 0, "T-H", 28, [], [{'weight': 67, 'name': 'T-F'}, {'weight': 92, 'name': 'T-G'}], 0, False, True)
        ],
        [
            TaskBlueprint(0, 1, "T-A", 100, [{'weight': 60, 'name': 'T-B'}], [], 1, True, False),
            TaskBlueprint(1, 1, "T-B", 39, [{'weight': 87, 'name': 'T-C'}], [{'weight': 60, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 1, "T-C", 88, [{'weight': 39, 'name': 'T-D'}], [{'weight': 87, 'name': 'T-B'}], 0, False, False),
            TaskBlueprint(3, 1, "T-D", 50, [], [{'weight': 39, 'name': 'T-C'}], 0, False, True),
        ]
    ],
    "worst-fit":
    [
        [
            TaskBlueprint(0, 0, "T-A", 28, [{'weight': 13, 'name': 'T-B'}, {'weight': 21, 'name': 'T-C'}, {'weight': 29, 'name': 'T-D'}], [], 1, True, False),
            TaskBlueprint(1, 0, "T-B", 73, [{'weight': 23, 'name': 'T-E'}], [{'weight': 13, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 0, "T-C", 84, [{'weight': 97, 'name': 'T-E'}], [{'weight': 21, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(3, 0, "T-D", 69, [{'weight': 80, 'name': 'T-E'}], [{'weight': 29, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(4, 0, "T-E", 94, [{'weight': 72, 'name': 'T-F'}, {'weight': 22, 'name': 'T-G'}], [{'weight': 23, 'name': 'T-B'}, {'weight': 97, 'name': 'T-C'}, {'weight': 80, 'name': 'T-D'}], 0, False, False),
            TaskBlueprint(5, 0, "T-F", 7, [{'weight': 62, 'name': 'T-H'}], [{'weight': 72, 'name': 'T-E'}], 0, False, False),
            TaskBlueprint(6, 0, "T-G", 80, [{'weight': 17, 'name': 'T-H'}], [{'weight': 22, 'name': 'T-E'}], 0, False, False),
            TaskBlueprint(7, 0, "T-H", 91, [], [{'weight': 62, 'name': 'T-F'}, {'weight': 17, 'name': 'T-G'}], 0, False, True),
        ],
        [
            TaskBlueprint(0, 1, "T-A", 20, [{'weight': 77, 'name': 'T-B'}], [], 1, True, False),
            TaskBlueprint(1, 1, "T-B", 27, [{'weight': 99, 'name': 'T-C'}], [{'weight': 77, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 1, "T-C", 16, [{'weight': 74, 'name': 'T-D'}], [{'weight': 99, 'name': 'T-B'}], 0, False, False),
            TaskBlueprint(3, 1, "T-D", 46, [], [{'weight': 74, 'name': 'T-C'}], 0, False, True),
        ]
    ],
    "example": [
        [
            TaskBlueprint(0, 0, "T-A", 69, [{'weight': 12, 'name': 'T-B'}, {'weight': 3, 'name': 'T-C'}, {'weight': 13, 'name': 'T-D'}], [], 1, True, False),
            TaskBlueprint(1, 0, "T-B", 92, [{'weight': 34, 'name': 'T-E'}], [{'weight': 12, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 0, "T-C", 50, [{'weight': 24, 'name': 'T-E'}], [{'weight': 3, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(3, 0, "T-D", 78, [{'weight': 32, 'name': 'T-E'}], [{'weight': 13, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(4, 0, "T-E", 24, [{'weight': 26, 'name': 'T-F'}, {'weight': 5, 'name': 'T-G'}], [{'weight': 34, 'name': 'T-B'}, {'weight': 24, 'name': 'T-C'}, {'weight': 32, 'name': 'T-D'}], 0, False, False),
            TaskBlueprint(5, 0, "T-F", 33, [{'weight': 75, 'name': 'T-H'}], [{'weight': 26, 'name': 'T-E'}], 0, False, False),
            TaskBlueprint(6, 0, "T-G", 20, [{'weight': 18, 'name': 'T-H'}], [{'weight': 5, 'name': 'T-E'}], 0, False, False),
            TaskBlueprint(7, 0, "T-H", 89, [], [{'weight': 75, 'name': 'T-F'}, {'weight': 18, 'name': 'T-G'}], 0, False, True),
        ],
        # [
        #     TaskBlueprint(0, 1, "T-A", 38, [{'weight': 85, 'name': 'T-B'}, {'weight': 85, 'name': 'T-C'}], [], 1, True, False),
        #     TaskBlueprint(1, 1, "T-B", 24, [{'weight': 70, 'name': 'T-D'}], [{'weight': 85, 'name': 'T-A'}], 0, False, False),
        #     TaskBlueprint(2, 1, "T-C", 100, [{'weight': 78, 'name': 'T-D'}], [{'weight': 85, 'name': 'T-A'}], 0, False, False),
        #     TaskBlueprint(3, 1, "T-D", 75, [], [{'weight': 70, 'name': 'T-B'}, {'weight': 78, 'name': 'T-C'}], 0, False, True),
        # ]
    ],
    "best-fit":
    [
        [
            TaskBlueprint(0, 0, "T-A", 69, [{'weight': 12, 'name': 'T-B'}, {'weight': 3, 'name': 'T-C'}, {'weight': 13, 'name': 'T-D'}], [], 1, True, False),
            TaskBlueprint(1, 0, "T-B", 92, [{'weight': 34, 'name': 'T-E'}], [{'weight': 12, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 0, "T-C", 50, [{'weight': 24, 'name': 'T-E'}], [{'weight': 3, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(3, 0, "T-D", 78, [{'weight': 32, 'name': 'T-E'}], [{'weight': 13, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(4, 0, "T-E", 24, [{'weight': 26, 'name': 'T-F'}, {'weight': 5, 'name': 'T-G'}], [{'weight': 34, 'name': 'T-B'}, {'weight': 24, 'name': 'T-C'}, {'weight': 32, 'name': 'T-D'}], 0, False, False),
            TaskBlueprint(5, 0, "T-F", 33, [{'weight': 75, 'name': 'T-H'}], [{'weight': 26, 'name': 'T-E'}], 0, False, False),
            TaskBlueprint(6, 0, "T-G", 20, [{'weight': 18, 'name': 'T-H'}], [{'weight': 5, 'name': 'T-E'}], 0, False, False),
            TaskBlueprint(7, 0, "T-H", 89, [], [{'weight': 75, 'name': 'T-F'}, {'weight': 18, 'name': 'T-G'}], 0, False, True),
        ],
        [
            TaskBlueprint(0, 1, "T-A", 38, [{'weight': 85, 'name': 'T-B'}, ], [], 1, True, False),
            TaskBlueprint(1, 1, "T-B", 24, [{'weight': 70, 'name': 'T-C'}], [{'weight': 85, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 1, "T-C", 100, [{'weight': 78, 'name': 'T-D'}], [{'weight': 70, 'name': 'T-B'}], 0, False, False),
            TaskBlueprint(3, 1, "T-D", 75, [], [{'weight': 78, 'name': 'T-C'}], 0, False, True),
        ]
    ],
    "workflows":
    [
        [
            TaskBlueprint(0, 0, "T-A", 67, [{'weight': 1, 'name': 'T-B'}, {'weight': 50, 'name': 'T-C'}, {'weight': 26, 'name': 'T-D'}], [], 1, True, False),
            TaskBlueprint(1, 0, "T-B", 54, [{'weight': 51, 'name': 'T-E'}], [{'weight': 1, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 0, "T-C", 63, [{'weight': 56, 'name': 'T-E'}], [{'weight': 50, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(3, 0, "T-D", 26, [{'weight': 98, 'name': 'T-E'}], [{'weight': 26, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(4, 0, "T-E", 25, [{'weight': 73, 'name': 'T-F'}, {'weight': 33, 'name': 'T-G'}], [{'weight': 51, 'name': 'T-B'}, {'weight': 56, 'name': 'T-C'}, {'weight': 98, 'name': 'T-D'}], 0, False, False),
            TaskBlueprint(5, 0, "T-F", 26, [{'weight': 16, 'name': 'T-H'}], [{'weight': 73, 'name': 'T-E'}], 0, False, False),
            TaskBlueprint(6, 0, "T-G", 7, [{'weight': 41, 'name': 'T-H'}], [{'weight': 33, 'name': 'T-E'}], 0, False, False),
            TaskBlueprint(7, 0, "T-H", 61, [], [{'weight': 16, 'name': 'T-F'}, {'weight': 41, 'name': 'T-G'}], 0, False, True)
        ],
        [
            TaskBlueprint(0, 1, "T-A", 32, [{'weight': 69, 'name': 'T-B'}], [], 1, True, False),
            TaskBlueprint(1, 1, "T-B", 20, [{'weight': 95, 'name': 'T-C'}], [{'weight': 69, 'name': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 1, "T-C", 65, [{'weight': 11, 'name': 'T-D'}], [{'weight': 95, 'name': 'T-B'}], 0, False, False),
            TaskBlueprint(3, 1, "T-D", 7, [], [{'weight': 11, 'name': 'T-C'}], 0, False, True),
        ]
        # [
        #     TaskBlueprint(0, 0, 'T-A', 20, [{"weight": 12, "name": 'T-B'}, {"weight": 15, "name": 'T-C'}, {"weight": 15, "name": 'T-C'}], [], TaskStatus.READY, True, False),
        #     TaskBlueprint(1, 0, 'T-B', 50, [{"weight": 10, "name": 'T-D'}], [{"weight": 12, "name": 'T-A'}], TaskStatus.UNSCHEDULED, False, False),
        #     TaskBlueprint(2, 0, 'T-C', 90, [{"weight": 5, "name": 'T-E'}], [{"weight": 15, "name": 'T-A'}], TaskStatus.UNSCHEDULED, False, False),
        #     TaskBlueprint(3, 0, 'T-D', 60, [{"weight": 10, "name": 'T-E'}], [{"weight": 10, "name": 'T-B'}], TaskStatus.UNSCHEDULED, False, False),
        #     TaskBlueprint(4, 0, 'T-E', 20, [], [{"weight": 10, "name": 'T-D'}, {"weight": 5, "name": 'T-C'}], TaskStatus.UNSCHEDULED, False, True),
        # ],
        # [
        #     TaskBlueprint(0, 1, 'T-A', 3, [{"weight": 3, "name": 'T-B'}, {"weight": 4, "name": 'T-C'}], [], TaskStatus.READY, True, False),
        #     TaskBlueprint(1, 1, 'T-B', 15, [{"weight": 6, "name": 'T-D'}], [{"weight": 3, "name": 'T-A'}], TaskStatus.UNSCHEDULED, False, False),
        #     TaskBlueprint(2, 1, 'T-C', 41, [{"weight": 2, "name": 'T-D'}], [{"weight": 4, "name": 'T-A'}], TaskStatus.UNSCHEDULED, False, False),
        #     TaskBlueprint(3, 1, 'T-D', 10, [], [{"weight": 6, "name": 'T-B'}, {"weight": 2, "name": 'T-C'}], TaskStatus.UNSCHEDULED, False, True),
        # ],
        # [
        #     TaskBlueprint(0, 2, 'T-A', 5, [{"weight": 31, "name": 'T-B'}], [], TaskStatus.READY, True, False),
        #     TaskBlueprint(1, 2, 'T-B', 7, [{"weight": 25, "name": 'T-C'}], [{"weight": 31, "name": 'T-A'}], TaskStatus.UNSCHEDULED, False, False),
        #     TaskBlueprint(2, 2, 'T-C', 3, [], [{"weight": 25, "name": 'T-B'}], TaskStatus.UNSCHEDULED, False, True),
        # ],
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
