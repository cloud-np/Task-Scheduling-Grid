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
        # {"name": "holes BEST-FIT",
        #  "time_types": ["EST", "EST"], "fill_type": "BEST-FIT"},
        # {"name": "holes FASTEST-FIT",
        #  "time_types": ["EST", "EST"], "fill_type": "FASTEST-FIT"},
        # {"name": "holes FIRST-FIT",
        #  "time_types": ["EST", "EST"], "fill_type": "FIRST-FIT"},
        # {"name": "holes WORST-FIT",
        #  "time_types": ["EST", "EST"], "fill_type": "WORST-FIT"},
        # EFT - EST
        {"name": "holes FASTEST-FIT", "time_types": ["EFT", "EST"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT", "time_types": ["EFT", "EST"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT", "time_types": ["EFT", "EST"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT", "time_types": ["EFT", "EST"], "fill_type": "WORST-FIT"},
        # EFT - EFT
        {"name": "holes FASTEST-FIT", "time_types": ["EFT", "EFT"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT", "time_types": ["EFT", "EFT"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT", "time_types": ["EFT", "EFT"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT", "time_types": ["EFT", "EFT"], "fill_type": "WORST-FIT"},
        # EST - EFT
        {"name": "holes FASTEST-FIT", "time_types": ["EST", "EFT"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT", "time_types": ["EST", "EFT"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT", "time_types": ["EST", "EFT"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT", "time_types": ["EST", "EFT"], "fill_type": "WORST-FIT"}
    ],

    "LFT_variations": [
        # LST - EFT
        {"name": "holes FASTEST-FIT", "time_types": ["LST", "EFT"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT", "time_types": ["LST", "EFT"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT", "time_types": ["LST", "EFT"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT", "time_types": ["LST", "EFT"], "fill_type": "WORST-FIT"},
        # LST - EST
        {"name": "holes FASTEST-FIT", "time_types": ["LST", "EST"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT", "time_types": ["LST", "EST"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT", "time_types": ["LST", "EST"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT", "time_types": ["LST", "EST"], "fill_type": "WORST-FIT"},
        # LFT - EST
        {"name": "holes FASTEST-FIT", "time_types": ["LFT", "EST"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT", "time_types": ["LFT", "EST"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT", "time_types": ["LFT", "EST"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT", "time_types": ["LFT", "EST"], "fill_type": "WORST-FIT"},
        # LFT - EFT
        {"name": "holes FASTEST-FIT", "time_types": ["LFT", "EFT"], "fill_type": "FASTEST-FIT"},
        {"name": "holes BEST-FIT", "time_types": ["LFT", "EFT"], "fill_type": "BEST-FIT"},
        {"name": "holes FIRST-FIT", "time_types": ["LFT", "EFT"], "fill_type": "FIRST-FIT"},
        {"name": "holes WORST-FIT", "time_types": ["LFT", "EFT"], "fill_type": "WORST-FIT"}],

    "holes-paper-2011": [
        # "holes-2011-FASTEST-FIT": [
        # {"name": "holes2011 FASTEST-EDF", "fill_type": "FASTEST-FIT", "priority_type": "EDF"},
        # {"name": "holes2011 FASTEST-LSTF", "fill_type": "FASTEST-FIT", "priority_type": "LSTF"},
        # {"name": "holes2011 FASTEST-HLF", "fill_type": "FASTEST-FIT", "priority_type": "HLF"},
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
        # {"name": "c3", "time_types": ["EST"], "fill_type": "NO-FILL"},
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
            TaskBlueprint(0, 0, "T-A", 1, None, [{'w': 15, 'n': 'T-B'}, {'w': 13, 'n': 'T-C'}, {'w': 1, 'n': 'T-D'}], [], 1, True, False),
            TaskBlueprint(1, 0, "T-B", 74, None, [{'w': 38, 'n': 'T-E'}], [{'w': 15, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 0, "T-C", 34, None, [{'w': 27, 'n': 'T-E'}], [{'w': 13, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(3, 0, "T-D", 2, None, [{'w': 56, 'n': 'T-E'}], [{'w': 1, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(4, 0, "T-E", 73, None, [{'w': 16, 'n': 'T-F'}, {'w': 97, 'n': 'T-G'}], [{'w': 38, 'n': 'T-B'}, {'w': 27, 'n': 'T-C'}, {'w': 56, 'n': 'T-D'}], 0, False, False),
            TaskBlueprint(5, 0, "T-F", 23, None, [{'w': 34, 'n': 'T-H'}], [{'w': 16, 'n': 'T-E'}], 0, False, False),
            TaskBlueprint(6, 0, "T-G", 79, None, [{'w': 53, 'n': 'T-H'}], [{'w': 97, 'n': 'T-E'}], 0, False, False),
            TaskBlueprint(7, 0, "T-H", 100, None, [], [{'w': 34, 'n': 'T-F'}, {'w': 53, 'n': 'T-G'}], 0, False, True),
        ],
        [
            TaskBlueprint(0, 1, "T-A", 14, None, [{'w': 46, 'n': 'T-B'}], [], 1, True, False),
            TaskBlueprint(1, 1, "T-B", 65, None, [{'w': 48, 'n': 'T-C'}], [{'w': 46, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 1, "T-C", 79, None, [{'w': 77, 'n': 'T-D'}], [{'w': 48, 'n': 'T-B'}], 0, False, False),
            TaskBlueprint(3, 1, "T-D", 30, None, [], [{'w': 77, 'n': 'T-C'}], 0, False, True),
        ]
    ],
    "fastest-fit":
    [
        [
            TaskBlueprint(0, 0, "T-A", 76, None, [{'w': 86, 'n': 'T-B'}, {'w': 9, 'n': 'T-C'}, {'w': 70, 'n': 'T-D'}], [], 1, True, False),
            TaskBlueprint(1, 0, "T-B", 79, None, [{'w': 55, 'n': 'T-E'}], [{'w': 86, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 0, "T-C", 50, None, [{'w': 50, 'n': 'T-E'}], [{'w': 9, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(3, 0, "T-D", 61, None, [{'w': 77, 'n': 'T-E'}], [{'w': 70, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(4, 0, "T-E", 76, None, [{'w': 26, 'n': 'T-F'}, {'w': 21, 'n': 'T-G'}], [{'w': 55, 'n': 'T-B'}, {'w': 50, 'n': 'T-C'}, {'w': 77, 'n': 'T-D'}], 0, False, False),
            TaskBlueprint(5, 0, "T-F", 38, None, [{'w': 67, 'n': 'T-H'}], [{'w': 26, 'n': 'T-E'}], 0, False, False),
            TaskBlueprint(6, 0, "T-G", 94, None, [{'w': 92, 'n': 'T-H'}], [{'w': 21, 'n': 'T-E'}], 0, False, False),
            TaskBlueprint(7, 0, "T-H", 28, None, [], [{'w': 67, 'n': 'T-F'}, {'w': 92, 'n': 'T-G'}], 0, False, True)
        ],
        [
            TaskBlueprint(0, 1, "T-A", 100, None, [{'w': 60, 'n': 'T-B'}], [], 1, True, False),
            TaskBlueprint(1, 1, "T-B", 39, None, [{'w': 87, 'n': 'T-C'}], [{'w': 60, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 1, "T-C", 88, None, [{'w': 39, 'n': 'T-D'}], [{'w': 87, 'n': 'T-B'}], 0, False, False),
            TaskBlueprint(3, 1, "T-D", 50, None, [], [{'w': 39, 'n': 'T-C'}], 0, False, True),
        ]
    ],
    "worst-fit":
    [
        [
            TaskBlueprint(0, 0, "T-A", 28, None, [{'w': 13, 'n': 'T-B'}, {'w': 21, 'n': 'T-C'}, {'w': 29, 'n': 'T-D'}], [], 1, True, False),
            TaskBlueprint(1, 0, "T-B", 73, None, [{'w': 23, 'n': 'T-E'}], [{'w': 13, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 0, "T-C", 84, None, [{'w': 97, 'n': 'T-E'}], [{'w': 21, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(3, 0, "T-D", 69, None, [{'w': 80, 'n': 'T-E'}], [{'w': 29, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(4, 0, "T-E", 94, None, [{'w': 72, 'n': 'T-F'}, {'w': 22, 'n': 'T-G'}], [{'w': 23, 'n': 'T-B'}, {'w': 97, 'n': 'T-C'}, {'w': 80, 'n': 'T-D'}], 0, False, False),
            TaskBlueprint(5, 0, "T-F", 7, None, [{'w': 62, 'n': 'T-H'}], [{'w': 72, 'n': 'T-E'}], 0, False, False),
            TaskBlueprint(6, 0, "T-G", 80, None, [{'w': 17, 'n': 'T-H'}], [{'w': 22, 'n': 'T-E'}], 0, False, False),
            TaskBlueprint(7, 0, "T-H", 91, None, [], [{'w': 62, 'n': 'T-F'}, {'w': 17, 'n': 'T-G'}], 0, False, True),
        ],
        [
            TaskBlueprint(0, 1, "T-A", 20, None, [{'w': 77, 'n': 'T-B'}], [], 1, True, False),
            TaskBlueprint(1, 1, "T-B", 27, None, [{'w': 99, 'n': 'T-C'}], [{'w': 77, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 1, "T-C", 16, None, [{'w': 74, 'n': 'T-D'}], [{'w': 99, 'n': 'T-B'}], 0, False, False),
            TaskBlueprint(3, 1, "T-D", 46, None, [], [{'w': 74, 'n': 'T-C'}], 0, False, True),
        ]
    ],
    "example": [
        [
            TaskBlueprint(0, 0, "T-A", 69, None, [{'w': 12, 'n': 'T-B'}, {'w': 3, 'n': 'T-C'}, {'w': 13, 'n': 'T-D'}], [], 1, True, False),
            TaskBlueprint(1, 0, "T-B", 92, None, [{'w': 34, 'n': 'T-E'}], [{'w': 12, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 0, "T-C", 50, None, [{'w': 24, 'n': 'T-E'}], [{'w': 3, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(3, 0, "T-D", 78, None, [{'w': 32, 'n': 'T-E'}], [{'w': 13, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(4, 0, "T-E", 24, None, [{'w': 26, 'n': 'T-F'}, {'w': 5, 'n': 'T-G'}], [{'w': 34, 'n': 'T-B'}, {'w': 24, 'n': 'T-C'}, {'w': 32, 'n': 'T-D'}], 0, False, False),
            TaskBlueprint(5, 0, "T-F", 33, None, [{'w': 75, 'n': 'T-H'}], [{'w': 26, 'n': 'T-E'}], 0, False, False),
            TaskBlueprint(6, 0, "T-G", 20, None, [{'w': 18, 'n': 'T-H'}], [{'w': 5, 'n': 'T-E'}], 0, False, False),
            TaskBlueprint(7, 0, "T-H", 89, None, [], [{'w': 75, 'n': 'T-F'}, {'w': 18, 'n': 'T-G'}], 0, False, True),
        ],
        # [
        #     TaskBlueprint(0, 1, "T-A", 38, [{'w': 85, 'n': 'T-B'}, {'w': 85, 'n': 'T-C'}], [], 1, True, False),
        #     TaskBlueprint(1, 1, "T-B", 24, [{'w': 70, 'n': 'T-D'}], [{'w': 85, 'n': 'T-A'}], 0, False, False),
        #     TaskBlueprint(2, 1, "T-C", 100, [{'w': 78, 'n': 'T-D'}], [{'w': 85, 'n': 'T-A'}], 0, False, False),
        #     TaskBlueprint(3, 1, "T-D", 75, [], [{'w': 70, 'n': 'T-B'}, {'w': 78, 'n': 'T-C'}], 0, False, True),
        # ]
    ],
    "best-fit":
    [
        [
            TaskBlueprint(0, 0, "T-A", 69, None, [{'w': 12, 'n': 'T-B'}, {'w': 3, 'n': 'T-C'}, {'w': 13, 'n': 'T-D'}], [], 1, True, False),
            TaskBlueprint(1, 0, "T-B", 92, None, [{'w': 34, 'n': 'T-E'}], [{'w': 12, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 0, "T-C", 50, None, [{'w': 24, 'n': 'T-E'}], [{'w': 3, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(3, 0, "T-D", 78, None, [{'w': 32, 'n': 'T-E'}], [{'w': 13, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(4, 0, "T-E", 24, None, [{'w': 26, 'n': 'T-F'}, {'w': 5, 'n': 'T-G'}], [{'w': 34, 'n': 'T-B'}, {'w': 24, 'n': 'T-C'}, {'w': 32, 'n': 'T-D'}], 0, False, False),
            TaskBlueprint(5, 0, "T-F", 33, None, [{'w': 75, 'n': 'T-H'}], [{'w': 26, 'n': 'T-E'}], 0, False, False),
            TaskBlueprint(6, 0, "T-G", 20, None, [{'w': 18, 'n': 'T-H'}], [{'w': 5, 'n': 'T-E'}], 0, False, False),
            TaskBlueprint(7, 0, "T-H", 89, None, [], [{'w': 75, 'n': 'T-F'}, {'w': 18, 'n': 'T-G'}], 0, False, True),
        ],
        [
            TaskBlueprint(0, 1, "T-A", 38, None, [{'w': 85, 'n': 'T-B'}, ], [], 1, True, False),
            TaskBlueprint(1, 1, "T-B", 24, None, [{'w': 70, 'n': 'T-C'}], [{'w': 85, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 1, "T-C", 100, None, [{'w': 78, 'n': 'T-D'}], [{'w': 70, 'n': 'T-B'}], 0, False, False),
            TaskBlueprint(3, 1, "T-D", 75, None, [], [{'w': 78, 'n': 'T-C'}], 0, False, True),
        ]
    ],
    "workflows":
    [
        [
            TaskBlueprint(0, 0, "T-A", 67, None, [{'w': 1, 'n': 'T-B'}, {'w': 50, 'n': 'T-C'}, {'w': 26, 'n': 'T-D'}], [], 1, True, False),
            TaskBlueprint(1, 0, "T-B", 54, None, [{'w': 51, 'n': 'T-E'}], [{'w': 1, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 0, "T-C", 63, None, [{'w': 56, 'n': 'T-E'}], [{'w': 50, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(3, 0, "T-D", 26, None, [{'w': 98, 'n': 'T-E'}], [{'w': 26, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(4, 0, "T-E", 25, None, [{'w': 73, 'n': 'T-F'}, {'w': 33, 'n': 'T-G'}], [{'w': 51, 'n': 'T-B'}, {'w': 56, 'n': 'T-C'}, {'w': 98, 'n': 'T-D'}], 0, False, False),
            TaskBlueprint(5, 0, "T-F", 26, None, [{'w': 16, 'n': 'T-H'}], [{'w': 73, 'n': 'T-E'}], 0, False, False),
            TaskBlueprint(6, 0, "T-G", 7, None, [{'w': 41, 'n': 'T-H'}], [{'w': 33, 'n': 'T-E'}], 0, False, False),
            TaskBlueprint(7, 0, "T-H", 61, None, [], [{'w': 16, 'n': 'T-F'}, {'w': 41, 'n': 'T-G'}], 0, False, True)
        ],
        [
            TaskBlueprint(0, 1, "T-A", 32, None, [{'w': 69, 'n': 'T-B'}], [], 1, True, False),
            TaskBlueprint(1, 1, "T-B", 20, None, [{'w': 95, 'n': 'T-C'}], [{'w': 69, 'n': 'T-A'}], 0, False, False),
            TaskBlueprint(2, 1, "T-C", 65, None, [{'w': 11, 'n': 'T-D'}], [{'w': 95, 'n': 'T-B'}], 0, False, False),
            TaskBlueprint(3, 1, "T-D", 7, None, [], [{'w': 11, 'n': 'T-C'}], 0, False, True),
        ]
        # [
        #     TaskBlueprint(0, 0, 'T-A', 20, [{"w": 12, "n": 'T-B'}, {"w": 15, "n": 'T-C'}, {"w": 15, "n": 'T-C'}], [], TaskStatus.READY, True, False),
        #     TaskBlueprint(1, 0, 'T-B', 50, [{"w": 10, "n": 'T-D'}], [{"w": 12, "n": 'T-A'}], TaskStatus.UNSCHEDULED, False, False),
        #     TaskBlueprint(2, 0, 'T-C', 90, [{"w": 5, "n": 'T-E'}], [{"w": 15, "n": 'T-A'}], TaskStatus.UNSCHEDULED, False, False),
        #     TaskBlueprint(3, 0, 'T-D', 60, [{"w": 10, "n": 'T-E'}], [{"w": 10, "n": 'T-B'}], TaskStatus.UNSCHEDULED, False, False),
        #     TaskBlueprint(4, 0, 'T-E', 20, [], [{"w": 10, "n": 'T-D'}, {"w": 5, "n": 'T-C'}], TaskStatus.UNSCHEDULED, False, True),
        # ],
        # [
        #     TaskBlueprint(0, 1, 'T-A', 3, [{"w": 3, "n": 'T-B'}, {"w": 4, "n": 'T-C'}], [], TaskStatus.READY, True, False),
        #     TaskBlueprint(1, 1, 'T-B', 15, [{"w": 6, "n": 'T-D'}], [{"w": 3, "n": 'T-A'}], TaskStatus.UNSCHEDULED, False, False),
        #     TaskBlueprint(2, 1, 'T-C', 41, [{"w": 2, "n": 'T-D'}], [{"w": 4, "n": 'T-A'}], TaskStatus.UNSCHEDULED, False, False),
        #     TaskBlueprint(3, 1, 'T-D', 10, [], [{"w": 6, "n": 'T-B'}, {"w": 2, "n": 'T-C'}], TaskStatus.UNSCHEDULED, False, True),
        # ],
        # [
        #     TaskBlueprint(0, 2, 'T-A', 5, [{"w": 31, "n": 'T-B'}], [], TaskStatus.READY, True, False),
        #     TaskBlueprint(1, 2, 'T-B', 7, [{"w": 25, "n": 'T-C'}], [{"w": 31, "n": 'T-A'}], TaskStatus.UNSCHEDULED, False, False),
        #     TaskBlueprint(2, 2, 'T-C', 3, [], [{"w": 25, "n": 'T-B'}], TaskStatus.UNSCHEDULED, False, True),
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
    [{"n": "A1", "w": 4}],
    [{"n": "A1", "w": 2}],
    [{"n": "A1", "w": 2}],
    [{"n": "A2", "w": 10}, {"n": "A3", "w": 5}, {"n": "A4", "w": 3}],
]

TASK_DAG_A = [
    [{"n": "A2", "w": 4}, {"n": "A3", "w": 2}, {"n": "A4", "w": 2}],
    [{"n": "A5", "w": 10}],
    [{"n": "A5", "w": 5}],
    [{"n": "A5", "w": 3}],
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
    [{"n": "B1", "w": 3}],
    [{"n": "B1", "w": 5}],
    [{"n": "B1", "w": 1}],
    [{"n": "B2", "w": 10}, {"n": "B4", "w": 9}],
    [{"n": "B3", "w": 3}, {"n": "B4", "w": 8}],
    [{"n": "B5", "w": 4}, {"n": "B6", "w": 2}]
]

TASK_DAG_B = [
    [{"n": "B2", "w": 3}, {"n": "B3", "w": 5}, {"n": "B4", "w": 1}],
    [{"n": "B5", "w": 10}],
    [{"n": "B6", "w": 3}],
    [{"n": "B5", "w": 9}, {"n": "B6", "w": 8}],
    [{"n": "B7", "w": 4}],
    [{"n": "B7", "w": 2}],
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
