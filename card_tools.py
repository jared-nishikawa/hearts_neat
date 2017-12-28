suits = 'CSDH'
ranks = '23456789TJQKA'

def ranksuit(num):
    assert num < 52 and num >= 0
    suit = num // 13
    rank = num % 13
    return rank, suit

def to_symbol(num):
    rank, suit = ranksuit(num)
    return ranks[rank] + suits[suit]

def to_num(symbol):
    assert len(symbol) == 2
    rank,suit = symbol
    return 13*suits.index(suit) + ranks.index(rank)

def trick_winner(trick):
    best, trick_suit = ranksuit(trick[0])
    result = trick[0]
    for card in trick:
        rank,suit = ranksuit(card)
        if suit != trick_suit:
            continue
        if rank > best:
            best = rank
            result = card
    return result



