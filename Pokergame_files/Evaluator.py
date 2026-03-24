
class Evaluator:
    win_table = {
        'high_card': {'value': 0, 'name': 'High Card'},
        'pair': {'value': 1, 'name': 'Pair'},
        'two_pair': {'value': 2, 'name': 'Two Pair'},
        'three_oak': {'value': 3, 'name': 'Three of a Kind'},
        'straight': {'value': 4, 'name': 'Straight'},
        'flush': {'value': 5, 'name': 'Flush'},
        'full_h': {'value': 6, 'name': 'Full House'},
        'four_oak': {'value': 7, 'name': 'Four of a Kind'},
        'five_oak': {'value': 8, 'name': 'Five of a Kind'},
        'str_flush': {'value': 9, 'name': 'Straight Flush'}
    }

    # checks which hand is better, returns string indicating result
    @staticmethod
    def check_better(hand1, hand2):
        h1_best_hand = Evaluator.evaluate_hand(hand1)
        h2_best_hand = Evaluator.evaluate_hand(hand2)
        if h1_best_hand['value'] > h2_best_hand['value']:
            result = 'h1_win'
        elif h1_best_hand['value'] < h2_best_hand['value']:
            print('best hand ', h1_best_hand['name'])
            result = 'h2_win'
        else:
            # card ranks are compared according to the best hand
            if h1_best_hand['name'] == 'Two Pair':
                result = Evaluator.check_better_2_pairs(hand1, hand2)
            elif h1_best_hand['name'] == 'Full House':
                result = Evaluator.check_better_full_house(hand1, hand2)
            elif h1_best_hand['name'] == 'Flush':
                result = Evaluator.check_better_flush(hand1, hand2)
            elif h1_best_hand['name'] == 'Straight':
                result = Evaluator.check_better_straight(hand1, hand2)
            else:
                result = Evaluator.check_better_pair(hand1, hand2)  # handles all pairs and high_card
        return result

    # checks which hand has higher ranks,
    # assumes both hands have two pairs, no joker in hand
    @staticmethod
    def check_better_2_pairs(hand1, hand2):
        for i in range(1, 4):
            idx = i % 3
            if hand1[idx].value > hand2[idx].value:
                return 'h1_win'
            elif hand1[idx].value < hand2[idx].value:
                return 'h2_win'
        if hand1[4].value > hand2[4].value:
            return 'h1_win'
        elif hand1[4].value < hand2[4].value:
            return 'h2_win'
        else:
            return "tie"

    # checks which hand has higher ranks,
    # assumes both hands have full house, no joker in hand
    @staticmethod
    def check_better_full_house(hand1, hand2):
        for i in range(1, 4):
            idx = (i % 3) + 1
            if hand1[idx].value > hand2[idx].value:
                return 'h1_win'
            elif hand1[idx].value < hand2[idx].value:
                return 'h2_win'
        return 'tie'

    # checks which hand has higher ranks,
    # assumes both hands have equal pair,n-of-kind or high card
    @staticmethod
    def check_better_pair(hand1, hand2):
        h1_ranks = Evaluator.get_pair_ranks(hand1)
        h2_ranks = Evaluator.get_pair_ranks(hand2)
        if len(h1_ranks) <= len(h2_ranks):
            amount_of_ranks = len(h1_ranks)
        else:
            amount_of_ranks = len(h2_ranks)

        for idx in range(amount_of_ranks - 1, 0, -1):
            if h1_ranks[idx] == h2_ranks[idx]:
                continue
            elif h1_ranks[idx] > h2_ranks[idx]:
                return 'h1_win'
            elif h1_ranks[idx] < h2_ranks[idx]:
                return 'h2_win'
        return 'tie'

    # checks which hand has higher ranks,
    # assumes both hands have flush
    @staticmethod
    def check_better_flush(hand1, hand2):
        h1_ranks = Evaluator.get_flush_ranks(hand1)
        h2_ranks = Evaluator.get_flush_ranks(hand2)
        for idx in range(len(h1_ranks) - 1, -1, -1):
            if h1_ranks[idx] > h2_ranks[idx]:
                return 'h1_win'
            elif h1_ranks[idx] < h2_ranks[idx]:
                return 'h2_win'
        return 'tie'

    # checks which hand has better straight,
    # assumes both hands form straight
    @staticmethod
    def check_better_straight(hand1, hand2):
        h1_rank = Evaluator.get_straight_hi(hand1)
        h2_rank = Evaluator.get_straight_hi(hand2)
        if h1_rank > h2_rank:
            result = 'h1_win'
        elif h1_rank < h2_rank:
            result = 'h2_win'
        else:
            result = 'tie'
        return result

    # checks highest rank of straight or straight-flush,
    # assumes hand forms straight
    @staticmethod
    def get_straight_hi(cards):
        rank = 0
        if cards[0].value >= 10:
            rank = 14
        for card in cards[::-1]:
            if card.suit != 'joker':
                if card.value == 14 and cards[0].value <= 5:
                    rank = 5
                elif cards[0].value < 10:
                    rank = cards[0].value + 4
                break
        return rank

    # checks highest card of straight or straight-flush, not in use
    @staticmethod
    def get_flush_hi(cards):
        if cards[4].suit == 'joker':
            rank = 14
        else:
            rank = cards[4].value
        return rank

    # return sorted ranks as list, assumes hand has pair, n-of-kind or high card,
    # list has a single value of each rank
    @staticmethod
    def get_pair_ranks(cards):
        ranks = []
        pair_rank = 0
        for idx, c in enumerate(cards[0:4], 1):
            if c.suit != 'joker':
                if ((c.value == cards[idx].value or cards[idx].suit == 'joker')
                        and pair_rank == 0):
                    pair_rank = c.value
                elif pair_rank != c.value != cards[idx].value:
                    ranks.append(c.value)
        if cards[4].suit != 'joker' and cards[4].value not in ranks:
            ranks.append(cards[4].value)
        if pair_rank != 0 and pair_rank not in ranks:
            ranks.append(pair_rank)
        return ranks

    # return ranks of flush hand as list sorted from highest to lowest
    @staticmethod
    def get_flush_ranks(cards):
        hand = cards.copy()
        ranks = []
        index = 0
        while len(ranks) < 5:
            if hand[index].suit != 'joker':
                ranks.append(hand[index].value)
                index += 1
            else:  # if hand has at least one joker, assign jokers rank as highest available rank
                for i in range(0, 5):
                    if (14 - i) not in ranks:
                        ranks.append(14 - i)
                        index += 1
                        break
                    else:
                        continue
        ranks.sort(reverse=True)
        print(ranks)
        return ranks

    # Checks and returns the best hand cards form as win_tab result
    @staticmethod
    def evaluate_hand(cards):
        best_pair = Evaluator.check_pairs(cards)
        is_flush = Evaluator.check_flush(cards)
        is_straight = Evaluator.check_straight(cards)
        # skips if no pairs or joker in hand => might be flush, straight or both
        if is_straight and is_flush:
            best_hand = Evaluator.win_table['str_flush'].copy()
        elif is_flush and best_pair['value'] < Evaluator.win_table['flush']['value']:
            best_hand = Evaluator.win_table['flush'].copy()
        elif is_straight and best_pair['value'] < Evaluator.win_table['straight']['value']:
            best_hand = Evaluator.win_table['straight'].copy()
        else:
            best_hand = best_pair
        return best_hand

    # Check if hand has pair, n-of-kind, two pair, full house or only high card,
    # returns the best hand cards form as win_tab result
    @staticmethod
    def check_pairs(cards):
        win_tab = Evaluator.win_table.copy()
        best_hand = win_tab['high_card']
        prev_pair = cards[4].value
        for idx, c in enumerate(cards[0:4], 1):
            if c.value == cards[idx].value or cards[idx].suit == 'joker':
                if best_hand['name'] == 'High Card':
                    best_hand = win_tab['pair'].copy()
                    prev_pair = c.value
                elif prev_pair != c.value and cards[idx].suit != 'joker':
                    if best_hand['name'] == 'Pair':
                        best_hand = Evaluator.win_table['two_pair'].copy()
                        prev_pair = c.value
                    elif best_hand['name'] == 'Three of a Kind':
                        best_hand = Evaluator.win_table['full_h'].copy()
                elif best_hand['name'] == 'Pair':
                    best_hand = Evaluator.win_table['three_oak'].copy()
                elif best_hand['name'] == 'Two Pair':
                    best_hand = Evaluator.win_table['full_h'].copy()
                elif best_hand['name'] == 'Three of a Kind':
                    best_hand = Evaluator.win_table['four_oak'].copy()
                elif best_hand['name'] == 'Four of a Kind':
                    best_hand = Evaluator.win_table['five_oak'].copy()
        return best_hand

    # return true if cards have flush
    @staticmethod
    def check_flush(cards):
        count = 0
        for card in cards[1:5]:
            if card.suit == cards[0].suit or card.suit == 'joker':
                count += 1
        if count == 4:
            return True
        return False

    # returns True if cards form a straight
    @staticmethod
    def check_straight(cards):
        # checking for pairs, hand cant be straight if it has pairs
        for idx, c in enumerate(cards[0:4], 1):
            if c.value == cards[idx].value:
                if cards[idx].suit != 'joker':
                    return False

        for idx, c in enumerate(cards[::-1], 1):
            if c.suit != 'joker' and cards[4 - idx].suit != 'joker':
                # if highest rank - lowest rank <= 4, hand must be straight
                if c.value - cards[0].value <= 4:
                    return True
                # if card is Ace, check if second-highest rank is 5 or less
                elif c.value == 14 and cards[4 - idx].value - 1 <= 4:
                    return True
                else:
                    return False
        return True
