from Pokergame_files.Card import Card
import random


class Deck:

    def __init__(self, joker):
        self.joker = joker
        self.deck = Deck.create_deck(joker)

    def draw_card(self):
        return self.deck.pop()

    @staticmethod
    def create_deck(jokers):
        suits = list(['diamonds', 'hearts', 'clubs', 'spades', 'joker'])
        deck = list()
        for s in range(0, 4):
            for value in range(2, 15):
                deck.append(Card(suits[s], value))
        for _ in range(jokers):
            deck.append(Card(suits[4], 69))
        random.shuffle(deck)
        return deck
