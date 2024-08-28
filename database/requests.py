from database.structure import async_session
from database.structure import User, Match, MatchOld, Predict, PredictOld, Tournament, TournamentOld, LeaderboardMain, LeaderboardTournament
from sqlalchemy import select, update, delete
import traceback


async def new_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id = tg_id, username = username))
            await session.commit()


async def new_predict(tg_id, match_id, tournament_id, result):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        predict = await session.scalar(select(Predict).where(Predict.match_id == match_id, Predict.user_id == user.id))
        
        if not predict:
            session.add(Predict(user_id = user.id, match_id = match_id, tournament_id = tournament_id, result = result))
        else:
            await session.execute(update(Predict).values(result = result).where(Predict.id == predict.id))
        await session.commit()


async def new_tournament(name):
    async with async_session() as session:
        tournament = await session.scalar(select(Tournament).where(Tournament.name == name))

        if not tournament:
            session.add(Tournament(name = name, is_open = False))
            await session.commit()
            return "Турнир добавлен!"
        return "Турнир уже существует!"
    

async def new_match(name, team1, team2):
    async with async_session() as session:
        try:
            tournament = await session.scalar(select(Tournament).where(Tournament.name == name))
            session.add(Match(tournament_id = tournament.id, team_1 = team1, team_2 = team2, result = 0))
            await session.commit()
            return "Матч добавлен!"
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())
            return "Что то пошло не так, попробуйте снова!"
        

async def new_predict_admin(tournament_name, username, predict, team1, team2):
    async with async_session() as session:
        try:
            user_id = await session.scalar(select(User.id).where(User.username == username))
            if not user_id:
                return "Пользователь не найден!"
            
            tournament_id = await session.scalar(select(Tournament.id).where(Tournament.name == tournament_name))
            match_id = await session.scalar(select(Match.id).where(Match.tournament_id == tournament_id).where(Match.team_1 == team1).where(Match.team_2 == team2))
            session.add(Predict(user_id = user_id, match_id = match_id, result = predict))
            await session.commit()
            return "Предикт добавлен!"
        except:
            return "Что то пошло не так, попробуйте снова!"



async def opened_tournaments():
    async with async_session() as session:
        return await session.scalars(select(Tournament).where(Tournament.is_open == True).order_by(Tournament.id.desc()))
    

async def closed_tournaments():
    async with async_session() as session:
        return await session.scalars(select(Tournament).where(Tournament.is_open == False).order_by(Tournament.id.desc()))


async def open_tournament(name):
    async with async_session() as session:
        await session.execute(update(Tournament).values(is_open = True).where(Tournament.name == name))
        await session.commit()
    

async def close_tournament(name):
    async with async_session() as session:
        await session.execute(update(Tournament).values(is_open = False).where(Tournament.name == name))
        await session.commit()


async def open_match(match_id):
    async with async_session() as session:
        await session.execute(update(Match).values(is_open = True).where(Match.id == match_id))
        await session.commit()


async def close_match(match_id):
    async with async_session() as session:
        await session.execute(update(Match).values(is_open = False).where(Match.id == match_id))
        await session.commit()


async def matches_to_predict(tournament_id):
    async with async_session() as session:
        return await session.scalars(select(Match).where(Match.result == 0).where(Match.tournament_id == tournament_id).where(Match.is_open == True).order_by(Match.id))


async def find_tournament_by_name(name):
    async with async_session() as session:
        return await session.scalar(select(Tournament).where(Tournament.name == name))
    

async def find_user_by_id(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))  
    

async def find_userid_by_tgid(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User.id).where(User.tg_id == tg_id))  


async def find_username_by_id(id):
    async with async_session() as session:
        return await session.scalar(select(User.username).where(User.id == id)) 
    

async def opened_matches():
    async with async_session() as session:
        return await session.scalars(select(Match).where(Match.result == 0))
    

async def get_match_pred(match_id):
    async with async_session() as session:
        return await session.scalars(select(Predict).where(Predict.match_id == match_id))


