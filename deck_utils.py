import random

suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
deck_dict = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
    
def convert_card_to_id(card):
    return deck_dict.index(card)+2

def convert_id_to_card(card_id):
    return deck_dict[card_id-2]

def shuffle_deck(deck):
    return random.shuffle(deck)

