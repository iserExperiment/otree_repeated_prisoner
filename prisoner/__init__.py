import random
import time

import numpy as np
from otree.api import *


doc = """
This is a one-shot "Prisoner's Dilemma". Two players are asked separately
whether they want to cooperate or defect. Their choices directly determine the
payoffs.
"""


class C(BaseConstants):
    NAME_IN_URL = 'prisoner'
    PLAYERS_PER_GROUP = 2
    CONVERSION_RATE = 1 / 150  # $0.006 for every point scored in Dal Bo and Frechette AER 2011

    INSTRUCTIONS_TEMPLATE = 'prisoner/instructions.html'

    TIME_LIMIT = False
    TIME_LIMIT_SECONDS = 3600  # time limit for session (in seconds) since first round of first match (3600 in Dal Bo and Frechette AER 2011)

    # payoff if 1 player defects and the other cooperates""",
    BETRAY_PAYOFF = 50
    BETRAYED_PAYOFF = 12

    # payoff if both players cooperate or both defect
    BOTH_COOPERATE_PAYOFF = 32  # one of two treatments in Dal Bo & Frechette AER 2011; values: 32, 40, 48
    BOTH_DEFECT_PAYOFF = 25

    DELTA = 0.50  # one of two treatments in Dal Bo & Frechette AER 2011; values: 0.50, 0.75
    NUM_MATCHES = 1  # set to high number (e.g., 50) if TIME_LIMIT == True
    MATCH_DURATION = np.random.geometric(
        p = (1 - DELTA),
        size = NUM_MATCHES
    )
    # the first argument here is the probability the match ends after each round (i.e., 1 - \DELTA); the second argument is the number of matches. For documentation, see: https://docs.scipy.org/doc/numpy-1.14.1/reference/generated/numpy.random.geometric.html

    NUM_ROUNDS = int(np.sum(MATCH_DURATION))

    LAST_ROUNDS = np.cumsum(MATCH_DURATION)
    LAST_ROUND = int(LAST_ROUNDS[-1])
    FIRST_ROUNDS = [1]
    for k in range(1, len(MATCH_DURATION)):
        FIRST_ROUNDS.append(int(LAST_ROUNDS[k - 1] + 1))


class Subsession(BaseSubsession):
    match_number = models.IntegerField()
    round_in_match_number = models.IntegerField()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    decision = models.StringField(
        choices=['Action 1', 'Action 2'],
        doc="""This player's decision""",
        # widget=widgets.RadioSelect,
    )


# FUNCTIONS
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        subsession.session.start_time = time.time()
        subsession.session.alive = True

    k = 0
    while k < len(C.LAST_ROUNDS):
        if subsession.round_number <= C.LAST_ROUNDS[k]:
            subsession.match_number = k + 1
            k = len(C.LAST_ROUNDS)
        else:
            k += 1

    subsession.round_in_match_number = subsession.round_number - C.FIRST_ROUNDS[subsession.match_number - 1] + 1

    if subsession.round_number in C.FIRST_ROUNDS:
        subsession.group_randomly()
    else:
        subsession.group_like_round(subsession.round_number - 1)


def other_player(player: Player) -> Player:
    return player.get_others_in_group()[0]


def set_payoff(player: Player):
    payoff_matrix = {
        'Action 1': {
            'Action 1': C.BOTH_COOPERATE_PAYOFF,
            'Action 2': C.BETRAYED_PAYOFF,
        },
        'Action 2': {
            'Action 1': C.BETRAY_PAYOFF,
            'Action 2': C.BOTH_DEFECT_PAYOFF
        },
    }

    player.payoff = payoff_matrix[player.decision][other_player(player).decision]


# PAGES
class Introduction(Page):
    # timeout_seconds = 100

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1


class Instructions_1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1


class Instructions_2(Page):
    @staticmethod
    def vars_for_template(player: Player):
        continuation_chance = int(round(C.DELTA * 100))
        return dict(
            continuation_chance=continuation_chance,
            die_threshold_plus_one=continuation_chance + 1,
        )

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1


class Instructions_3(Page):
    @staticmethod
    def vars_for_template(player: Player):
        continuation_chance = int(round(C.DELTA * 100))
        return dict(
            continuation_chance=continuation_chance,
            die_threshold_plus_one=continuation_chance + 1,
        )

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1


class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            set_payoff(p)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        me = player
        opponent = other_player(me)
        return {
            'my_decision': me.decision,
            'opponent_decision': opponent.decision,
            'same_choice': me.decision == opponent.decision,
            'both_cooperate': me.decision == "Action 1" and opponent.decision == "Action 1",
            'both_defect': me.decision == "Action 2" and opponent.decision == "Action 2",
            'i_cooperate_he_defects': me.decision == "Action 1" and opponent.decision == "Action 2",
            'i_defect_he_cooperates': me.decision == "Action 2" and opponent.decision == "Action 1",
        }


class EndRound(Page):
    # timeout_seconds = 100

    @staticmethod
    def vars_for_template(player: Player):
        continuation_chance = int(round(C.DELTA * 100))

        if player.subsession.round_number in C.LAST_ROUNDS:
            dieroll = random.randint(continuation_chance + 1, 100)
        else:
            dieroll = random.randint(1, continuation_chance)

        return dict(
            dieroll=dieroll,
            continuation_chance=continuation_chance,
            die_threshold_plus_one=continuation_chance + 1,
        )


class EndWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        elapsed_time = time.time() - subsession.session.start_time

        if (
            C.TIME_LIMIT == True
            and
            elapsed_time > C.TIME_LIMIT_SECONDS
            and
            subsession.round_number in C.LAST_ROUNDS
        ):
            subsession.session.alive = False


class End(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (
            player.session.alive == False
            or
            player.subsession.round_number == C.LAST_ROUND
        )


page_sequence = [
    Introduction,
    Instructions_1,
    Instructions_2,
    Instructions_3,
    Decision,
    ResultsWaitPage,
    Results,
    EndRound,
    EndWaitPage,
    End,
]
