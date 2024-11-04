import streamlit as st
from components.field_label import render_field_label
from datetime import datetime as dt
from utils.auth import protected
from utils.validation import clean_number_input
import pandas as pd
from utils.fuel_calculations import *
from api.queries.fuel_calculation import *
from api.queries.fuel_record import *
from api.queries.sql_functions import *
from api.queries.daily_fuel_mileage import *


@protected()
def render_home(user=None):
    def init_page_session_state():
        if "fuel_record_list" not in st.session_state:
            st.session_state["fuel_record_list"] = get_all_fuel_records()
        if "calculated_record_list" not in st.session_state:
            st.session_state["calculated_record_list"] = get_all_fuel_calculation_records()
        if "day_start_mileage_list" not in st.session_state:
            st.session_state["day_start_mileage_list"] = get_all_daily_fuel_mileage_records()

    init_page_session_state()


    locations = {
        "Total": ["FC College", "Barkat Market", "Central Park", "Jinnah Hospital"],
        "GO": ["Pekhewal Morr", "Gajjumatta"],
        "PSO": ["Karim Market", "Muslim Town", "Barkat Market"],
        "Shell": ["Karim Market"],
    }

    fuel_data = {}
    processed_fuel_data = {}
    day_start_mileage_data = {}

    st.markdown(
        "<h1 style='font-size:clamp(24px,2vw,40px);'>Track My Fuel 😩💦</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<p style='color:gray; font-size:20px;'>Welcome to the <b>Ultimate Fuel Tracker 🚗💨 </b>! This app helps you keep an eye on all things fuel-related!
        Let's hit the road and make every kilometer count! 🚀</p>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<p style='font-size:clamp( 18px, 1.2vw, 24px); color:gray;'>📅 Today's Date: <span style='color:#4CAF50;'>{dt.now().strftime("%d-%m-%Y")}</span></p>",
        unsafe_allow_html=True,
    )

    # Divider
    st.divider()

# Day start mileage component
    render_field_label(text="🚗 Day Start Mileage")
    day_start_mileage_col1, day_start_mileage_col2, day_start_mileage_col3 = st.columns(3)
    with day_start_mileage_col1:
        day_start_mileage_data['day_start_mileage'] = clean_number_input(
            st.number_input(
                "Enter mileage in kilometers (e.g., 12.5):",
                min_value=0.0,
                placeholder=0,
                step=0.1,
                format="%.2f",
                label_visibility="collapsed",
            )
        )

    with day_start_mileage_col2:
        day_start_mileage_data['date'] = st.date_input("Fueling date", dt.now(),label_visibility="collapsed",format="DD/MM/YYYY",key="date2").strftime("%Y-%m-%d")
    with day_start_mileage_col3:
        if st.button("Submit",key="button2"):
            try:
                create_daily_fuel_mileage_record(day_start_mileage_data)
                st.session_state["day_start_mileage_list"].append(day_start_mileage_data)
                st.toast('Record Submitted', icon='🎉')
            except SupabaseAPIError as e:
                st.error(str(e))

    if st.session_state["day_start_mileage_list"]:
        st.write(pd.DataFrame(st.session_state["day_start_mileage_list"]))

    # Divider
    st.divider()
    st.markdown(
        "<h2 style='font-size:clamp(22px,1.7vw,35px);'>Fuel Record</h2>",
        unsafe_allow_html=True,
    )

    #date
    render_field_label(text="📅 Fueling Date")
    fuel_data["fueling_date"] = st.date_input("Fueling date", dt.now(),label_visibility="collapsed",format="DD/MM/YYYY").strftime("%Y-%m-%d")
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
            list(locations.keys()),
            label_visibility="collapsed",
        )
    with fueling_station_info_col2:
        render_field_label(text="📍 Fueling Station Location")
        fuel_data["fueling_station_location"] = st.selectbox(
            "Enter fueling station location",
            locations[fuel_data["fueling_station_name"]],
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


    if st.button("Submit"):
        try:
            st.session_state["fuel_record_list"].append(fuel_data)
            processed_fuel_data = process_fuel_data(st.session_state["fuel_record_list"])
            st.session_state["calculated_record_list"].append(processed_fuel_data)
            create_fuel_and_calculation(fuel_record=fuel_data,fuel_calculation_record=processed_fuel_data)
            st.toast('Record Submitted', icon='🎉')
        except SupabaseAPIError as e:
            st.session_state["fuel_record_list"].pop()
            st.session_state["calculated_record_list"].pop()
            st.error(e)




    if st.session_state.get("fuel_record_list", None):
        df_record = pd.DataFrame(st.session_state["fuel_record_list"])
        df_calc = pd.DataFrame(st.session_state["calculated_record_list"])

        st.divider()
        st.markdown(
        "<h2 style='font-size:clamp(22px,1.7vw,35px);'>Fuel Records</h2>",
        unsafe_allow_html=True,
        )
        st.write(df_record)

        st.divider()
        st.markdown(
        "<h2 style='font-size:clamp(22px,1.7vw,35px);'>Fuel Calculation Records</h2>",
        unsafe_allow_html=True,
        )
        st.write(df_calc)


render_home()
