#!/usr/bin/python

import random
import card_tools
import pickle
from naive import NaivePlayer
from human import HumanPlayer
from deep import DeepPlayer

DEBUG = False

class Game(object):
    def __init__(self, players, seed=0):
        assert len(players) == 4
        random.seed(seed)

        # Adjustable
        self.players = players

    def reset_score(self):
        for player in self.players:
            player.reset()

    def get_score(self):
        return [player.points for player in self.players]

    def play_round(self, pass_direction):
        # pass_direction should be:
        #   1 = left
        #   2 = across
        #   3 = right
        #   0 = keep 
        cards = range(52)
        random.shuffle(cards)
        # Reset players and
        # Deal cards
        for ind,player in enumerate(self.players):
            player.round_reset()
            player.receive(cards[13*ind:13*(ind+1)])

        # Pass cards
        # (if not keep)
        if pass_direction != 0:
            passed_cards = []
            for ind,player in enumerate(self.players):
                three = [player.pass_card() for _ in range(3)]
                passed_cards.append(three)

            for ind,three in enumerate(passed_cards):
                receiver = (ind+pass_direction) % 4
                self.players[receiver].receive(three)

        # Play tricks
        for i in range(13):
            lookup = {}
            trick = []
            # If first round,
            # find the two of clubs
            if i == 0:
                for ind,player in enumerate(self.players):
                    if player.hand[0] == 1:
                        start = ind

            # Play the trick
            for ind in range(start, start+4):
                player = self.players[ind%4]
                played_card = player.play_card(trick)
                trick.append(played_card)
                lookup[played_card] = ind%4

                # Notify all players:
                for player in self.players:
                    player.info(trick, method="trick")

            #print [card_tools.to_symbol(card) for card in trick]
            winning_card = card_tools.trick_winner(trick)
            w = lookup[winning_card]
            # Record starter for next round
            start = w
            #print "Winner:", w
            winner = self.players[w]
            winner.receive_points(trick)

        # Check for moon-shooting
        moon_shooter = None
        for player in self.players:
            if player.round_points == 26:
                moon_shooter = player
        if moon_shooter:
            for player in self.players:
                if player is not moon_shooter:
                    player.round_points = 26
                else:
                    player.round_points = 0
        for player in self.players:
            player.addup_points()

        if DEBUG:
            print self.get_score()
            print


    def play_game(self):
        # Left, right, across, keep
        round_num = 0
        #pass_dir = [1,3,2,0]
        # No passing
        pass_dir = [0,0,0,0]
        while 1:
            self.play_round(pass_dir[round_num % 4])
            score = self.get_score()
            #print "Score:", score
            if any(map(lambda x: x >= 100, score)):
                return score

if __name__ == '__main__':
    DEBUG = True
    s = 10000
    with open('best_player.dat', 'rb') as f:
        net = pickle.load(f)
    while 1:

        players = [NaivePlayer() for _ in range(3)]
        #players = [DeepPlayer(net) for _ in range(3)]
        #players.append(HumanPlayer())
        players.append(DeepPlayer(net))
        G = Game(players, s)
        score = G.play_game()
        print score
        print
        raw_input()
        s += 1

