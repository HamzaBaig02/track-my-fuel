import streamlit as st
from supabase import Client
from api.exceptions import *
from utils.logger import logger

supabase: Client = st.session_state["supabase"]

def create_fuel_calculation_record(fuel_calculation_record, fuel_record_id):
    try:
        fuel_calculation_record['fuel_record_id'] = fuel_record_id
        logger.info("Attempting to create a fuel calculation record.")

        response = (
            supabase.table("fuel_calculation")
            .insert(fuel_calculation_record)
            .execute()
        )

        logger.info("API Success: Fuel calculation record created successfully.")
        return response.data
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not create fuel calculation record. Error: {e}")
        raise

def get_all_fuel_calculation_records():
    try:
        logger.info("Fetching all fuel calculation records.")

        response = supabase.table("fuel_calculation").select("*").execute()

        logger.info("API Success: Fuel calculation records fetched successfully.")
        return response.data
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not fetch fuel calculation records")
