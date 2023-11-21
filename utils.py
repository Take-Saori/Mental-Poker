import streamlit as st
import os
from collections import Counter

def get_image_path(hand_list, image_dir):
    image_paths = []
    for card in hand_list:
        for image in os.scandir(image_dir):
            if card['suit'] in image.name and card['rank'] in image.name:
                image_paths.append(image.path)
    return image_paths


def show_5_images(image_paths_list):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(image_paths_list[0])
    with col2:
        st.image(image_paths_list[1])
    with col3:
        st.image(image_paths_list[2])
    with col4:
        st.image(image_paths_list[3])
    with col5:
        st.image(image_paths_list[4])



def get_winner(alice_hand, bob_hand):
    # Map hand name and points (for ranking purposes)
    hand_points = {
        'Royal Straight Flush' : 10,
        'Straight Flush' : 9,
        'Four of a Kind' : 8,
        'Full House' : 7,
        'Flush' : 6,
        'Straight' : 5,
        'Three of a Kind' : 4,
        'Two Pair' : 3,
        'Pair' : 2,
        'High Card' : 1
    }

    alice_hand_name = hand_name(alice_hand)
    bob_hand_name = hand_name(bob_hand)

    if hand_points[alice_hand_name] > hand_points[bob_hand_name]:
        return 'Alice'
    elif hand_points[alice_hand_name] < hand_points[bob_hand_name]:
        return 'Bob'
    else: # Equal
        return 'Draw'
    


def hand_name(hand_list):
    """
    Return name of the hand.

    Ranking of a hand:
    1. Royal Straight Flush: All same suit, ranks are: 10, Jack, Queen, King, and Ace
    2. Straight Flush: 5 consecutive cards of the same suit
    3. Four of a Kind: 4 cards of the same rank
    4. Full House: 3 matching cards of one rank and 2 matching cards of another rank
    5. Flush: any 5 cards of the same suit
    6. Straight: 5 cards of consecutive rank but from more than one suit (meaning different suit)
    7. Three of a Kind: 3 cards of the same rank
    8. Two Pair: 2 cards of one rank, plus 2 cards of another rank (different from the first pair)
    9. Pair: 2 cards of the same rank
    10. High Card: Nothing, basically not the above hands.
    """

    # Map ranks to numerical values for comparison
    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'jack': 11, 'queen': 12, 'king': 13, 'ace': 14}
    
    # Sort the hand by rank values
    sorted_hand = sorted(hand_list, key=lambda card: rank_values[card['rank']])

    # Check for poker hands
    # is_straight = all(rank_values[sorted_hand[i]['rank']] == rank_values[sorted_hand[i - 1]['rank']] + 1 for i in range(1, len(sorted_hand)))
    is_straight = all(rank_values[sorted_hand[i]['rank']]+1 == rank_values[sorted_hand[i+1]['rank']] for i in range(len(sorted_hand)-1))
    is_flush = all(card['suit'] == sorted_hand[0]['suit'] for card in sorted_hand[1:])



    if is_straight and is_flush:
        if sorted_hand[0]['rank'] == '10':
            return 'Royal Straight Flush'
        else:
            return 'Straight Flush'
        
    rank_list = [card['rank'] for card in sorted_hand]
    # Get the dictionary of counts of each unique value(rank in this case) from rank_list
    unique_value_count_dict = Counter(rank_list)
    # Get counts list of each ranks (basically, the frequency list of each rank)
    count_list = list(unique_value_count_dict.values())
    # If a certain rank appeared 4 times in the rank_list, four of a kind
    if 4 in count_list:
        return 'Four of a Kind'
    
    # If a certain rank appeared 3 times and another different rank appeared 2 times
    elif 3 in count_list and 2 in count_list:
        return 'Full House'
    
    elif is_flush:
        return 'Flush'
    
    elif is_straight:
        return 'Straight'
    
    elif 3 in count_list:
        return 'Three of a Kind'
    
    # If 2 cards of one rank, plus 2 cards of another rank appeared
    elif count_list.count(2) == 2:
        return 'Two Pair'
    
    elif 2 in count_list:
        return 'Pair'
    
    else:
        return 'High Card'