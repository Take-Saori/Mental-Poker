import socket
import pickle
import streamlit as st
import itertools
import os


def xor_encrypt_decrypt(message, key):
    encrypted_message = bytes([message_byte ^ key_byte for message_byte, key_byte in zip(message, itertools.cycle(key.encode()))])
    return encrypted_message

def generate_deck():
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
    return deck

def get_image_path(hand_list, image_dir):
    image_paths = []
    for card in hand_list:
        for image in os.scandir(image_dir):
            if card['suit'] in image.name and card['rank'] in image.name:
                image_paths.append(image.path)
    return image_paths

if __name__ == "__main__":
    image_dir = 'poker_card_images'
    port = 52625
    st.title("Bob's Poker Game")

    if 'alice_in_game' not in st.session_state:
        st.session_state.alice_in_game = False

    if 'game_ended' not in st.session_state:
        st.session_state.game_ended = False

    if 'sent_deck' not in st.session_state:
        st.session_state.sent_deck = False


    try: 
        if not st.session_state.alice_in_game:
            waiting_message = st.info("Bob is waiting for Alice to connect...")
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(('localhost', port))
            print(server_socket.getsockname())
            server_socket.listen()
            st.session_state.ip_address, st.session_state.port = server_socket.accept()
            # conn, addr = server_socket.accept()
            # st.write(f"Alice connected from {st.session_state.port}")
            waiting_message.empty()
            st.session_state.alice_in_game = True
        
        if st.session_state.alice_in_game and 'ip_address' in st.session_state:
            if not st.session_state.sent_deck:
                deck = generate_deck()
                serialized_deck = pickle.dumps(deck)
                st.session_state.ip_address.send(serialized_deck)
                st.session_state.sent_deck = True

            wait_picked_cards_message = st.info("Sent encrypted deck to Alice. Waiting for Alice to pick her and Bob's cards...")
            picked_cards = pickle.loads(st.session_state.ip_address.recv(40000))
            wait_picked_cards_message.empty()

            alice_picked_cards = picked_cards[0]
            bob_picked_cards = picked_cards[1]

            st.session_state.ip_address.send(pickle.dumps(alice_picked_cards))
            # st.write("Sent Alice's cards!")
            st.session_state.game_ended = True


    finally:
        server_socket.close()

    if st.session_state.game_ended:
        st.write("Bob's Hand: ")
        bob_card_images = get_image_path(bob_picked_cards, image_dir)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(bob_card_images[0])
        with col2:
            st.image(bob_card_images[1])
        with col3:
            st.image(bob_card_images[2])
        with col4:
            st.image(bob_card_images[3])
        with col5:
            st.image(bob_card_images[4])

        st.write("Alice's Picked Cards: ")
        alice_card_images = get_image_path(alice_picked_cards, image_dir)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(alice_card_images[0])
        with col2:
            st.image(alice_card_images[1])
        with col3:
            st.image(alice_card_images[2])
        with col4:
            st.image(alice_card_images[3])
        with col5:
            st.image(alice_card_images[4])
