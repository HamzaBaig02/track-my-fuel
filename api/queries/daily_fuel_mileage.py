import streamlit as st
from supabase import Client
from api.exceptions import *
from utils.logger import logger

supabase: Client = st.session_state["supabase"]

def create_daily_fuel_mileage_record(daily_fuel_mileage_record):
    try:
        logger.info("Attempting to create a daily fuel mileage record.")
        response = (
            supabase.table("daily_fuel_mileage")
            .insert(daily_fuel_mileage_record)
            .execute()
        )
        logger.info("API Success: Daily fuel mileage record created successfully.")
        return response.data[0]
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not create daily fuel mileage record. Error: {e}")
        raise

def get_all_daily_fuel_mileage_records():
    try:
        logger.info("Fetching all daily fuel mileage records.")
        response = supabase.table("daily_fuel_mileage").select("*").execute()
        logger.info("API Success: Daily fuel mileage records fetched successfully.")
        return response.data
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not fetch daily fuel mileage records. Error: {e}")
        return None
