#!/usr/bin/env python
# A program to simulate the well-known game of Klondike (or Patience, or
# Solitaire, depending on your nationality

import copy

ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
suits = ("C", "D", "S", "H")

class Card(object):
    def __init__(self, rank, suit, face_up=True):
        self.rank = rank
        self.suit = suit
        self.face_up = face_up

    def __repr__(self):
        if self.face_up:
            return self.rank + self.suit
        else:
            return (self.rank + self.suit).lower()

    rank_trans = dict([(v, i) for (i, v) in enumerate(ranks)])
    def __cmp__(self, other):
        return cmp(self.__class__.rank_trans[self.rank],
                   other.__class__.rank_trans[other.rank])

    def follows(self, other):
        if self < other:
            return False
        if self.suit != other.suit:
            return False
        if self.__class__.rank_trans[self.rank] - 1 == \
            other.__class__.rank_trans[other.rank]:
            return True
        return False

def make_deck(face_up=False):
    return [Card(rank, suit, face_up) for suit in suits for rank in ranks]

def turn_up(tableau):
    for pile in range(7) + ['waste']:
        try:
            tableau[pile][-1].face_up = True
        except IndexError:
            pass

def deal(deck):
    deck = copy.deepcopy(deck)
    tableau = {}
    for suit in suits:
        tableau[suit] = []
    for pile_num in range(7):
        tableau[pile_num] = []
    tableau['stock'] = []
    tableau['waste'] = []

    start = 0
    while start < 7:
        for pile in range(start, 7):
            tableau[pile].append(deck.pop())
        start += 1
    tableau['stock'] = deck
    turn_up(tableau)
    return tableau

if __name__ == '__main__':
    from random import shuffle
    from pprint import pprint as pp
    deck = make_deck()
    shuffle(deck)
    tab = deal(deck)
    pp(tab)
