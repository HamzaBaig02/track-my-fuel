import streamlit as st
from api.exceptions import SupabaseAPIError
from utils.logger import logger


def create_fuel_record(fuel_record):
    try:
        logger.info("Attempting to create a fuel record.")

        response = (
            st.session_state["supabase"]
            .table("fuel_record")
            .insert(fuel_record)
            .execute()
        )
        filtered_response = [
            {
                k: v
                for k, v in record.items()
                if k
                in [
                    "id",
                    "fueling_date",
                    "fuel_added",
                    "fuel_rate",
                    "reserve_switch_mileage",
                    "fuel_addition_mileage",
                    "fueling_station_name",
                    "fueling_station_location",
                ]
            }
            for record in response.data
        ]
        logger.info("API Success: Fuel record created successfully.")
        return filtered_response[0]
    except Exception as e:
        logger.error(f"API Failure: Could not create fuel record. Error: {e}")
        raise SupabaseAPIError(f"Failed to create fuel record: {e}")


def get_all_fuel_records():
    try:
        logger.info("Fetching all fuel records.")
        response = (
            st.session_state["supabase"]
            .table("fuel_record")
            .select(
                "id,fueling_date,fuel_added,fuel_rate,reserve_switch_mileage,fuel_addition_mileage,fueling_station_name,fueling_station_location"
            )
            .order(
                "fueling_date", desc=False
            )
            .order("created_at", desc=False)
            .execute()
        )

        logger.info("API Success: Fuel records fetched successfully.")
        return response.data
    except Exception as e:
        logger.error(f"API Failure: Could not fetch fuel records. Error: {e}")
        raise SupabaseAPIError(f"Failed to fetch fuel records: {e}")


def get_fuel_record_by_id(id):
    """
    Fetches a fuel record by its ID.
    """
    try:
        logger.info(f"Attempting to fetch fuel record with ID: {id}.")
        response = (
            st.session_state["supabase"]
            .table("fuel_record")
            .select(
                "id,fueling_date,fuel_added,fuel_rate,reserve_switch_mileage,fuel_addition_mileage,fueling_station_name,fueling_station_location"
            )
            .eq("id", id)
            .execute()
        )

        if response.data:
            logger.info("API Success: Fuel record fetched successfully.")
            return response.data[0]
        else:
            logger.warning("API Warning: Record not found.")
            return None
    except Exception as e:
        logger.error(f"API Failure: Could not fetch fuel record. Error: {e}")
        raise SupabaseAPIError(f"Failed to fetch fuel record by ID: {e}")


def get_fuel_record_and_previous_by_id(id):
    try:
        current_record = get_fuel_record_by_id(id)

        if not current_record:
            logger.warning("API Warning: Record not found.")
            return None

        fueling_date = current_record["fueling_date"]

        previous_record_response = (
            st.session_state["supabase"]
            .table("fuel_record")
            .select(
                "id,fueling_date,fuel_added,fuel_rate,reserve_switch_mileage,"
                "fuel_addition_mileage,fueling_station_name,fueling_station_location"
            )
            .lt("fueling_date", fueling_date)
            .order("fueling_date", desc=True)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )

        previous_record = previous_record_response.data[0] if previous_record_response.data else None

        logger.info("API Success: Fuel record and previous record fetched successfully.")
        if previous_record:
            return [previous_record,current_record]
        else:
            return [current_record]

    except Exception as e:
        logger.error(f"API Failure: Could not fetch fuel records. Error: {e}")
        raise SupabaseAPIError(f"Failed to fetch fuel records by ID: {e}")


def delete_fuel_record(id):
    """
    Deletes a fuel record by ID.
    """
    try:
        logger.info(f"Attempting to delete fuel record with ID: {id}.")
        response = (
            st.session_state["supabase"]
            .table("fuel_record")
            .delete()
            .eq("id", id)
            .execute()
        )

        if response.data:
            logger.info("API Success: Fuel record deleted successfully.")
            return {"status": "success", "message": "Record deleted successfully"}
        else:
            logger.warning("API Warning: Record not found for deletion.")
            return None
    except Exception as e:
        logger.error(f"API Failure: Could not delete fuel record. Error: {e}")
        raise SupabaseAPIError(f"Failed to delete fuel record: {e}")


def update_fuel_record(id, update_data):
    """
    Updates a fuel record by ID with the provided update_data dictionary.
    """
    try:
        logger.info(f"Attempting to update fuel record with ID: {id}.")
        response = (
            st.session_state["supabase"]
            .table("fuel_record")
            .update(update_data)
            .eq("id", id)
            .execute()
        )

        if response.data:
            logger.info("API Success: Fuel record updated successfully.")
            return response.data[0]
        else:
            logger.warning("API Warning: Record not found for update.")
            return None
    except Exception as e:
        logger.error(f"API Failure: Could not update fuel record. Error: {e}")
        raise SupabaseAPIError(f"Failed to update fuel record: {e}")



def get_locations():
    """
    Fetches distinct fueling stations and their respective locations.
    """
    try:
        logger.info("Fetching distinct fueling stations and locations.")

        response = (
            st.session_state["supabase"]
            .rpc("get_distinct_fueling_stations_and_locations")
            .execute()
        )

        if response.data:
            logger.info("API Success: Distinct fueling stations and locations fetched successfully.")
            formatted_locations = {
            record["fueling_station_name"]: record["locations"]
            for record in response.data
        }
            return formatted_locations
        else:
            logger.warning("API Warning: No fueling stations or locations found.")
            return {}
    except Exception as e:
        logger.error(f"API Failure: Could not fetch fueling stations and locations. Error: {e}")
        raise SupabaseAPIError(f"Failed to fetch fueling stations and locations: {e}")
