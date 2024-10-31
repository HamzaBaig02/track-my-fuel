import streamlit as st
from supabase import create_client, Client

class SupabaseEngine:
    url = st.secrets['supabase']['url']
    key = st.secrets['supabase']['key']
    def __init__(self):
        self.supabase: Client = create_client(self.url,self.key)

if "supabase" not in st.session_state:
     st.session_state['supabase'] = SupabaseEngine().supabase

pg = st.navigation([
    st.Page("page_functions/home.py", title="Home", icon="🏠"),
    st.Page("page_functions/auth.py", title="Login/Signup", icon="🔑"),
    st.Page("page_functions/logout.py", title="Logout", icon="🚪")
])
pg.run()





