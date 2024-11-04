import streamlit as st
from api.exceptions import *
from utils.logger import logger


def create_fuel_and_calculation(fuel_record, fuel_calculation_record):
    """
    This is calling a postgres function through supabase api, the function takes the above params as json and inserts them into respective tables.
    The purpose of this funciton is so that the insertion on two different tables occurs as a single transaction, which is not possible calling supabase rest api create endpoints for our database.
    """
    try:
        logger.info("Attempting to execute create_fuel_and_calculation SQL function.")

        response = st.session_state["supabase"].rpc(
            "create_fuel_and_calculation",
            {
                "fuel_record": fuel_record,
                "fuel_calculation_record": fuel_calculation_record,
            },
        ).execute()

        logger.info("API Success: create_fuel_and_calculation SQL function executed successfully.")

        return response.data["fuel_record"], response.data["fuel_calculation"]

    except Exception as e:
        logger.error(f"API Failure: Error executing create_fuel_and_calculation SQL function. Error: {e}")
        raise SupabaseAPIError("Error Creating Record, Please Try Again")
