from Pokergame_files.Deck import Deck
from Pokergame_files.Player import Player
from Pokergame_files.Evaluator import Evaluator


class Game:

    def __init__(self, jokers=0):
        self.deck = Deck(jokers)
        self.evaluator = Evaluator
        self.players = list()
        self.game_state = 'created'

    # return best hand player is currently holding
    def get_evaluation(self, g_id):
        cards = self.get_cards(g_id)
        return self.evaluator.evaluate_hand(cards)

    def get_hand_name(self, g_id):
        return self.get_evaluation(g_id)['name']

    def get_winner(self):
        best_p_idx = [0]
        for idx in range(1, len(self.players)):
            better = self.evaluator.check_better(self.get_cards(best_p_idx[0]), self.get_cards(idx))
            if better == 'h1_win':
                continue
            elif better == 'h2_win':
                best_p_idx = [idx]
            else:
                best_p_idx.append(idx)  # tie
                # tie not handled properly, needs more work if bet is applied
                # (split pot between tied players)
        return best_p_idx

    def start_new_game(self, jokers):
        self.deck = Deck(jokers)
        self.game_state = 'start'
        for idx, player in enumerate(self.players, 0):
            self.deal_cards(idx)

    def deal_cards(self, g_id):
        for i in range(5):
            if len(self.players[g_id].cards) < i+1:
                self.players[g_id].cards.append(self.deck.draw_card())
            else:
                self.players[g_id].cards[i] = (self.deck.draw_card())
        self.players[g_id].sort_cards()

    # deals cards if player has empty hand or if player wants to switch cards
    def switch_cards(self, g_id, fold_bits):
        for i, bit in enumerate(fold_bits, 0):
            # replace card marked for folding with card from deck
            if bit == 0:
                self.players[g_id].cards[i] = self.deck.draw_card()
        self.players[g_id].sort_cards()
        self.game_state = 'switch'

    # returns players cards
    def get_cards(self, g_id):
        return self.players[g_id].cards.copy()

    def add_player(self, name, money=500):
        self.players.append(Player(money, name))

    def play(self, jokers):
        self.start_new_game(jokers)


