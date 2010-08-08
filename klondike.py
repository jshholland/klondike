#!/usr/bin/env python
# A program to simulate the well-known game of Klondike (or Patience, or
# Solitaire, depending on your nationality

import random

ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
suits = ("C", "D", "S", "H")

class Card(object):
    def __init__(self, rank, suit, face_up=True):
        self.rank = rank
        self.suit = suit
        self.face_up = face_up

    def __str__(self):
        if self.face_up:
            return self.rank + self.suit
        else:
            return (self.rank + self.suit).lower()

    __repr__ = __str__

    rank_trans = dict((v, i) for (i, v) in enumerate(ranks))
    def __cmp__(self, other):
        return cmp(self.rank_trans[self.rank],
                   other.rank_trans[other.rank])

    def follows(self, other):
        if self < other:
            return False
        if self.suit != other.suit:
            return False
        if self.rank_trans[self.rank] - 1 == \
            other.rank_trans[other.rank]:
            return True
        return False

class Deck(object):
    def __init__(self, shuffled=True):
        self.data = [Card(rank, suit, False) for suit in suits for rank in ranks]
        if shuffled:
            self.shuffle()

    def __str__(self):
        return ', '.join(str(card) for card in self.data)

    __repr__ = __str__

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __contains__(self, item):
        return item in self.data

    def deal_card(self, face_up=True):
        card = self.data.pop()
        card.face_up = face_up
        return card

    def shuffle(self):
        random.shuffle(self.data)

class Tableau(object):
    def __init__(self, deck, num_piles=7):
        self.waste = []
        self.stock = []
        self.avail = []
        self.foundation = {}
        self.pile = [[] for num in range(num_piles)]
        for suit in suits:
            self.foundation[suit] = []

        iteration = num_piles
        while iteration:
            for num in range(iteration):
                self.pile[num].append(deck.deal_card(False))
            iteration -= 1
        self.stock = list(deck)
        self.turn_up()

    def __str__(self):
        return '\n'.join(["Stock (%d card(s)): %s" % (len(self.stock), self.stock),
                          "Face-up (%d card(s)): %s" % (len(self.avail), self.avail)] +
                         ["%s (%d card(s)): %s" % (suit, len(self.foundation[suit]), self.foundation[suit])
                             for suit in suits] +
                         ["Pile %d (%d card(s)): %s" % (num, len(pile), pile) for num, pile in
                              enumerate(self.pile)])

    __repr__ = __str__

    def turn_up(self):
        for card in self.avail:
            card.face_up = True

        for card in self.playable():
            card.face_up = True

    def playable(self):
        for pile in self.pile:
            if pile:
                yield pile[-1]
        if self.avail:
            yield self.avail[-1]

    def deal_stock(self, num=3):
        for i in range(num):
            try:
                card = self.stock.pop()
                card.face_up = True
                self.avail.append(card)
            except IndexError:
                pass

    def replace_stock(self):
        if self.stock:
            return
        self.stock = list(reversed(self.avail))
        self.avail[:] = []
        for card in self.stock:
            card.face_up = False

    def move_to_foundation(self, card):
        for pile in self.pile + [self.avail]:
            if pile and card == pile[-1]:
                del pile[-1]
                break
        self.foundation[card.suit].append(card)
        self.turn_up()

def solve(tableau, max_goes=5):
    goes_since_moving = 0
    def tidy():
        goes_since_moving = 0
        print
        print tableau
    while True:
        for card in tableau.playable():
            foundation = tableau.foundation[card.suit]
            if foundation and card.follows(foundation[-1]):
                tableau.move_to_foundation(card)
                tidy()
                break
            if not foundation and card.rank == 'A':
                tableau.move_to_foundation(card)
                tidy()
                break
        else:
            if tableau.stock:
                tableau.deal_stock()
                print
                print tableau
            elif goes_since_moving <= max_goes:
                tableau.replace_stock()
                print
                print tableau
                goes_since_moving += 1
            else:
                print "\nGave up!"
                break

if __name__ == '__main__':
    tab = Tableau(Deck())
    print tab
    solve(tab, 1)
