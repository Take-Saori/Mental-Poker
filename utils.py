import streamlit as st
import os

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

