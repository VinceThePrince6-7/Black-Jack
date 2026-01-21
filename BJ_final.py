import random
from dataclasses import dataclass

# ==================================================
# TOGGLE CARD COUNTING HERE
# ==================================================
USE_CARD_COUNTING = False  # True = counting agent, False = baseline agent

# ==================================================
# GAME SETTINGS
# ==================================================
NUM_DECKS = 1
MIN_CARDS_BEFORE_SHUFFLE = 11

CARDS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

# ==================================================
# DECK
# ==================================================
def create_shoe():
    shoe = []
    for _ in range(NUM_DECKS):
        for c in CARDS:
            shoe += [c] * 4
    random.shuffle(shoe)
    return shoe

def draw(shoe):
    return shoe.pop()

# ==================================================
# HI-LO COUNTING
# ==================================================
def hilo(card):
    if card in ('2','3','4','5','6'):
        return 1
    if card in ('10','J','Q','K','A'):
        return -1
    return 0

# ==================================================
# HAND
# ==================================================
@dataclass
class Hand:
    cards: list

    def add(self, card):
        self.cards.append(card)

    def value(self):
        total = 0
        aces = 0

        for c in self.cards:
            if c in ('J','Q','K'):
                total += 10
            elif c == 'A':
                total += 11
                aces += 1
            else:
                total += int(c)

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

# ==================================================
# BLACKJACK ENVIRONMENT
# ==================================================
class BlackjackEnv:
    def __init__(self):
        self.shoe = create_shoe()
        self.running_count = 0

    def reset(self):
        if len(self.shoe) < MIN_CARDS_BEFORE_SHUFFLE:
            self.shoe = create_shoe()
            self.running_count = 0

        self.player = Hand([])
        self.dealer = Hand([])

        for _ in range(2):
            c = draw(self.shoe)
            self.player.add(c)
            self.running_count += hilo(c)

            c = draw(self.shoe)
            self.dealer.add(c)
            self.running_count += hilo(c)

        return self._get_state()

    def step(self, action):
        # 0 = stand, 1 = hit

        if action == 1:  # HIT
            c = draw(self.shoe)
            self.player.add(c)
            self.running_count += hilo(c)

            if self.player.value() > 21:
                return self._get_state(), -1, True

            return self._get_state(), 0, False

        # STAND
        while self.dealer.value() < 17:
            c = draw(self.shoe)
            self.dealer.add(c)
            self.running_count += hilo(c)

        p = self.player.value()
        d = self.dealer.value()

        if d > 21 or p > d:
            return self._get_state(), 1, True
        if p < d:
            return self._get_state(), -1, True
        return self._get_state(), 0, True

    def _get_state(self):
        if USE_CARD_COUNTING:
            decks_remaining = max(1, len(self.shoe) / 52)
            true_count = self.running_count / decks_remaining
        else:
            true_count = 0

        return (
            self.player.value(),
            self._dealer_upcard_value(),
            self._bin_true_count(true_count)
        )

    def _dealer_upcard_value(self):
        c = self.dealer.cards[0]
        if c in ('J','Q','K'):
            return 10
        if c == 'A':
            return 11
        return int(c)

    def _bin_true_count(self, tc):
        if 5 <= tc:
            return 5
        elif 3.5 < tc < 5:
            return 3
        elif 1 < tc < 3.5:
            return 2
        elif -1 < tc < 1:
            return 0
        elif -3.5 < tc <= -1:
            return -2
        elif -5 < tc <= -3.5:
            return -5
        elif  tc < -5:
            return -5
    