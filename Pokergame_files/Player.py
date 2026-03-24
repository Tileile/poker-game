
class Player:

    def __init__(self, money, name="player"):
        self.cards = list()
        self.money = money
        self.name = name
        #self.game_id = g_id

    def print_hand(self):
        for card in self.cards:
            print(card.value, card.suit)

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, index):
        del self.cards[index]

    def sort_cards(self):
        for o in range(len(self.cards)):
            min_idx = o
            for i in range(o + 1, len(self.cards)):
                if self.cards[i].value < self.cards[min_idx].value:
                    min_idx = i
            if min_idx != o:
                self.cards[o], self.cards[min_idx] = self.cards[min_idx], self.cards[o]

    #def print_info(self):
        #print(self.game_id)



