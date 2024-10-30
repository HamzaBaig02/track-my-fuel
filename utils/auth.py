import streamlit as st

def protected(redirect_page="page_functions/auth.py"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not st.session_state.get("authenticated", False):
                st.warning("You need to be logged in to access this page.")
                st.switch_page(redirect_page)
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator