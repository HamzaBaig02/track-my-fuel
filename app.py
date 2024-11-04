import streamlit as st
from api.client import SupabaseEngine
from utils.cookies import get_cookie_manager
import time
from utils.logger import logger

def init_session_state():
    if "supabase" not in st.session_state:
        cookie_manager = get_cookie_manager()
        access_token = cookie_manager.get("access_token")
        time.sleep(1)
        refresh_token = cookie_manager.get("refresh_token")
        time.sleep(1)
        try:
            if access_token and refresh_token:
                supabase = SupabaseEngine().supabase
                response = supabase.auth.set_session(access_token, refresh_token)
                cookie_manager.set("refresh_token",response.session.refresh_token)
                cookie_manager.set("access_token",response.session.access_token)
                time.sleep(2)
                logger.info("Login in sucessful, setting auth cookies...")
                st.session_state["supabase"] = supabase
            else:
                raise Exception("Token not found in cookies")
        except Exception as e:
            logger.error(str(e))
            st.session_state["supabase"] = SupabaseEngine().supabase
    return


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
