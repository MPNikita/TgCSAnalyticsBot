from database.structure import async_session
from database.structure import User, Match, Predict, Tournament
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
            session.add(Tournament(name = name, state = 'Open'))
            await session.commit()
            return "Tournament made!"
        return "Tournament exists!"
    

async def new_match(name, team1, team2):
    async with async_session() as session:
        try:
            tournament = await session.scalar(select(Tournament).where(Tournament.name == name))
            session.add(Match(tournament_id = tournament.id, team_1 = team1, team_2 = team2, result = 0))
            await session.commit()
            return "Match Added"
        except:
            return "Wrong tournament!!! Try again"


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
