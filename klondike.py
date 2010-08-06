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

    def __repr__(self):
        if self.face_up:
            return self.rank + self.suit
        else:
            return (self.rank + self.suit).lower()

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

    def __repr__(self):
        return ', '.join(str(card) for card in self.data)

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


if __name__ == '__main__':
    from pprint import pprint as pp
    deck = Deck()
    pp(deck)