async def update_match(match_id, result):
    async with async_session() as session:
        await session.execute(update(Match).values(result = result).where(Match.id == match_id))
        predicts = await session.scalars(select(Predict).where(Predict.match_id == match_id))
        for pred in predicts:
            #update main leaderboard
            main_lead = await session.scalar(select(LeaderboardMain).where(LeaderboardMain.user_id == pred.user_id))
            result_of_predict = 1 if pred.result == result else 0
            if not main_lead:
                session.add(LeaderboardMain(user_id = pred.user_id, 
                                                  correct_predictions = result_of_predict,
                                                  number_of_predictions = 1))
            else:
                await session.execute(update(LeaderboardMain).values(correct_predictions = main_lead.correct_predictions + result_of_predict, number_of_predictions = main_lead.number_of_predictions + 1).where(LeaderboardMain.user_id == pred.user_id))
            
            #update tournament leaderboard
            match_ = await session.scalar(select(Match).where(Match.id == pred.match_id))
            tour_lead = await session.scalar(select(LeaderboardTournament).where(LeaderboardTournament.user_id == pred.user_id).where(LeaderboardTournament.tournament_id == match_.tournament_id))
            if not tour_lead:
                session.add(LeaderboardTournament(user_id = pred.user_id,
                                                  tournament_id = match_.tournament_id,
                                                  correct_predictions = result_of_predict,
                                                  number_of_predictions = 1))
            else:
                await session.execute(update(LeaderboardTournament).values(correct_predictions = tour_lead.correct_predictions + result_of_predict, number_of_predictions = tour_lead.number_of_predictions + 1).where(LeaderboardTournament.tournament_id == match_.tournament_id).where(LeaderboardTournament.user_id == pred.user_id))
        
        await session.commit()


async def get_tournaments():
    async with async_session() as session:
        return await session.scalars(select(Tournament).order_by(Tournament.id.desc()))
    

async def get_ongiong_tournaments():
    async with async_session() as session:
        return await session.scalars(select(Tournament.name).where(Tournament.time_state == 'Ongoing').order_by(Tournament.id.desc()))
 

async def get_ongiong_tournaments_nameid():
    async with async_session() as session:
        return await session.execute(select(Tournament.id, Tournament.name).where(Tournament.time_state == 'Ongoing').order_by(Tournament.id.desc()))


async def get_leaderboard(name):
    async with async_session() as session:
        tournament = await session.scalar(select(Tournament).where(Tournament.name == name))
        
        if not tournament:
            return await session.scalars(select(LeaderboardMain).join(User, User.id == LeaderboardMain.user_id).order_by(LeaderboardMain.correct_predictions.desc(), LeaderboardMain.number_of_predictions, User.username))
        
        return await session.scalars(select(LeaderboardTournament).join(User, User.id == LeaderboardTournament.user_id).where(LeaderboardTournament.tournament_id == tournament.id).order_by(LeaderboardTournament.correct_predictions.desc(), LeaderboardTournament.number_of_predictions, User.username))


async def get_user_by_id(id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.id == id))
    

async def open_check(tournament_id):
    async with async_session() as session:
        tournament = await session.scalar(select(Tournament).where(Tournament.id == tournament_id).where(Tournament.is_open == True))

        if not tournament:
            return False
        return True
    

async def find_tournamentid_by_matchid(match_id):
    async with async_session() as session:
        return await session.scalar(select(Match.tournament_id).where(Match.id == match_id))


async def  get_mainleaderboard():
    async with async_session() as session:
        return await session.scalars(select(LeaderboardMain).join(User, User.id == LeaderboardMain.user_id).order_by(LeaderboardMain.correct_predictions.desc(), LeaderboardMain.number_of_predictions, User.username))
    

async def  get_tournamentleaderboard(tournament_id):
    async with async_session() as session:
        return await session.scalars(select(LeaderboardTournament).join(User, User.id == LeaderboardTournament.user_id).where(LeaderboardTournament.tournament_id == tournament_id).order_by(LeaderboardTournament.correct_predictions.desc(), LeaderboardTournament.number_of_predictions, User.username))


