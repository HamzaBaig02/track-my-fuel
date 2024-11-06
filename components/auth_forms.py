import streamlit as st
from utils.validation import is_valid_email

def render_signup_form():
    registration_data = {}
    with st.form(key="signup_form"):
        st.subheader("Create a New Account")
        registration_data['email'] = st.text_input("Email", key="signup_email").strip()
        registration_data['password'] = st.text_input("Password", type="password", key="signup_password")
        registration_data['confirm_password'] = st.text_input("Confirm Password", type="password", key="signup_confirm_password")

        submit_button = st.form_submit_button("Sign Up")
        if submit_button:
            registration_data['email'] = registration_data['email'].strip()
            if not is_valid_email(registration_data['email']):
                st.error("Email address is not valid")
            elif registration_data['password'] != registration_data['confirm_password']:
                st.error("Passwords do not match.")
            else:
                return registration_data

def render_login_form():
    login_data = {}
    with st.form(key="login_form"):
        st.subheader("Login to Your Account")
        login_data['email'] = st.text_input("Email", key="login_email").strip()
        login_data['password'] = st.text_input("Password", type="password", key="login_password")

        submit_button = st.form_submit_button("Login")
        if submit_button:
            login_data['email'] = login_data['email'].strip()
            if not is_valid_email(login_data['email']):
                st.error("Email address is not valid")
            else:
                return login_data
