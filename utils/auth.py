import streamlit as st
from supabase import create_client, Client

# Initialize the Supabase client
url = "https://pzhtrihimqxysvbziuoy.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB6aHRyaWhpbXF4eXN2YnppdW95Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAxMjYyNjQsImV4cCI6MjA0NTcwMjI2NH0._5e5q04u6UKwIpC7sz49RU69J6cTgbeZrcC_geKYmBQ"
supabase: Client = create_client(url, key)



def protected(redirect_page="page_functions/auth.py"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                response = supabase.auth.get_user()
                kwargs['user'] = response.user
                if not response:
                    st.switch_page(redirect_page)
            except Exception:
                st.switch_page(redirect_page)
            return func(*args, **kwargs)
        return wrapper
    return decorator