from settings import *


class Player:
    def __init__(self):
        self.balance = 1000.00
        self.bet_size = 10.00
        self.last_payout = 0.00
        self.total_won = 0.00
        self.total_wager = 0.00

    def get_data(self):
        pass

    def place_bet(self):
        bet = self.bet_size
        self.balance -= bet
        self.total_wager += bet
