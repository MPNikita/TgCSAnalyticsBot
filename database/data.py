# Emulation of data
# id: random num

# id_tournament, name, date_begin, date_end
data_tournament = [{'id': 1203918, 'name': 'Katowice 2024'},
                   {'id': 213, 'name': 'Moscow 2024'},
                   {'id': 123, 'name': 'London 2024'},
                   ]

# id_match, first_team, second_team, result [0 - TBD, 1 - first_team, 2 - second_team]
# id_tournament 
data_matches = [{'id': 213124, 'id_tournament': 1203918, 'first_team': 'mouz', 'second_team': 'sampi', 'result': 0},
                {'id': 214124, 'id_tournament': 1203918, 'first_team': 'spirti', 'second_team': 'revenant', 'result': 0},
                {'id': 543534, 'id_tournament': 1203918, 'first_team': 'g2', 'second_team': 'sinners', 'result': 0},
                {'id': 131231, 'id_tournament': 213, 'first_team': 'vitality', 'second_team': 'saw', 'result': 0},
                {'id': 892137, 'id_tournament': 213, 'first_team': 'ence', 'second_team': 'faze', 'result': 0},
                {'id': 908965, 'id_tournament': 123, 'first_team': 'insilio', 'second_team': 'amkal', 'result': 0},
                ]

#id_tg !not int it is BIGGER INT!, username
data_user = [{'id': 213124, 'username': 'zelix'},
             {'id': 231455, 'username': 'generalfy'},
             {'id': 567565, 'username': 'tvinkle'},
             ]

#id, id_user, id_match, result [0 - skip, 1 - 1 team, 2 - 2 team]
data_predictions = [{'id:': 1, 'id_user': 1, 'id_match': 1, 'result': 1},
                    {'id:': 2, 'id_user': 1, 'id_match': 3, 'result': 0},
                    {'id:': 3, 'id_user': 2, 'id_match': 6, 'result': 2},
                    {'id:': 4, 'id_user': 3, 'id_match': 5, 'result': 2},
                    ]

#id_user, number_of_predictions, correct_predictions
data_leaderboard = [{'id': 1, 'number_of_predictions': 3, 'correct_predictions': 2},
                    {'id': 2, 'number_of_predictions': 5, 'correct_predictions': 5},
                    {'id': 3, 'number_of_predictions': 1, 'correct_predictions': 0},
                    ]
