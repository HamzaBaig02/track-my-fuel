import streamlit as st
from api.client import SupabaseEngine
from utils.cookies import get_cookie_manager
import time
from utils.logger import logger

def init_session_state():
    if "supabase" not in st.session_state:
        logger.info("Initializing session state and retrieving cookies for authentication.")

        cookie_manager = get_cookie_manager()

        try:
            access_token = cookie_manager.get("access_token")
            time.sleep(1)
            refresh_token = cookie_manager.get("refresh_token")
            time.sleep(1)

            if access_token and refresh_token:
                logger.info("Access and refresh tokens found. Attempting to set session.")

                supabase = SupabaseEngine().supabase
                response = supabase.auth.set_session(access_token, refresh_token)

                cookie_manager.set("refresh_token", response.session.refresh_token)
                time.sleep(1)
                cookie_manager.set("access_token", response.session.access_token)
                time.sleep(1)

                logger.info("Login successful, authentication cookies set.")

                st.session_state["supabase"] = supabase
            else:
                logger.warning("Token not found in cookies. Redirecting to login.")
                raise Exception("Token not found in cookies")

        except Exception as e:
            logger.error(f"Session initialization error: {e}")
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
