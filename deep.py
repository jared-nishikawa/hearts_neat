import card_tools
from player import Player

class DeepPlayer(Player):
    def __init__(self, net):
        self.net = net
        Player.__init__(self)

    def pick_max(self, vector):
        M = max(vector)
        return vector.index(M)

    def decide_play_card(self, trick):
        if not trick and not sum(self.played):
            return 0

        trick_vector = [0]*52
        for card in trick:
            trick_vector[card] = 1
        input_vector = self.hand + self.played + trick_vector
        output_vector = self.net.activate(input_vector)

        # Filters
        # Must play a card in my own hand
        for i in range(52):
            if self.hand[i] == 0:
                output_vector[i] = -1

        #   Two of clubs to start <- Done
        
        #   Can't lead with hearts until hearts is broken
        #       (unless I only have hearts left)
        if not trick and not self.hearts_broken() and \
                any(self.hand[:39]):
            for i in range(39,52):
                output_vector[i] = -1

        elif trick:
        #   Must follow suit
            trick_suit = card_tools.ranksuit(trick[0])[1]
            available_cards = self.hand[13*trick_suit:13*(trick_suit + 1)]
            if any(available_cards):
                for i in range(52):
                    if card_tools.ranksuit(i)[1] != trick_suit:
                        output_vector[i] = -1

        #   Can't play points on the first hand
            else:
                if len(self.played) < 4:
                    output_vector[23] == -1
                    for i in range(39,52):
                        output_vector[i] = -1

        #print output_vector
        return self.pick_max(output_vector)
