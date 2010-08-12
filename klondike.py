#!/usr/bin/env python
"""
A program to simulate the well-known game of Klondike (or Patience, or
Solitaire, depending on your nationality)
"""

import random

ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
suits = ("C", "D", "S", "H")

class Card(object):
    """
    Class to represent a single playing card. Keeps track of suit, rank and
    colour as well as whether it is face-up or not. A face-up card is printed
    out in capitals, a face down one in lower case.
    """

    def __init__(self, rank, suit, face_up=True):
        """
        Initialise a Card with its rank and suit. Works out colour based on
        alternating colours in the suits list.
        """
        self.rank = rank
        self.suit = suit
        self.face_up = face_up

        blacks = suits[::2]
        reds = suits[1::2]
        if self.suit in blacks:
            self.colour = "B"
        elif self.suit in reds:
            self.colour = "R"

    def __str__(self):
        if self.face_up:
            return self.rank + self.suit
        else:
            return (self.rank + self.suit).lower()

    __repr__ = __str__

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    _rank_trans = dict((v, i) for (i, v) in enumerate(ranks))
    def __cmp__(self, other):
        return cmp(self._rank_trans[self.rank],
                   other._rank_trans[other.rank])

    def follows(self, other):
        """
        Predicate to tell whether self follows other (in terms of foundation
        piles).
        """
        if self < other:
            return False
        if self.suit != other.suit:
            return False
        if self._rank_trans[self.rank] - 1 == \
            other._rank_trans[other.rank]:
            return True
        return False

    def can_go_on(self, other):
        """
        Predicate to tell whether self can be placed on top of another within
        the tableau.
        """
        if self.colour == other.colour:
            return False
        if self._rank_trans[self.rank] + 1 == \
            other._rank_trans[other.rank]:
            return True
        return False

class Deck(object):
    """
    Class to represent a deck made out of cards. Builds a deck out of each
    possible combination of suit and rank face-down. Will shuffle the deck
    using the random.shuffle function from the Python standard library
    according to the shuffled argument passed in.
    """

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
        """
        Remove the last card from the deck and return it (face-up according to
        the argument passed in.
        """
        card = self.data.pop()
        card.face_up = face_up
        return card

    def shuffle(self):
        """
        Shuffle the deck.
        """
        random.shuffle(self.data)

class Tableau(object):
    """
    Represent the tableau in a game of patience. Ideally supposed to be as
    modifiable as possible, but there is a little bit of hard-coded values in
    there.
    """

    def __init__(self, deck, num_piles=7):
        """
        Initialise the tableau with a given deck and number of piles.
        """
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
        """
        Turn all the available cards in the tableau face up.
        """
        for card in self.avail:
            card.face_up = True

        for card in self.playable():
            card.face_up = True

    def playable(self):
        """
        Iterate on all the playable cards in the tableau.
        """
        for pile in self.pile:
            if pile:
                yield pile[-1]
        if self.avail:
            yield self.avail[-1]

    def deal_stock(self, num=3):
        """
        Deal off (at most, if the deck is nearly empty) num cards from the
        stock onto the waste pile.
        """
        for i in range(num):
            try:
                card = self.stock.pop()
                card.face_up = True
                self.avail.append(card)
            except IndexError:
                pass

    def replace_stock(self):
        """
        Replace the stock by turning the waste pile upside down. Null operation
        if there are still cards in the stock.
        """
        if self.stock:
            return
        self.stock = list(reversed(self.avail))
        self.avail[:] = []
        for card in self.stock:
            card.face_up = False

    def _find_and_delete(self, card):
        """
        Utility method to find and delete a card playable from the tableau
        (usually as a precursor to putting a copy somewhere else).
        """
        for pile in self.pile + [self.avail]:
            if pile and card == pile[-1]:
                del pile[-1]
                break

    def move_to_foundation(self, card):
        """
        Move the given card to the relevant foundation pile.
        """
        self._find_and_delete(card)
        self.foundation[card.suit].append(card)
        self.turn_up()

    def move_onto(self, card, other_card):
        """
        Move a single card onto another face-up card in the tableau.
        """
        # Don't use self._find_and_delete so we can find the one we're
        # moving onto in the same iteration.
        for pile in self.pile + [self.avail]:
            if pile and card == pile[-1]:
                del pile[-1]
            if pile and other_card == pile[-1]:
                pile.append(card)
        self.turn_up()

    def move_to_empty(self, card):
        """
        Move a card onto an empty pile in the tableau.
        """
        first_empty = filter(lambda l: not l, self.pile)[0]
        self._find_and_delete(card)
        first_empty.append(card)
        self.turn_up()

def solve(tableau, max_goes=5):
    """
    Solver function for standard patience. Gives up after max_goes times
    through the stock without moving anything.
    """
    goes_since_moving = 0
    def _tidy():
        goes_since_moving = 0
        print
        print tableau
    while True:
        for card in tableau.playable():
            foundation = tableau.foundation[card.suit]
            if foundation and card.follows(foundation[-1]):
                tableau.move_to_foundation(card)
                _tidy()
                break
            if not foundation and card.rank == 'A':
                tableau.move_to_foundation(card)
                _tidy()
                break
            if card.rank == 'K' and not all(tableau.pile):
                tableau.move_to_empty(card)
                _tidy()
                break
            for other_card in (pile[-1] for pile in tableau.pile if pile):
                if card.can_go_on(other_card):
                    tableau.move_onto(card, other_card)
                    _tidy()
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
