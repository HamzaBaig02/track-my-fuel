import streamlit as st
from components.field_label import render_field_label
from utils.validation import clean_number_input
from datetime import datetime as dt
from components.constants import LOCATIONS
from api.queries.fuel_record_table import get_fuel_record_by_id, update_fuel_record

def render_update_fuel_record_form():
    record_id = st.text_input("Enter Record ID", "")

    if st.button("Fetch Record") and record_id:
        submit_toast = st.toast('Fetching Record...', icon='⌛')

        fuel_record = get_fuel_record_by_id(record_id)

        if fuel_record:
            st.session_state["fuel_record_to_update"] = fuel_record
            submit_toast.toast('Record Fetched!', icon='🎉')
        else:
            st.error("Record not found.")
            st.session_state["fuel_record_to_update"] = None


    if st.session_state.get("fuel_record_to_update", None):
        fuel_data = {}

        # Fueling Date
        render_field_label(text="📅 Fueling Date")
        fuel_data["fueling_date"] = st.date_input(
            "Fueling date",
            dt.strptime(st.session_state["fuel_record_to_update"]["fueling_date"], "%Y-%m-%d"),
            label_visibility="collapsed",
            key="fueling_date_input"
        ).strftime("%Y-%m-%d")

        # Fuel Added
        render_field_label(text="⛽ Fuel Added")
        fuel_data["fuel_added"] = clean_number_input(
            st.number_input(
                "Enter fuel added in liters",
                value=float(st.session_state["fuel_record_to_update"]["fuel_added"]),
                min_value=0.0,
                step=0.1,
                format="%.2f",
                label_visibility="collapsed",
                key="fuel_added_input"
            )
        )

        # Fuel Rate
        render_field_label(text="💲 Fuel Rate")
        fuel_data["fuel_rate"] = clean_number_input(
            st.number_input(
                "Enter fuel rate per liter",
                value=float(st.session_state["fuel_record_to_update"]["fuel_rate"]),
                min_value=0.0,
                step=0.1,
                format="%.2f",
                label_visibility="collapsed",
                key="fuel_rate_input"
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
                index=list(LOCATIONS.keys()).index(st.session_state["fuel_record_to_update"]["fueling_station_name"]),
                key="fueling_station_name_input"
            )
        with fueling_station_info_col2:
            render_field_label(text="📍 Fueling Station Location")
            fuel_data["fueling_station_location"] = st.selectbox(
                "Enter fueling station location",
                LOCATIONS[fuel_data["fueling_station_name"]],
                label_visibility="collapsed",
                index=LOCATIONS[st.session_state["fuel_record_to_update"]["fueling_station_name"]].index(st.session_state["fuel_record_to_update"]["fueling_station_location"]),
                key="fueling_station_location_input"
            )

        # Reserve Switch Mileage
        render_field_label(text="🔄 Reserve Switch Mileage")
        fuel_data["reserve_switch_mileage"] = clean_number_input(
            st.number_input(
                "Enter reserve switch mileage when fuel was added (km per liter)",
                value=float(st.session_state["fuel_record_to_update"]["reserve_switch_mileage"]),
                min_value=0.0,
                step=0.1,
                format="%.2f",
                label_visibility="collapsed",
                key="reserve_switch_mileage_input"
            )
        )

        # Fuel Addition Mileage
        render_field_label(text="📊 Fuel Addition Mileage")
        fuel_data["fuel_addition_mileage"] = clean_number_input(
            st.number_input(
                "Enter mileage when fuel was added (km per liter)",
                value=float(st.session_state["fuel_record_to_update"]["fuel_addition_mileage"]),
                min_value=0.00,
                step=0.10,
                format="%.2f",
                label_visibility="collapsed",
                key="fuel_addition_mileage_input"
            )
        )

        if st.button("Update Record"):
            try:
                submit_toast = st.toast('Updating...', icon='⌛')
                update_fuel_record(record_id, fuel_data)
                st.success("Record updated successfully!")

                st.session_state["fuel_record_to_update"] = None
                submit_toast.toast('Record Updated!', icon='🎉')
                st.rerun()
            except Exception as e:
                st.error(f"Failed to update record: {e}")


