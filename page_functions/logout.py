import streamlit as st
from utils.cookies import get_cookie_manager
import time

try:
    st.session_state['supabase'].auth.sign_out()
    st.session_state.clear()
    cookie_manager = get_cookie_manager()
    cookie_manager.set('access_token',None)
    cookie_manager.set('refresh_token',None)
    time.sleep(2)
    st.subheader("You've been logged out successfully!")

    st.switch_page("page_functions/auth.py")
except Exception as e:
    st.error(str(e))
    st.switch_page("page_functions/auth.py")