import streamlit as st
from components.field_label import render_field_label
from datetime import datetime as dt
from utils.validation import clean_number_input
from utils.fuel_calculations import *
from api.queries.fuel_calculation_table import *
from api.queries.fuel_record_table import *
from api.queries.sql_functions import *
from api.queries.daily_fuel_mileage_table import *
from components.constants import LOCATIONS


def render_fuel_record_form():
    """Render the form to capture fuel record details."""
    fuel_data = {}

    # Fueling Date
    render_field_label(text="📅 Fueling Date")
    fuel_data["fueling_date"] = st.date_input("Fueling date", dt.now(), label_visibility="collapsed", format="DD/MM/YYYY").strftime("%Y-%m-%d")

    # Fuel Added
    render_field_label(text="⛽ Fuel Added")
    fuel_data["fuel_added"] = clean_number_input(
        st.number_input(
            "Enter fuel added in liters",
            min_value=0.0,
            step=0.1,
            format="%.2f",
            label_visibility="collapsed",
        )
    )

    # Fuel Rate
    render_field_label(text="💲 Fuel Rate")
    fuel_data["fuel_rate"] = clean_number_input(
        st.number_input(
            "Enter fuel rate per liter",
            min_value=0.0,
            step=0.1,
            format="%.2f",
            label_visibility="collapsed",
        )
    )

    # Fueling Station Information
    fueling_station_info_col1, fueling_station_info_col2 = st.columns(2)
    with fueling_station_info_col1:
        render_field_label(text="🏢 Fueling Station Name")
        fuel_data["fueling_station_name"] = st.selectbox(
            "Enter fueling station name",
            list(LOCATIONS.keys()),
            label_visibility="collapsed",
        )
    with fueling_station_info_col2:
        render_field_label(text="📍 Fueling Station Location")
        fuel_data["fueling_station_location"] = st.selectbox(
            "Enter fueling station location",
            LOCATIONS[fuel_data["fueling_station_name"]],
            label_visibility="collapsed",
        )

    # Reserve Switch Mileage
    render_field_label(text="🔄 Reserve Switch Mileage")
    fuel_data["reserve_switch_mileage"] = clean_number_input(
        st.number_input(
            "Enter reserve switch mileage when fuel was added (km per liter)",
            min_value=0.0,
            step=0.1,
            format="%.2f",
            label_visibility="collapsed",
        )
    )

    # Fuel Addition Mileage
    render_field_label(text="📊 Fuel Addition Mileage")
    fuel_data["fuel_addition_mileage"] = clean_number_input(
        st.number_input(
            "Enter mileage when fuel was added (km per liter)",
            min_value=0.00,
            step=0.10,
            format="%.2f",
            label_visibility="collapsed",
        )
    )

    # Submit Button
    fuel_record, fuel_calculation = None, None
    if st.button("Submit"):
        try:
            with st.spinner("Submitting..."):
                submit_toast = st.toast('Submitting...', icon='⌛')
                fuel_record_list_temp = st.session_state["fuel_record_list"].copy()
                fuel_record_list_temp.append(fuel_data)
                processed_fuel_data = process_fuel_data(fuel_record_list_temp)

                fuel_record, fuel_calculation = create_fuel_and_calculation(
                    fuel_record=fuel_data,
                    fuel_calculation_record=processed_fuel_data
                )

                submit_toast.toast('Record Submitted', icon='🎉')
        except SupabaseAPIError as e:
            st.error(e)

    return fuel_record, fuel_calculation