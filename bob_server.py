import socket
import pickle
import streamlit as st
import utils
import deck_utils
from protocol import Protocol
import random

if __name__ == "__main__":
    image_dir = 'poker_card_images'
    port = 52625
    bob_protocol = Protocol()
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
                deck = [i+2 for i in range(52)]
                random.shuffle(deck)
                # Encrypt deck
                for i in range(len(deck)):
                    deck[i] = bob_protocol.get_encrypted_card(deck[i])

                serialized_deck = pickle.dumps(deck)
                st.session_state.ip_address.send(serialized_deck)
                st.session_state.sent_deck = True

            wait_picked_cards_message = st.info("Sent encrypted deck to Alice. Waiting for Alice to pick her and Bob's cards...")
            picked_cards = pickle.loads(st.session_state.ip_address.recv(40000))
            wait_picked_cards_message.empty()

            alice_picked_cards = picked_cards[0]
            bob_hand = picked_cards[1]

            # Decrypt bob's hand using bob's key
            for i in range(len(bob_hand)):
                bob_hand[i] = bob_protocol.get_decrypted_card(bob_hand[i])
            
            # Decrypt alice's hand using bob's key, so only alice's "lock" on her hand
            for i in range(len(alice_picked_cards)):
                alice_picked_cards[i] = bob_protocol.get_decrypted_card(alice_picked_cards[i])

            # Send both cards so that they know each other's cards after game ends
            st.session_state.ip_address.send(pickle.dumps([alice_picked_cards, bob_hand]))
            # st.write("Sent Alice's cards!")

            # Receive decrypted alice's hand
            alice_hand = pickle.loads(st.session_state.ip_address.recv(40000))
            st.session_state.game_ended = True


    finally:
        server_socket.close()

    if st.session_state.game_ended:
        # Convert the card_id to card suit and ranks
        for i in range(len(alice_hand)):
            alice_hand[i] = deck_utils.convert_id_to_card(alice_hand[i])
        for i in range(len(bob_hand)):
            bob_hand[i] = deck_utils.convert_id_to_card(bob_hand[i])

        winner = utils.get_winner(alice_hand, bob_hand)
        if winner == 'Draw':
            st.header('Draw!')
        elif winner == 'Bob':
            st.header('You Won!')
        else: # Alice winner
            st.header('You Lost...')

        st.subheader(f"Bob's Hand: {utils.hand_name(bob_hand)}")
        bob_card_images = utils.get_image_path(bob_hand, image_dir)
        utils.show_5_images(bob_card_images)

        st.subheader(f"Alice's Hand: {utils.hand_name(alice_hand)}")
        alice_card_images = utils.get_image_path(alice_hand, image_dir)
        utils.show_5_images(alice_card_images)

        
