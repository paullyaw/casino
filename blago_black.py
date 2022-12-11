from random import shuffle


class blackjack:
    def __init__(self):
        self.cards = []
        self.table = []
        self.bank = 0
        self.player_cards = []
        self.pl_sum = 0
        self.dl_sum = 0
        self.dealer_cards = ''
        self.fl = True
        ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        suits = {'Hearts', 'Diamonds', 'Spades', 'Clubs'}
        for card in ranks:
            for suit in suits:
                self.cards.append((card, suit))

    def cardshuffle(self):
        shuffle(self.cards)

    def tabledeck(self):
        self.player_cards = [self.cards[0], self.cards[1]]
        self.cards.remove(self.cards[0])
        self.cards.remove(self.cards[0])
        print(self.player_cards)
        self.dealer_cards = self.cards[0], self.cards[1]
        self.cards.remove(self.cards[0])
        self.cards.remove(self.cards[0])
        print('dealer: X,', self.dealer_cards[1])
        self.dl_sum = self.dealer_cards[0][0] + self.dealer_cards[1][0]
        self.pl_sum = self.player_cards[0][0] + self.player_cards[1][0]

    def game(self):
        jk = jack_combo(self.cards, self.pl_sum, self.dl_sum, self.player_cards, self.dealer_cards)
        while self.fl:
            self.fl = jk.double()
            move = input()
            if move == 'stand':
                self.fl = jk.stand()
            elif move == 'hit':
                self.fl = jk.hit()


class jack_combo():
    def __init__(self, cards, plsum, dlsum, plcard, dlcard):
        self.cards = cards
        self.pl_sum = plsum
        self.dl_sum = dlsum
        self.player_cards = plcard
        self.dealer_cards = dlcard

    def double(self):
        if self.player_cards[0][0] == self.player_cards[1][0]:
            print('double?')
            ans = input()
            if ans == 'yes':
                self.player_cards.append(self.cards[0])
                self.pl_sum += self.cards[0][0]
                self.cards.remove(self.cards[0])
                print(self.player_cards)
                print('dealer:', self.dealer_cards)
                if self.pl_sum > 21:
                    print('perebor, dealer wins')
                    return False
                elif self.dl_sum > self.pl_sum:
                    print('dealer wins')
                    return False
                elif self.pl_sum > self.dl_sum:
                    print('you win')
                    return False
                else:
                    print('draw')
                    return False
            else:
                return True

    def hit(self):
        self.player_cards.append(self.cards[0])
        self.pl_sum += self.cards[0][0]
        self.cards.remove(self.cards[0])
        print(self.player_cards)
        if self.pl_sum > 21:
            print('perebor, dealer wins')
            return False
        else:
            return True

    def stand(self):
        print(self.dealer_cards)
        print(self.player_cards)
        if self.dl_sum > self.pl_sum:
            print('dealer wins')
            return False
        elif self.pl_sum > self.dl_sum:
            print('you win')
            return False
        else:
            print('draw')
            return False


b = blackjack()
b.cardshuffle()
b.tabledeck()
b.game()
