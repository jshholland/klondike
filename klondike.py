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
        self.data = [Card(rank, suit) for suit in suits for rank in ranks]
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

    def deal_card(self):
        card = self.data.pop()
        card.face_up = True
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
                self.pile[num].append(deck.deal_card())
            iteration -= 1
        self.stock = list(deck)

    def __str__(self):
        return '\n'.join(["Stock (%d card(s)): %s" % (len(self.stock), self.stock),
                          "Face-up (%d card(s)): %s" % (len(self.avail), self.avail)] +
                         ["%s (%d card(s)): %s" % (suit, len(self.foundation[suit]), self.foundation[suit])
                             for suit in suits] +
                         ["Pile %d (%d card(s)): %s" % (num, len(pile), pile) for num, pile in
                              enumerate(self.pile)])

    __repr__ = __str__


if __name__ == '__main__':
    tab = Tableau(Deck())
    print tab
