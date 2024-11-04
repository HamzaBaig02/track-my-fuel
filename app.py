import streamlit as st
from api.client import SupabaseEngine

def init_session_state():
    if "supabase" not in st.session_state:
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
