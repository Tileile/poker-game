from Game import Game
from Bot import Bot

import json

from flask import Flask, Response
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

game = Game(1)
bot = Bot()
game.add_player("pena", 400)
game.add_player("bot", 400)
game.add_player("bot2", 400)
game.add_player("bot3", 400)


#game.players[0].cards = list([game.deck.deck[10],game.deck.deck[11],game.deck.deck[52],game.deck.deck[52],game.deck.deck[52]])
#game.players[1].cards = list([game.deck.deck[10],game.deck.deck[23],game.deck.deck[52],game.deck.deck[52],game.deck.deck[52]])
#game.players[2].cards = list([game.deck.deck[10],game.deck.deck[23],game.deck.deck[52],game.deck.deck[52],game.deck.deck[52]])


@app.route('/start_game/<jokers>')
def start_game(jokers):
    if game.game_state == 'switch' or game.game_state == 'created':
        jokers_int = int(jokers)
        game.start_new_game(jokers_int)
        info = get_card_names(0)
    else:
        return Response(response=json.dumps({'error': 'switch not allowed'}), status=500, mimetype="application/json")

    json_info = json.dumps(info)

    return Response(response=json_info, status=200, mimetype="application/json")


def get_card_names(g_id):
    cards = game.get_cards(g_id)
    info = {
        'cards': {'card0': f'PNG-cards-1.3/{cards[0].value}_of_{cards[0].suit}.png',
                  'card1': f'PNG-cards-1.3/{cards[1].value}_of_{cards[1].suit}.png',
                  'card2': f'PNG-cards-1.3/{cards[2].value}_of_{cards[2].suit}.png',
                  'card3': f'PNG-cards-1.3/{cards[3].value}_of_{cards[3].suit}.png',
                  'card4': f'PNG-cards-1.3/{cards[4].value}_of_{cards[4].suit}.png',
                  }
    }
    return info


def get_cards_info(g_id):
    cards = game.get_cards(g_id)
    rv = [{'rank': cards[0].value, 'suit': cards[0].suit},
          {'rank': cards[1].value, 'suit': cards[1].suit},
          {'rank': cards[2].value, 'suit': cards[2].suit},
          {'rank': cards[3].value, 'suit': cards[3].suit},
          {'rank': cards[4].value, 'suit': cards[4].suit}
          ]
    return rv


def ask_switch():
    print(' 0=fold, 1=keep, input example: 0,0,0,1,0 (each bit represents card in order)')
    binary_input = input('Input which cards to fold: ')
    switch = [int(bit) for bit in binary_input]
    return switch


