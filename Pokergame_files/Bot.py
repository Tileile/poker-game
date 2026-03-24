
class Bot:

    # Checks most potential cards to fold/keep for straight flush.
    # Returns bits representing cards to fold/keep(0/1)
    @staticmethod
    def get_straight_flush_bits(hand):
        straight_bits = Bot.get_straight_bits(hand)
        flush_bits = Bot.get_flush_bits(hand)
        str_flush_bits = [bit1 & bit2 for bit1, bit2 in zip(straight_bits, flush_bits)]
        return str_flush_bits

    # Checks most potential cards to fold/keep for straight,
    # Returns bits representing cards to fold/keep(0/1)
    @staticmethod
    def get_straight_bits(hand):
        best_bits = [0, 0, 0, 0, 0]  # bits representing cards to fold/keep(0/1)
        for i, card in enumerate(hand[0:4], 1):  # 'card' represents reference card
            bits = [0, 0, 0, 0, 0]
            bits[i-1] = 1
            for n in range(i, 5):  # n refers to current comparison card(cards remaining after i)
                if ((hand[n].value - card.value <= 4 or (hand[n].value == 14 and hand[i-1].value <= 5))
                        and hand[n].value != card.value and hand[n].value != hand[n-1].value
                        or hand[n].suit == 'joker'):
                    bits[n] = 1
            # if bits represent better hand than current best
            if best_bits.count(1) <= bits.count(1):
                best_bits = bits
        return best_bits

    # Checks if any of two consecutive cards match, matching cards are marked for keeping.
    # (Handles n-of-kinds, pair, two pair and full house)
    # Returns bits representing cards to fold/keep(0/1)
    @staticmethod
    def get_pair_bits(hand):
        cards = [0, 0, 0, 0, 0]  # bits representing cards to fold/keep
        for i, card in enumerate(hand[0:4], 1):
            # if two consecutive cards match, keep both
            if card.value == hand[i].value:
                cards[i-1], cards[i] = 1, 1
            elif hand[i].suit == 'joker':
                # if no pairs in hand, keep the largest card (along with joker)
                if cards.count(1) == 0:
                    cards[i-1] = 1
                # joker is never folded
                cards[i] = 1
        return cards

    # Checks most potential cards to fold/keep for flush.
    # Returns bits representing cards to fold/keep(0/1)
    @staticmethod
    def get_flush_bits(hand):
        best_bits = [0, 0, 0, 0, 0]  # bits representing cards to fold/keep(0/1)
        for i, card in enumerate(hand[0:4], 1):
            bits = [0, 0, 0, 0, 0]
            bits[i - 1] = 1
            for n in range(i, 5):
                if hand[n].suit == card.suit or hand[n].suit == 'joker':
                    bits[n] = 1
            # if bits represent better flush than current best
            if best_bits.count(1) <= bits.count(1):
                best_bits = bits
        return best_bits

    # unused function, returns indexes of cards to fold as list
    @staticmethod
    def get_cards_to_fold(cards):
        fold = []
        for i, keep in enumerate(cards, 0):
            if keep == 0:
                fold.append(i)
        return fold

    # returns most potential cards to fold/keep, represented as bits
    @staticmethod
    def get_best_hand(hand, pair=3, flush=2, straight=2, str_flush=1):
        # get potential cards to keep as bits
        straight_bits = Bot.get_straight_bits(hand)
        pair_bits = Bot.get_pair_bits(hand)
        flush_bits = Bot.get_flush_bits(hand)
        str_flush_bits = Bot.get_straight_flush_bits(hand)
        # checks which option is the best choice for strongest hand
        if str_flush_bits.count(0) == str_flush:
            best_bits = str_flush_bits
        elif flush_bits.count(0) <= flush and pair_bits.count(0) > pair or flush_bits.count(0) <= 1:
            best_bits = flush_bits
        elif straight_bits.count(0) <= straight and pair_bits.count(0) > pair or straight_bits.count(0) <= 1:
            best_bits = straight_bits
        elif pair_bits.count(0) < 5:  # chosen if hand has any pairs
            best_bits = pair_bits
        else:
            best_bits = [0, 0, 0, 0, 1]  # keeps the highest card

        return best_bits
