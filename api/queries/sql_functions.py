import streamlit as st
from supabase import Client
from api.exceptions import *

supabase: Client = st.session_state["supabase"]


def create_fuel_and_calculation(fuel_record, fuel_calculation_record):
    """
    This is calling a postgres function through supabase api, the function takes the above params as json and inserts them into respective tables.
    The purpose of this funciton is so that the insertion on two different tables occurs as a single transaction, which is not possible calling supabase rest api create endpoints for our database

    """
    try:
        response = supabase.rpc(
            "create_fuel_and_calculation",
            {
                "fuel_record": fuel_record,
                "fuel_calculation_record": fuel_calculation_record,
            },
        ).execute()
    except Exception:
        raise SupabaseAPIError("Error Creating Record, Please Try Again")
    return response.data["fuel_record"], response.data["fuel_calculation"]
