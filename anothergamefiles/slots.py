import random


class Slots:
    def __init__(self):
        self.sings = ["seven", "cherry", "lemon", "bar"]
        self.scoreboard = [[], [], []]

    def shuffle(self):
        for i in range(3):
            n = 0
            line = set()
            while n != 3:
                line = set([random.choice(self.sings) for _ in range(3)])
                n = len(line)
            index = 0
            for sing in line:
                self.scoreboard[index].append(sing)
                index += 1

        print(*self.scoreboard, sep="\n")

    def combinations(self):
        if self.scoreboard[0][0] == self.scoreboard[0][1] == self.scoreboard[0][2] and \
                self.scoreboard[1][0] == self.scoreboard[1][1] == self.scoreboard[1][2] and \
                self.scoreboard[2][0] == self.scoreboard[2][1] == self.scoreboard[2][2]:
            print("JACKPOT")
        elif self.scoreboard[1][0] == self.scoreboard[1][1] == self.scoreboard[1][2]:
            print("Win")
        elif self.scoreboard[1][0] == self.scoreboard[1][1] == self.scoreboard[1][2] == "seven":
            print("BIG WIN")
        else:
            print("Lose")


def main():
    s = Slots()
    s.shuffle()
    s.combinations()


if __name__ == '__main__':
    main()
