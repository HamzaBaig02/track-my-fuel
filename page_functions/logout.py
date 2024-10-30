import streamlit as st
from utils.auth import supabase

try:
    response = supabase.auth.sign_out()

    st.subheader("You've been logged out successfully!")
except Exception as e:
    st.error(str(e))