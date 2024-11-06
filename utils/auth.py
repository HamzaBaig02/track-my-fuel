import streamlit as st
from utils.logger import logger

#decorator
def protected(redirect_page="page_functions/auth.py"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:

                if st.session_state.get('authenticated_user',None):
                    return func(*args, **kwargs)
                response = st.session_state['supabase'].auth.get_user()
                kwargs['user'] = response.user
                st.session_state['authenticated_user'] = response.user
                logger.info(f"Current User: {response.user}.")
                if not response:
                    st.switch_page(redirect_page)
            except Exception:
                st.switch_page(redirect_page)
            return func(*args, **kwargs)
        return wrapper
    return decorator