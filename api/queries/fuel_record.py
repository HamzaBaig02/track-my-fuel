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
        filtered_response = [
            {k: v for k, v in record.items() if k in ["id","fueling_date","fuel_added","fuel_rate","reserve_switch_mileage","fuel_addition_mileage","fueling_station_name","fueling_station_location"]}
            for record in response.data
        ]
        logger.info("API Success: Fuel record created successfully.")
        return filtered_response[0]
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not create fuel record. Error: {e}")
        raise

def get_all_fuel_records():
    try:
        logger.info("Fetching all fuel records.")

        response = supabase.table("fuel_record").select("id,fueling_date,fuel_added,fuel_rate,reserve_switch_mileage,fuel_addition_mileage,fueling_station_name,fueling_station_location").execute()

        logger.info("API Success: Fuel records fetched successfully.")
        return response.data
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not fetch fuel records. Error: {e}")
        return None


def delete_fuel_record(id):
    """
    Deletes a fuel record by ID.
    """
    try:
        logger.info(f"Attempting to delete fuel record with ID: {id}.")
        response = supabase.table("fuel_record").delete().eq("id", id).execute()

        if response.data:
            logger.info("API Success: Fuel record deleted successfully.")
            return {"status": "success", "message": "Record deleted successfully"}
        else:
            logger.warning("API Warning: Record not found for deletion.")
            return {"status": "error", "message": "Record not found"}
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not delete fuel record. Error: {e}")
        raise


def update_fuel_record(id, update_data):
    """
    Updates a fuel record by ID with the provided update_data dictionary.
    """
    try:
        logger.info(f"Attempting to update fuel record with ID: {id}.")
        response = (
            supabase.table("fuel_record")
            .update(update_data)
            .eq("id", id)
            .execute()
        )

        if response.data:
            logger.info("API Success: Fuel record updated successfully.")
            return response.data[0]
        else:
            logger.warning("API Warning: Record not found for update.")
            return {"status": "error", "message": "Record not found"}
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not update fuel record. Error: {e}")
        raise
