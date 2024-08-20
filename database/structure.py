from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, async_sessionmaker
from sqlalchemy import BigInteger, String, ForeignKey

import os
from dotenv import load_dotenv


load_dotenv()
engine = create_async_engine(url=os.getenv('DB_URL'))
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key = True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(32))


class Tournament(Base):
    __tablename__ = 'tournaments'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    state: Mapped[str] = mapped_column(String(16))


class Match(Base):
    __tablename__ = 'matches'

    id: Mapped[int] = mapped_column(primary_key=True)
    tournament_id: Mapped[int] = mapped_column(ForeignKey('tournaments.id'))
    team_1: Mapped[str] = mapped_column(String(64))
    team_2: Mapped[str] = mapped_column(String(64))
    result: Mapped[int] = mapped_column()


class Predict(Base):
    __tablename__ = 'predictions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    match_id: Mapped[int] = mapped_column(ForeignKey('matches.id'))
    result: Mapped[int] = mapped_column()


""" class Leaderboard(Base):
    __tablename__ = 'leaderboard'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    correct_predictions: Mapped[int] = mapped_column()
    number_of_predictions: Mapped[int] = mapped_column() """

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)