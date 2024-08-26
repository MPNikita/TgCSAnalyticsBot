from aiogram.fsm.state import State, StatesGroup


class Predict(StatesGroup):
    show_tournament = State()
    make_predict = State()


class TournamentCreation(StatesGroup):
    name = State()


class MatchCreation(StatesGroup):
    team1 = State()
    team2 = State()
    creation = State()


class OpenPredicts(StatesGroup):
    open_ = State()


class ClosePredicts(StatesGroup):
    close_ = State()


class MatchStats(StatesGroup):
    stats = State()


class MatchUpdate(StatesGroup):
    show_stats = State()
    match_upd = State()


class ShowLeaders(StatesGroup):
    show_lead = State()
    show_tournaments = State()


class Broadcast(StatesGroup):
    got_msg = State()
    confirm = State()


class AdminMakePredict(StatesGroup):
    tournament_name = State()
    making = State()

class ShowPredicts(StatesGroup):
    got_tournament = State()
