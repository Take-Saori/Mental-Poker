import logging
import socket
import pickle
import streamlit as st
import utils

@st.cache_resource
def initialize_socket(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    return client_socket

@st.cache_resource
def receive_deck(_client_socket):
        data = _client_socket.recv(1024)
        data = pickle.loads(data)
        return data

if __name__ == "__main__":
    image_dir = 'poker_card_images'
    port = 52625
    st.title("Alice's Poker Game")

    if 'picked' not in st.session_state:
        st.session_state.picked = False

    if 'game_ended' not in st.session_state:
        st.session_state.game_ended = False
    
    if 'received_deck' not in st.session_state:
        st.session_state.received_deck = False

    if 'confirm_clicked' not in st.session_state:
        st.session_state.confirm_clicked = False

    client_socket = initialize_socket(port)
    # st.write(f"Alice connected to Bob on port {port}")

    data = receive_deck(client_socket)

    try:
    
        # st.write("Alice has received the encrypted deck from Bob")

        # Pick 5 cards
        if not st.session_state.picked:

            pick_5_alice = st.subheader("Pick 5 numbers for yourself.")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                image1 = st.image("poker_card_images/card back orange.png")
                number1 = st.number_input('Number 1', label_visibility='collapsed', key='1', min_value=0, max_value=52, value=int(0), disabled=st.session_state.confirm_clicked)
            with col2:
                image2 = st.image("poker_card_images/card back orange.png")
                number2 = st.number_input('Number 2', label_visibility='collapsed', key='2', min_value=0, max_value=52, value=int(0), disabled=st.session_state.confirm_clicked)
            with col3:
                image3 = st.image("poker_card_images/card back orange.png")
                number3 = st.number_input('Number 3', label_visibility='collapsed', key='3', min_value=0, max_value=52, value=int(0), disabled=st.session_state.confirm_clicked)
            with col4:
                image4 = st.image("poker_card_images/card back orange.png")
                number4 = st.number_input('Number 4', label_visibility='collapsed', key='4', min_value=0, max_value=52, value=int(0), disabled=st.session_state.confirm_clicked)
            with col5:
                image5 = st.image("poker_card_images/card back orange.png")
                number5 = st.number_input('Number 5', label_visibility='collapsed', key='5', min_value=0, max_value=52, value=int(0), disabled=st.session_state.confirm_clicked)


            pick_5_bob = st.subheader("Pick 5 numbers for Bob.")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                image6 = st.image("poker_card_images/card back orange.png")
                number6 = st.number_input('Number 1', label_visibility='collapsed', key='6', min_value=0, max_value=52, value=int(0), disabled=st.session_state.confirm_clicked)
            with col2:
                image7 = st.image("poker_card_images/card back orange.png")
                number7 = st.number_input('Number 2', label_visibility='collapsed', key='7', min_value=0, max_value=52, value=int(0), disabled=st.session_state.confirm_clicked)
            with col3:
                image8 = st.image("poker_card_images/card back orange.png")
                number8 = st.number_input('Number 3', label_visibility='collapsed', key='8', min_value=0, max_value=52, value=int(0), disabled=st.session_state.confirm_clicked)
            with col4:
                image9 = st.image("poker_card_images/card back orange.png")
                number9 = st.number_input('Number 4', label_visibility='collapsed', key='9', min_value=0, max_value=52, value=int(0), disabled=st.session_state.confirm_clicked)
            with col5:
                image10 = st.image("poker_card_images/card back orange.png")
                number10 = st.number_input('Number 5', label_visibility='collapsed', key='10', min_value=0, max_value=52, value=int(0), disabled=st.session_state.confirm_clicked)

            confirm_numbers = st.button("Confirm numbers", disabled=st.session_state.confirm_clicked)

            if confirm_numbers:
                st.session_state.confirm_clicked = True
                alice_numbers = [number1, number2, number3, number4, number5]
                bob_numbers = [number6, number7, number8, number9, number10]
                alice_num_str = ', '.join(str(num) for num in alice_numbers)
                bob_num_str = ', '.join(str(num) for num in bob_numbers)
                st.write(f"The chosen numbers for Alice is: {alice_num_str}")
                st.write(f"The chosen numbers for Bob is: {bob_num_str}")
                st.session_state.picked = True

        if st.session_state.picked:
            alice_picked_cards = data[:5]
            bob_picked_cards = data[-6:]
            picked_cards = [alice_picked_cards, bob_picked_cards, alice_numbers, bob_numbers]

            # Send the picked cards to Bob
            client_socket.send(pickle.dumps(picked_cards))

            # st.write("Alice has sent her picked cards to Bob")

            alice_hand = pickle.loads(client_socket.recv(1024))
            # st.write("Alice has sent the encrypted selected cards to Bob")
            st.session_state.game_ended = True

        if st.session_state.game_ended:
            st.write("Alice's Hand: ")
            alice_card_images = utils.get_image_path(alice_hand, image_dir)
            utils.show_5_images(alice_card_images)
            # col1, col2, col3, col4, col5 = st.columns(5)
            # with col1:
            #     st.image(alice_card_images[0])
            # with col2:
            #     st.image(alice_card_images[1])
            # with col3:
            #     st.image(alice_card_images[2])
            # with col4:
            #     st.image(alice_card_images[3])
            # with col5:
            #     st.image(alice_card_images[4])
            st.write("Bob's Hand: ")
            bob_card_images = utils.get_image_path(bob_picked_cards, image_dir)
            utils.show_5_images(bob_card_images)
            # col1, col2, col3, col4, col5 = st.columns(5)
            # with col1:
            #     st.image(bob_card_images[0])
            # with col2:
            #     st.image(bob_card_images[1])
            # with col3:
            #     st.image(bob_card_images[2])
            # with col4:
            #     st.image(bob_card_images[3])
            # with col5:
            #     st.image(bob_card_images[4])
            

    finally:
        if st.session_state.game_ended:
            print('in finally')
            client_socket.close()
