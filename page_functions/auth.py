import streamlit as st
from components.auth_forms import render_login_form, render_signup_form
from utils.auth import supabase


def render_login_signup():

    try:
        response =  supabase.auth.get_user()
        if response:
            st.switch_page("page_functions/home.py")
    except Exception as e:
        st.error(str(e))


    auth_choice = st.selectbox("Select an option", ["Login", "Sign Up"])
    if auth_choice == "Sign Up":
        registration_data = render_signup_form()
        if registration_data:
            try:
                response = supabase.auth.sign_up(
                    {"email": registration_data["email"], "password": registration_data["password"]}
                )
            except Exception as e:
                st.error(str(e))

    elif auth_choice == "Login":
        login_data = render_login_form()
        if login_data:
            try:
                response = supabase.auth.sign_in_with_password(
                    {"email": login_data["email"], "password": login_data["password"]}
                )
                if not response.user:
                    st.error('Unable to login')
                st.switch_page("page_functions/home.py")
            except Exception as e:
                st.error(str(e))


render_login_signup()