async def get_tournament_name_by_id(id):
    async with async_session() as session:
        return await session.scalar(select(Tournament.name).where(Tournament.id == id))
    

async def get_tournament_id_by_name(name):
    async with async_session() as session:
        return await session.scalar(select(Tournament.id).where(Tournament.name == name))


async def get_users_id():
    async with async_session() as session:
        return await session.scalars(select(User.tg_id))
    

async def get_predict_by_ids(user_id, match_id):
    async with async_session() as session:
        return await session.scalar(select(Predict.result).where(Predict.user_id == user_id).where(Predict.match_id == match_id))


async def get_predict_by_uidtid(user_id, tournament_id):
    async with async_session() as session:
        preds = await session.scalars(select(Predict.id).where(Predict.user_id == user_id).where(Predict.tournament_id == tournament_id))
        


async def get_open_matches_by_tournament_name(tournament_name):
    async with async_session() as session:
        tournament_id = await get_tournament_id_by_name(tournament_name)
        return await session.execute(select(Match.id, Match.team_1, Match.team_2).where(Match.tournament_id == tournament_id).where(Match.result == 0))


async def get_id_nc_matches_by_tid(tournament_id):
    async with async_session() as session:
        return await session.scalars(select(Match.id).where(Match.tournament_id == tournament_id).where(Match.result == 0))
    

async def get_predicted_matches_bytid(tournament_id):
    async with async_session() as session:
        return await session.execute(select(Match.id, Match.team_1, Match.team_2).where(Match.tournament_id == tournament_id).where(Match.result == 0))


async def get_predict_by_uidmid(user_id, match_id):
    async with async_session() as session:
        return await session.scalar(select(Predict.result).where(Predict.user_id == user_id).where(Predict.match_id == match_id))


async def get_closed_matches(tournament_id):
    async with async_session() as session:
        return await session.execute(select(Match.id, Match.team_1, Match.team_2).where(Match.tournament_id == tournament_id).where(Match.is_open == False).order_by(Match.id.desc()))


async def get_opened_matches(tournament_id):
    async with async_session() as session:
        return await session.execute(select(Match.id, Match.team_1, Match.team_2).where(Match.tournament_id == tournament_id).where(Match.is_open == True).order_by(Match.id.desc()))


async def get_tournament_id_by_match(match_id):
    async with async_session() as session:
        return await session.scalar(select(Match.tournament_id).where(Match.id == match_id))


async def migrate_data():
    async with async_session() as session:
        #migrate tournaments
        pass
        """ tournaments = await session.scalars(select(TournamentOld))

        for tournament in tournaments:
            is_open = True if tournament.state == 'Open' else False
            session.add(Tournament(id = tournament.id, 
                                         name = tournament.name, 
                                         is_open = is_open, 
                                         time_state = 'Past'))
        await session.commit() """

        #migrate matches

        """ matches = await session.scalars(select(MatchOld))

        for match_ in matches:
            session.add(Match(id = match_.id,
                                         tournament_id = match_.tournament_id,
                                         team_1 = match_.team_1,
                                         team_2 = match_.team_2,  
                                         is_open = False, 
                                         result = match_.result))
        
        await session.commit() """

        #migrate predicts

        """ predicts = await session.scalars(select(PredictOld))

        for pred in predicts:
            tournament_id = await get_tournament_id_by_match(pred.match_id)
            session.add(Predict(id = pred.id,
                                         user_id = pred.user_id,
                                         match_id = pred.match_id,
                                         tournament_id = tournament_id,
                                         result = pred.result))
        
        await session.commit() """


async def fill_texts():
    async with async_session() as session:
        #migrate tournaments
        pass


async def predict_matches_check(tournament_id):
    async with async_session() as session:
        count_matches = len(list(await session.scalars(select(Match.id).where(Match.result == 0).where(Match.tournament_id == tournament_id).where(Match.is_open == True).order_by(Match.id))))

        if count_matches == 0:
            return False
        return True