@app.route('/switch/<binary_values>')
def switch(binary_values):
    if game.game_state == 'start':

        switch = [int(bit) for bit in binary_values]
        game.switch_cards(0, switch)
        #game.switch_cards(1, bot.get_best_hand(game.get_cards(1)))
        #game.switch_cards(2, bot.get_best_hand(game.get_cards(2)))
        #game.switch_cards(3, bot.get_best_hand(game.get_cards(3)))

        player_info = get_card_names(0)
        bot_info = get_card_names(1)
        bot2_info = get_card_names(2)
        bot3_info = get_card_names(3)

        # for making separate function for evaluation use these two variables
        winner_idx = game.get_winner()
        hand_name = game.get_hand_name(winner_idx[0])

        info = {'p_cards': player_info,
                'bot_cards': bot_info,
                'bot2_cards': bot2_info,
                'bot3_cards': bot3_info,
                'winner_index': winner_idx,
                'hand_name': hand_name,
                'cards': [get_cards_info(0), get_cards_info(1)]
                }

    # Validate the info JSON before responding
    else:
        return Response(response=json.dumps({'error': 'Information not found'}), status=500,
                        mimetype="application/json")

    json_info = json.dumps(info)

    return Response(response=json_info, status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run(use_reloader=True, host="localhost", port=3000)

'''
#debugging
win_t = [
    {'count': 0, 'name': 'high_card'},
    {'count': 0, 'name': 'pair'},
    {'count': 0, 'name': 'two_pair'},
    {'count': 0, 'name': 'three_oak'},
    {'count': 0, 'name': 'straight'},
    {'count': 0, 'name': 'flush'},
    {'count': 0, 'name': 'full_house'},
    {'count': 0, 'name': 'four_oak'},
    {'count': 0, 'name': 'five_oak'},
    {'count': 0, 'name': 'str_flush'},
    {'count': 0, 'name': 'total'},
]
'''

'''
g_id = 0
g_id2 = 1
#already created at the beginning
#bot = Bot
#game = Game(1)
#game.add_player("pena", 400)
#game.add_player("bot", 400)
game.start_new_game(1)
print('P1')
game.players[0].print_hand()
print('P2')
game.players[1].print_hand()
print('P3')
game.players[2].print_hand()

#game.switch_cards(0, ask_switch())
#game.switch_cards(1, bot.get_best_hand(game.get_cards(1)))
#game.switch_cards(2, bot.get_best_hand(game.get_cards(2)))
game.players[0].cards = list([game.deck.deck[0],game.deck.deck[1],game.deck.deck[2],game.deck.deck[3],game.deck.deck[18]])
game.players[1].cards = list([game.deck.deck[1],game.deck.deck[2],game.deck.deck[3],game.deck.deck[4],game.deck.deck[19]])
game.players[2].cards = list([game.deck.deck[2],game.deck.deck[3],game.deck.deck[4],game.deck.deck[5],game.deck.deck[20]])

print('P1')
game.players[0].print_hand()

print('P2')
game.players[1].print_hand()
print('P3')
game.players[2].print_hand()
ranks = game.evaluator.get_pair_ranks(game.get_cards(0))
print(ranks)
winners = game.get_winner()
if len(winners) > 1:
    line = 'Game is tie, '
    for winner in winners:
        line += f'P{winner+1} '
    line += ' win'
    print(line)
else:
    print('winner ' + str(game.get_winner()[0]+1))
print(game.get_hand_name(game.get_winner()[0]))
'''

'''

# game.deal_cards(g_id, list())
# game.deal_cards(g_id, (0,))
# print(game.deck[46].suit)
# game.players[g_id].cards = list([game.deck[1],game.deck[2],game.deck[3],game.deck[4],game.deck[8]])
# game.players[g_id].print_hand()

# game.players[g_id].print_hand()
win1 = 0
win2 = 0
tie = 0
bot = Bot
# print(game.check_hand(g_id))
for c in range(10000):
    game.start_new_game(1)

    game.deal_cards(g_id)
    hand1 = game.get_cards(g_id)
    best_bits1 = bot.get_best_hand(hand1)
    game.switch_cards(g_id, best_bits1)

    game.deal_cards(g_id2)
    hand2 = game.get_cards(g_id2)
    best_bits2 = bot.get_best_hand(hand2)
    game.switch_cards(g_id2, best_bits2)

    better = game.evaluator.check_better(hand1, hand2)
    if better == 'h1_win':
        win_t[game.get_evaluation(g_id)['value']]['count'] += 1
        win1 += 1
    elif better == 'h2_win':
        win_t[game.get_evaluation(g_id2)['value']]['count'] += 1
        win2 += 1
    else:
        tie += 1
    for idx in range(0, 5):
        print(f'{game.players[g_id].cards[idx].value:2} {game.players[g_id].cards[idx].suit:8.8s}', ' | ',
              game.players[g_id2].cards[idx].value, game.players[g_id2].cards[idx].suit)
    print('P1', game.get_evaluation(g_id), 'P2', game.get_evaluation(g_id2))
    print(game.evaluator.check_better(hand1, hand2))

print(win_t)
print('P1 wins: ', win1, 'P2 wins:', win2, 'ties:', tie)


# debugging -->

game = Game(1)

#game.deal_cards(g_id, list([0, 1, 2, 3, 4]))
game.players[g_id].cards = list([game.deck.deck[10],game.deck.deck[10],game.deck.deck[10],game.deck.deck[11],game.deck.deck[11]])
game.players[g_id].print_hand()
print(game.get_best_hand(g_id))

#game.deal_cards(g_id2, list([0, 1, 2, 3, 4]))
game.players[g_id2].cards = list([game.deck.deck[10],game.deck.deck[10],game.deck.deck[11],game.deck.deck[11],game.deck.deck[11]])
game.players[g_id2].print_hand()
print(game.get_best_hand(g_id2))

print(game.evaluator.check_better(game.get_cards(g_id), game.get_cards(g_id2)))
#print(check_potential_straight_flush(list([game.deck[0],game.deck[1],game.deck[2],game.deck[25],game.deck[52]])))

'''
