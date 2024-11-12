import streamlit as st
from supabase import create_client, Client

import streamlit as st
from supabase import create_client, Client

class SupabaseEngine:
    _instance = None
    supabase: Client

    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseEngine, cls).__new__(cls)
            cls._instance.supabase = create_client(cls.url, cls.key) 
        return cls._instance
