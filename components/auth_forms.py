import streamlit as st

def render_signup():
    st.subheader("Create a New Account")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")

    if st.button("Sign Up"):
        pass
        # if username in user_data:
        #     st.error("Username already exists. Please choose a different one.")
        # elif password != confirm_password:
        #     st.error("Passwords do not match.")
        # else:
        #     user_data[username] = password
        #     st.success("Account created successfully! Please log in.")
        #     st.session_state["authenticated"] = False

def render_login():
    st.subheader("Login to Your Account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        pass
        # if username in user_data and user_data[username] == password:
        #     st.session_state["authenticated"] = True
        #     st.success("Logged in successfully!")
        # else:
        #     st.error("Invalid username or password.")