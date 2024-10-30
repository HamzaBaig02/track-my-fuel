import streamlit as st
from components.auth_forms import render_login,render_signup

def render_login_signup():
    auth_choice = st.selectbox("Select an option", ["Login", "Sign Up"])
    if auth_choice == "Sign Up":
        render_signup()
    elif auth_choice == "Login":
        render_login()


render_login_signup()