import streamlit as st
from utils.logger import logger

def protected(redirect_page="page_functions/auth.py"):
    """
    Decorator to protect routes requiring user authentication. Redirects to
    `redirect_page` if the user is not authenticated.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not st.session_state.get("authenticated_user"):
                try:
                    response = st.session_state["supabase"].auth.get_user()
                except Exception as e:
                    logger.error(f"Auth Error: {e}")
                    st.switch_page(redirect_page)
                    return

                if response:
                    st.session_state["authenticated_user"] = response.user
                    logger.info(f"Current User: {response.user}")
                else:
                    logger.warning("User not authenticated. Redirecting.")
                    st.switch_page(redirect_page)
                    return

            return func(*args, **kwargs)

        return wrapper
    return decorator
