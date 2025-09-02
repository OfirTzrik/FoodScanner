import streamlit as st
import os
from PIL import Image

def apply_styles():
    st.set_page_config(
        page_title = "Frige App",
        page_icon = Image.open("assets/logo.png"), 
        layout = "wide",
        initial_sidebar_state = "collapsed"
    )

    hide_streamlit_style_option = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        div.stButton > button {
            height: 50px;
            width: 150px;
            font-size: 20px;
        }
        div.stTextInput > input {
            height: 50px;
            font-size: 18px;
        }
        </style>
    """
    st.markdown(hide_streamlit_style_option, unsafe_allow_html=True)