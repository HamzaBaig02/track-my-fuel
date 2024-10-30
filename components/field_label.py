import streamlit as st

def render_field_label( text:str, font_size:int = 24, font_color:str = 'grey'):
    return st.markdown(
    f"<p style='font-size:{font_size}px; color:{font_color}; margin-bottom:0px;'>{text}</p>",
    unsafe_allow_html=True
)