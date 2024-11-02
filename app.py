import streamlit as st
from utils.api import SupabaseEngine
from utils.cookies import get_cookie_manager
import time

def init_session_state():
    if "supabase" not in st.session_state:
        cookie_manager = get_cookie_manager()
        access_token = cookie_manager.get("access_token")
        refresh_token = cookie_manager.get("refresh_token")
        time.sleep(2)
        if access_token and refresh_token:
            supabase = SupabaseEngine().supabase
            supabase.auth.set_session(access_token, refresh_token)
            st.session_state["supabase"] = supabase
        else:
            st.session_state["supabase"] = SupabaseEngine().supabase
    if "fuel_record_list" not in st.session_state:
        st.session_state["fuel_record_list"] = []
    if "calculated_record_list" not in st.session_state:
        st.session_state["calculated_record_list"] = []


st.set_page_config(page_title="Fuel Tracker", page_icon="⛽")
pg = st.navigation(
    [
        st.Page("page_functions/home.py", title="Home", icon="🏠"),
        st.Page("page_functions/auth.py", title="Login/Signup", icon="🔑"),
        st.Page("page_functions/logout.py", title="Logout", icon="🚪"),
    ]
)


init_session_state()
pg.run()
