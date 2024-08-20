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
        predict = await session.scalar(select(Predict).where(Predict.match_id == match_id))

        if not predict:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            session.add(Predict(user_id = user.id, match_id = match_id, result = result))
        else:
            await session.execute(update(Predict).values(result = result).where(Predict.id == predict.id))
        await session.commit()


async def new_tournament(tg_id, match_id, result):
    async with async_session() as session:
        predict = await session.scalar(select(Predict).where(Predict.match_id == match_id))

        if not predict:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            """ session.add(Predict(user_id = user.id))
            session.add(Predict(match_id = match_id))
            session.add(Predict(result = result)) """
            await session.commit()
        else:
            await session.execute(update(Predict).values(result = result).where(Predict.id == predict.id))



async def ongoing_tournaments():
    async with async_session() as session:
        return await session.scalars(select(Tournament).where(Tournament.state == 'Open'))
    

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
