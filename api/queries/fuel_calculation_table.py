import streamlit as st
from api.exceptions import *
from utils.logger import logger

def create_fuel_calculation_record(fuel_calculation_record, fuel_record_id):
    try:
        fuel_calculation_record["fuel_record_id"] = fuel_record_id
        logger.info("Attempting to create a fuel calculation record.")

        response = (
            st.session_state["supabase"]
            .table("fuel_calculation")
            .insert(fuel_calculation_record)
            .execute()
        )
        filtered_response = [
            {
                k: v
                for k, v in record.items()
                if k
                in [
                    "id",
                    "fuel_litres",
                    "distance_on_reserve",
                    "fuel_litres_adjusted",
                    "fuel_average",
                    "upcoming_fueling",
                    "fuel_days",
                    "travel_avg",
                    "distance_fuel_adjusted",
                    "fuel_record_id",
                ]
            }
            for record in response.data
        ]

        logger.info("API Success: Fuel calculation record created successfully.")
        return filtered_response[0]
    except SupabaseAPIError as e:
        logger.error(
            f"API Failure: Could not create fuel calculation record. Error: {e}"
        )
        raise


def get_all_fuel_calculation_records():
    try:
        logger.info("Fetching all fuel calculation records.")

        # response = (
        #     st.session_state["supabase"]
        #     .table("fuel_calculation")
        #     .select(
        #         "fuel_record_id,fuel_litres,distance_on_reserve,fuel_litres_adjusted,fuel_average,upcoming_fueling,fuel_days,travel_avg,distance_fuel_adjusted,id"
        #     )
        #     .execute()
        # )

        response = st.session_state["supabase"].rpc("get_sorted_fuel_calculations").execute()

        logger.info("API Success: Fuel calculation records fetched successfully.")
        return response.data
    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not fetch fuel calculation records")



def update_fuel_calculation_record_by_form_id(form_id, data):
    try:
        logger.info(f"Attempting to update fuel calculation record with ID: {id}")

        response = (
            st.session_state["supabase"]
            .table("fuel_calculation")
            .update(data)
            .eq("fuel_record_id", form_id)
            .execute()
        )

        if response.data:
            updated_record = response.data[0]
            logger.info("API Success: Fuel calculation record updated successfully.")
            return updated_record
        else:
            logger.warning("API Warning: No records were updated.")
            return None

    except SupabaseAPIError as e:
        logger.error(f"API Failure: Could not update fuel calculation record. Error: {e}")
        raise


