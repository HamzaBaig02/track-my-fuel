import streamlit as st
from supabase import create_client, Client

class SupabaseEngine:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]

    def __init__(self):
        self.supabase: Client = create_client(self.url, self.key)