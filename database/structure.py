from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, async_sessionmaker
from sqlalchemy import BigInteger, String, ForeignKey, SmallInteger, Text, Date, DateTime, Boolean

import datetime
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
    username: Mapped[str] = mapped_column(String(64), insert_default = '#Unknown#')


class TournamentOld(Base):
    __tablename__ = 'tournaments'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    state: Mapped[str] = mapped_column(String(16))


class Tournament(Base):
    __tablename__ = 'new_tournaments'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    is_open = mapped_column(Boolean(), insert_default = False)
    open_date = mapped_column(Date(), nullable = True)
    close_date = mapped_column(Date(), nullable = True)
    time_state: Mapped[str] = mapped_column(String(16), insert_default = 'In future')


class MatchOld(Base):
    __tablename__ = 'matches'

    id: Mapped[int] = mapped_column(primary_key=True)
    tournament_id: Mapped[int] = mapped_column(ForeignKey('tournaments.id'))
    team_1: Mapped[str] = mapped_column(String(64))
    team_2: Mapped[str] = mapped_column(String(64))
    result: Mapped[int] = mapped_column()


class Match(Base):
    __tablename__ = 'new_matches'

    id: Mapped[int] = mapped_column(primary_key=True)
    tournament_id: Mapped[int] = mapped_column(ForeignKey('new_tournaments.id'))
    team_1: Mapped[str] = mapped_column(String(64))
    team_2: Mapped[str] = mapped_column(String(64))
    start_datetime = mapped_column(DateTime(), nullable = True)
    is_open = mapped_column(Boolean(), insert_default = False)
    result = mapped_column(SmallInteger(), insert_default = 0)


class PredictOld(Base):
    __tablename__ = 'predictions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    match_id: Mapped[int] = mapped_column(ForeignKey('matches.id'))
    #tournament_id: Mapped[int] = mapped_column(ForeignKey('tournaments.id'))
    result: Mapped[int] = mapped_column()


class Predict(Base):
    __tablename__ = 'new_predictions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    match_id: Mapped[int] = mapped_column(ForeignKey('new_matches.id'))
    tournament_id: Mapped[int] = mapped_column(ForeignKey('new_tournaments.id'))
    date = mapped_column(DateTime(), nullable = True)
    result = mapped_column(SmallInteger())


class LeaderboardMain(Base):
    __tablename__ = 'all_leaderboard'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    correct_predictions: Mapped[int] = mapped_column()
    number_of_predictions: Mapped[int] = mapped_column()


""" class LeaderboardTournamentOld(Base):
    __tablename__ = 'leaders_by_tour'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    tournament_id: Mapped[int] = mapped_column(ForeignKey('tournaments.id'))
    correct_predictions: Mapped[int] = mapped_column()
    number_of_predictions: Mapped[int] = mapped_column()
 """

class LeaderboardTournament(Base):
    __tablename__ = 'new_leaders_by_tour'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    tournament_id: Mapped[int] = mapped_column(ForeignKey('new_tournaments.id'))
    correct_predictions: Mapped[int] = mapped_column()
    number_of_predictions: Mapped[int] = mapped_column()


class TextOfTop(Base):
    __tablename__ = 'texts_for_tops'

    id: Mapped[int] = mapped_column(primary_key=True)
    tournament_id: Mapped[int] = mapped_column(ForeignKey('tournaments.id'))
    text = mapped_column(Text())
      

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
