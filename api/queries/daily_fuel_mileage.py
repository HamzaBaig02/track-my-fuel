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
        filtered_response = [
            {k: v for k, v in record.items() if k in ["id","date","day_start_mileage"]}
            for record in response.data
        ]
        logger.info("API Success: Daily fuel mileage record created successfully.")
        return filtered_response[0]
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not create daily fuel mileage record. Error: {e}")
        raise

def get_all_daily_fuel_mileage_records():
    try:
        logger.info("Fetching all daily fuel mileage records.")
        response = supabase.table("daily_fuel_mileage").select("id,date,day_start_mileage").execute()
        logger.info("API Success: Daily fuel mileage records fetched successfully.")
        return response.data
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not fetch daily fuel mileage records. Error: {e}")
        return None


def delete_daily_fuel_mileage_record(id):
    """
    Deletes a daily fuel mileage record by ID.
    """
    try:
        logger.info(f"Attempting to delete daily fuel mileage record with ID: {id}.")
        response = supabase.table("daily_fuel_mileage").delete().eq("id", id).execute()

        if response.data:
            logger.info("API Success: Daily fuel mileage record deleted successfully.")
            return {"status": "success", "message": "Record deleted successfully"}
        else:
            logger.warning("API Warning: Record not found for deletion.")
            return {"status": "error", "message": "Record not found"}
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not delete daily fuel mileage record. Error: {e}")
        raise


def update_daily_fuel_mileage_record(id, update_data):
    """
    Updates a daily fuel mileage record by ID with the provided update_data dictionary.
    """
    try:
        logger.info(f"Attempting to update daily fuel mileage record with ID: {id}.")
        response = (
            supabase.table("daily_fuel_mileage")
            .update(update_data)
            .eq("id", id)
            .execute()
        )

        if response.data:
            logger.info("API Success: Daily fuel mileage record updated successfully.")
            return response.data[0]
        else:
            logger.warning("API Warning: Record not found for update.")
            return {"status": "error", "message": "Record not found"}
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not update daily fuel mileage record. Error: {e}")
        raise