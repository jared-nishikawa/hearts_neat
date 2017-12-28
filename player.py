class Player(object):
    def __init__(self):
        self.hand = [0]*52
        self.played = [0]*52
        self.points = 0
        self.round_points = 0

    def round_reset(self):
        self.hand = [0]*52
        self.played = [0]*52
        self.round_points = 0

    def reset(self):
        self.round_reset()
        self.points = 0

    def hearts_broken(self):
        if any(self.played[39:]):
            return True
        return False

    def receive(self, cards):
        for card in cards:
            self.hand[card] = 1

    def pass_card(self):
        card = self.decide_pass_card()
        self.hand[card] = 0
        return card

    def play_card(self, trick):
        card = self.decide_play_card(trick)
        self.hand[card] = 0
        return card

    def decide_pass_card(self):
        raise NotImplementedError

    def decide_play_card(self, trick):
        raise NotImplementedError
    
    def receive_points(self, trick):
        for card in trick:
            # Hearts
            if card >= 39:
                self.round_points += 1
            # Queen of spades
            if card == 23:
                self.round_points += 13

    def addup_points(self):
        self.points += self.round_points
        self.round_points = 0

    def info(self, data, method=None):
        if method=="trick":
            for card in data:
                self.played[card] = 1



        

