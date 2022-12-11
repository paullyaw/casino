import random
import main as mn

class Deck:
    def __init__(self):
        self.players = input()
        self.cards = []
        self.table = []
        self.bank = 0
        ranks = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}
        suits = {'Hearts', 'Diamonds', 'Spades', 'Clubs'}
        for card in ranks:
            for suit in suits:
                self.cards.append((card, suit))

    def shuffle(self):
        random.shuffle(self.cards)
        pass

    def tabledeck(self):
        ur_cards = self.cards[0], self.cards[0]
        self.cards.remove(self.cards[0])
        self.cards.remove(self.cards[0])
        print(ur_cards)
        k = 3
        while k <= 5:
            bet = input()
            if bet == 'check':
                print(self.bank)
                pass
            elif bet == 'bet':
                last = int(input())
                self.bank += last
            elif bet == 'raise':
                last = last * int(input())
                self.bank += last
                print(self.bank)
            elif bet == 'call':
                self.bank += last
                print(self.bank)
            elif bet == 'fold':
                break
            if k == 3:
                self.table.append(self.cards[0])
                self.table.append(self.cards[1])
                self.table.append(self.cards[2])
                self.cards.remove(self.cards[0])
                self.cards.remove(self.cards[0])
                self.cards.remove(self.cards[0])
                print(self.table)
                k += 1
            else:
                self.table.append(self.cards[0])
                self.cards.remove(self.cards[0])
                print(self.table)
                k += 1


def main():
    d = Deck()
    d.shuffle()
    d.tabledeck()
    mn.Combo(d)
    pass


if __name__ == '__main__':
    main()
