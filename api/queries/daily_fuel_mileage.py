import streamlit as st
from supabase import Client


supabase:Client = st.session_state["supabase"]

def create_daily_fuel_mileage_record(daily_fuel_mileage_record):
    response = (
    supabase.table("daily_fuel_mileage")
    .insert(daily_fuel_mileage_record)
    .execute()
    )
    return response.data[0]

def get_all_daily_fuel_mileage_records():
    response = supabase.table("daily_fuel_mileage").select("*").execute()
    return response.data