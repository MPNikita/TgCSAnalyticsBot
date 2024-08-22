import database.requests as rq

async def update_text_tops(match_id):
    match_ = await rq.find_tournamentid_by_matchid(match_id)
    
    #update main_top
    top = await rq.get_mainleaderboard()
    top_text = "Мощнейший всеобщий топ\n"

    place = 0
    coun = 0
    prev_num = 0
    prev_corr = 0
    flag = False

    for user_top in top:
        wr = user_top.correct_predictions / user_top.number_of_predictions * 100
        if not flag:
            prev_num = user_top.number_of_predictions
            prev_corr = user_top.correct_predictions
            flag = True
            place += 1
        place += 1
        coun += 1
        if prev_num == user_top.number_of_predictions and prev_corr == user_top.correct_predictions:
            place -= 1
        elif place != coun:
            place = coun
        top_str = f'{place}. @{user_top.username} {user_top.correct_predictions}/{user_top.number_of_predictions} {wr:.2f}%\n'
        top_text += top_str
        prev_num = user_top.number_of_predictions
        prev_corr = user_top.correct_predictions
    
    with open('tops/main_top.txt', 'w+') as f:
        f.write(top_text)
    
    #update tournament_top
    tournament = await rq.get_tournament_name_by_id(match_id)

    top = await rq.get_tournamentleaderboard(match_.tournament_id)
    top_text = f"Мощнейший топ {tournament.name}\n"

    place = 0
    coun = 0
    prev_num = 0
    prev_corr = 0
    flag = False

    for user_top in top:
        wr = user_top.correct_predictions / user_top.number_of_predictions * 100
        if not flag:
            prev_num = user_top.number_of_predictions
            prev_corr = user_top.correct_predictions
            flag = True
            place += 1
        place += 1
        coun += 1
        if prev_num == user_top.number_of_predictions and prev_corr == user_top.correct_predictions:
            place -= 1
        elif place != coun:
            place = coun
        top_str = f'{place}. @{user_top.username} {user_top.correct_predictions}/{user_top.number_of_predictions} ({wr:.2f})%\n'
        top_text += top_str
        prev_num = user_top.number_of_predictions
        prev_corr = user_top.correct_predictions

    name = tournament.name
    name = name.replace(' ', '_')
    with open(f'tops/{name}_top.txt', 'w+') as f:
        f.write(top_text)