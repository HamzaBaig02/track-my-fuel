import streamlit as st
from supabase import Client


supabase:Client = st.session_state["supabase"]

def create_fuel_calculation_record(fuel_calculation_record,fuel_record_id):
    fuel_calculation_record['fuel_record_id'] = fuel_record_id
    response = (
    supabase.table("fuel_calculation")
    .insert(fuel_calculation_record)
    .execute()
    )

    return response.data

def get_all_fuel_calculation_records():
    response = supabase.table("fuel_calculation").select("*").execute()
    return response.data