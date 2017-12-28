import card_tools
from player import Player

class HumanPlayer(Player):
    def _show_hand(self):
        print [card_tools.to_symbol(index) \
                for index,card in enumerate(self.hand) if card]

    def _get_card(self):
        self._show_hand()
        #print [card_tools.to_symbol(card) for card in trick]
        while 1:
            card = raw_input("Play a card: ")
            try:
                num = card_tools.to_num(card)
                if not self.hand[num]:
                    print("Card not in hand")
                else:
                    break
            except ValueError:
                print("Not a valid card")
            except AssertionError:
                print("Not a valid card")

        return num

    def decide_pass_card(self):
        return self._get_card()

    def decide_play_card(self, trick):
    
        if not trick:
            # Play two of clubs to start
            if not sum(self.played):
                if not self.hand[0]:
                    raise Exception("This player should have the two of clubs")
                # 0 = two of clubs
                return 0

            # Can't lead with hearts until hearts is broken
            # unless I have only hearts left
            while 1:
                num = self._get_card()
                if not self.hearts_broken() and num >= 39 and \
                        any(self.hand[:39]):
                    print("Can't lead with hearts")
                else:
                    return num
        
        trick_suit = card_tools.ranksuit(trick[0])[1]
        available_cards = self.hand[13*trick_suit:13*(trick_suit + 1)]
        #print available_cards
        
        # If you have the suit, must follow suit
        if any(available_cards):
            while 1:
                num = self._get_card()
                if card_tools.ranksuit(num)[1] != trick_suit:
                    print("Not a valid card to play")
                else:
                    return num

        # Can't play points on first turn
        elif len(self.played) < 4:
            while 1:
                num = self._get_card()
                if num >= 39 or num == 23:
                    print("Can't play points on the first hand")
                else:
                    break

        return self._get_card()

    def info(self, data, method=None):
        if method == "trick":
            print [card_tools.to_symbol(card) for card in data]
        Player.info(self, data, method)
