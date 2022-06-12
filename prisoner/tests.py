from otree.api import Currency as cu, currency_range
from . import *
from otree.api import Bot

import random


#class PlayerBot(Bot):
#    def play_round(self):
#        yield (Introduction)
#        yield (Decision, {"decision": 'Cooperate'})
#        assert 'Both of you chose to Cooperate' in self.html
#        assert self.player.payoff == C.BOTH_COOPERATE_PAYOFF
#        yield (Results)

class PlayerBot(Bot):
    def play_round(self):
        if self.subsession.round_number == 1:
            yield (Instructions_1)
            yield (Instructions_2)
            yield (Instructions_3)
            if random.uniform(0, 1) > 0.5:
                yield (Decision, {"decision": 'Action 1'})
                yield (Results)
                yield (EndRound)
            else:
                yield (Decision, {"decision": 'Action 2'})
                yield (Results)
                yield (EndRound)

        else:
            if random.uniform(0, 1) > 0.5:
                yield (Decision, {"decision": 'Action 1'})
                yield (Results)
                yield (EndRound)
            else:
                yield (Decision, {"decision": 'Action 2'})
                yield (Results)
                yield (EndRound)