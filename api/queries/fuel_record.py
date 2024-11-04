import streamlit as st
from supabase import Client


supabase:Client = st.session_state["supabase"]

def create_fuel_record(fuel_record):
    response = (
    supabase.table("fuel_record")
    .insert(fuel_record)
    .execute()
    )
    return response.data[0]

def get_all_fuel_records():
    response = supabase.table("fuel_record").select("*").execute()
    return response.data
