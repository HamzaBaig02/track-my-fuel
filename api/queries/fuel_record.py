import streamlit as st
from supabase import Client
from api.exceptions import *
from utils.logger import logger

supabase: Client = st.session_state["supabase"]

def create_fuel_record(fuel_record):
    try:
        logger.info("Attempting to create a fuel record.")

        response = (
            supabase.table("fuel_record")
            .insert(fuel_record)
            .execute()
        )

        logger.info("API Success: Fuel record created successfully.")
        return response.data[0]
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not create fuel record. Error: {e}")
        raise

def get_all_fuel_records():
    try:
        logger.info("Fetching all fuel records.")

        response = supabase.table("fuel_record").select("*").execute()

        logger.info("API Success: Fuel records fetched successfully.")
        return response.data
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not fetch fuel records. Error: {e}")
        return None
