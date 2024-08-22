from database.structure import async_session
from database.structure import User, Match, Predict, Tournament, LeaderboardMain, LeaderboardTournament
from sqlalchemy import select, update, delete


async def new_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id = tg_id, username = username))
            await session.commit()


async def new_predict(tg_id, match_id, result):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        predict = await session.scalar(select(Predict).where(Predict.match_id == match_id, Predict.user_id == user.id))
        
        if not predict:
            session.add(Predict(user_id = user.id, match_id = match_id, result = result))
        else:
            await session.execute(update(Predict).values(result = result).where(Predict.id == predict.id))
        await session.commit()


async def new_tournament(name):
    async with async_session() as session:
        tournament = await session.scalar(select(Tournament).where(Tournament.name == name))

        if not tournament:
            session.add(Tournament(name = name, state = 'Close'))
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
        except:
            return "Турнир не найден, попробуйте снова!"


async def opened_tournaments():
    async with async_session() as session:
        return await session.scalars(select(Tournament).where(Tournament.state == 'Open'))
    

async def closed_tournaments():
    async with async_session() as session:
        return await session.scalars(select(Tournament).where(Tournament.state == 'Close'))


async def open_tournament(name):
    async with async_session() as session:
        await session.execute(update(Tournament).values(state = "Open").where(Tournament.name == name))
        await session.commit()
    

async def close_tournament(name):
    async with async_session() as session:
        await session.execute(update(Tournament).values(state = "Close").where(Tournament.name == name))
        await session.commit()


async def matches_to_predict(tournament_id):
    async with async_session() as session:
        return await session.scalars(select(Match).where((Match.result == 0) & (Match.tournament_id == tournament_id)).order_by(Match.id))
    

async def check_predict(tournament_id):
    async with async_session() as session:
        return await session.scalars(select(Match).where((Match.result == 0) & (Match.tournament_id == tournament_id)).order_by(Match.id))


async def find_tournament_by_name(name):
    async with async_session() as session:
        return await session.scalar(select(Tournament).where(Tournament.name == name))
    

async def find_user_by_id(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))  


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
            tour_lead = await session.scalar(select(LeaderboardTournament).where(LeaderboardTournament.user_id == pred.user_id))
            match_ = await session.scalar(select(Match).where(Match.id == pred.match_id))
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
        return await session.scalars(select(Tournament))
    

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
        tournament = await session.scalar(select(Tournament).where(Tournament.id == tournament_id).where(Tournament.state == 'Open'))

        if not tournament:
            return False
        return True