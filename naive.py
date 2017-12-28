import card_tools
from player import Player

# Clubs 0-12
# Spades 13-25
# Diamonds 26-38
# Hearts 39-52

class NaivePlayer(Player):
    def _first(self):
        M = self.hand.index(1)
        return M

    def decide_pass_card(self):
        return self._first()

    def decide_play_card(self, trick):
        if not trick:
            return self._first()

        trick_suit = card_tools.ranksuit(trick[0])[1]
        available_cards = self.hand[13*trick_suit:13*(trick_suit + 1)]
        if any(available_cards):
            M = available_cards.index(1)
            index = 13*trick_suit + M
            self.hand[index] = 0
            return index

        return self._first()
    

