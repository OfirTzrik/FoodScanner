import streamlit as st
import os
from PIL import Image

def apply_styles():
    st.set_page_config(
        page_title = "Frige App",
        page_icon = Image.open("assets/logo.png"), 
        layout = "wide",   
    )