import streamlit as st
from components.field_label import render_field_label
from datetime import datetime as dt
from components.constants import LOCATIONS
from api.queries.fuel_record_table import get_fuel_record_by_id, delete_fuel_record
from utils.misc import refresh


def render_delete_fuel_record_form():
    record_id = st.text_input("Enter Record ID to Delete", "")

    if st.button("Fetch Record") and record_id:
        submit_toast = st.toast('Fetching Record...', icon='⌛')
        fuel_record = get_fuel_record_by_id(record_id)

        if fuel_record:
            st.session_state["fuel_record_to_delete"] = fuel_record
            submit_toast.toast('Record Fetched!', icon='🎉')
        else:
            st.error("Record not found.")
            st.session_state["fuel_record_to_delete"] = None

    if st.session_state.get("fuel_record_to_delete", None):
        fuel_data = st.session_state["fuel_record_to_delete"]

        # Display fields with disabled attribute set to True
        # Fueling Date
        render_field_label(text="📅 Fueling Date")
        st.date_input(
            "Fueling date",
            dt.strptime(fuel_data["fueling_date"], "%Y-%m-%d"),
            label_visibility="collapsed",
            key="delete_fueling_date_input",
            disabled=True
        )

        # Fuel Added
        render_field_label(text="⛽ Fuel Added")
        st.number_input(
            "Fuel added in liters",
            value=float(fuel_data["fuel_added"]),
            min_value=0.0,
            step=0.1,
            format="%.2f",
            label_visibility="collapsed",
            key="delete_fuel_added_input",
            disabled=True
        )

        # Fuel Rate
        render_field_label(text="💲 Fuel Rate")
        st.number_input(
            "Fuel rate per liter",
            value=float(fuel_data["fuel_rate"]),
            min_value=0.0,
            step=0.1,
            format="%.2f",
            label_visibility="collapsed",
            key="delete_fuel_rate_input",
            disabled=True
        )

        # Fueling Station Information
        fueling_station_info_col1, fueling_station_info_col2 = st.columns(2)
        with fueling_station_info_col1:
            render_field_label(text="🏢 Fueling Station Name")
            st.selectbox(
                "Fueling station name",
                list(LOCATIONS.keys()),
                index=list(LOCATIONS.keys()).index(fuel_data["fueling_station_name"]),
                label_visibility="collapsed",
                key="delete_fueling_station_name_input",
                disabled=True
            )
        with fueling_station_info_col2:
            render_field_label(text="📍 Fueling Station Location")
            st.selectbox(
                "Fueling station location",
                LOCATIONS[fuel_data["fueling_station_name"]],
                index=LOCATIONS[fuel_data["fueling_station_name"]].index(fuel_data["fueling_station_location"]),
                label_visibility="collapsed",
                key="delete_fueling_station_location_input",
                disabled=True
            )

        # Reserve Switch Mileage
        render_field_label(text="🔄 Reserve Switch Mileage")
        st.number_input(
            "Reserve switch mileage (km per liter)",
            value=float(fuel_data["reserve_switch_mileage"]),
            min_value=0.0,
            step=0.1,
            format="%.2f",
            label_visibility="collapsed",
            key="delete_reserve_switch_mileage_input",
            disabled=True
        )

        # Fuel Addition Mileage
        render_field_label(text="📊 Fuel Addition Mileage")
        st.number_input(
            "Fuel addition mileage (km per liter)",
            value=float(fuel_data["fuel_addition_mileage"]),
            min_value=0.00,
            step=0.10,
            format="%.2f",
            label_visibility="collapsed",
            key="delete_fuel_addition_mileage_input",
            disabled=True
        )

        if st.button("Delete Record"):
            try:
                submit_toast = st.toast('Deleting...', icon='⌛')
                delete_fuel_record(record_id)
                st.success("Record deleted successfully!")
                st.session_state["fuel_record_to_delete"] = None
                submit_toast.toast('Record Deleted!', icon='🗑️')
                refresh()
                st.rerun()
            except Exception as e:
                st.error(f"Failed to delete record: {e}")
