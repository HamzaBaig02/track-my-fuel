import streamlit as st
from supabase import create_client, Client

import streamlit as st
from supabase import create_client, Client

class SupabaseEngine:
    def __init__(self):
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        self.supabase = create_client(url, key)

