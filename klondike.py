#!/usr/bin/env python
# A program to simulate the well-known game of Klondike (or Patience, or
# Solitaire, depending on your nationality

import random

ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
suits = ("C", "D", "S", "H")

class Card(object):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return self.rank + self.suit

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

def make_deck():
    deck = []
    for rank in ranks:
        for suit in suits:
            deck.append(Card(rank, suit))
    random.shuffle(deck)
    return deck
