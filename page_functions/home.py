import streamlit as st
from components.field_label import render_field_label
from components.fuel_record_form import render_fuel_record_form
from components.fuel_record_update_form import render_update_fuel_record_form
from components.fuel_record_delete import render_delete_fuel_record_form
from datetime import datetime as dt
from utils.auth import protected
from utils.validation import clean_number_input
import pandas as pd
from utils.fuel_calculations import *
from api.queries.fuel_calculation_table import *
from api.queries.fuel_record_table import *
from api.queries.sql_functions import *
from api.queries.daily_fuel_mileage_table import *
from utils.misc import refresh

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

    day_start_mileage_data = {}
    fuel_record = {}
    fuel_calculation = {}

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
        f"<p style='font-size:clamp( 18px, 1.2vw, 24px); color:gray;'>📅 Today's Date: <span style='color:#4CAF50;'>{dt.now().strftime('%d-%m-%Y')}</span></p>",
        unsafe_allow_html=True,
    )
    if st.button("Refresh 🔄"):
        refresh()
    # Divider
    st.divider()

    # Day start mileage form
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
                daily_fuel_submit_toast = st.toast('Submitting...', icon='⌛')
                day_start_mileage_response = create_daily_fuel_mileage_record(day_start_mileage_data)
                st.session_state["day_start_mileage_list"].append(day_start_mileage_response)
                daily_fuel_submit_toast.toast('Record Submitted', icon='🎉')
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

    fuel__record_form_choice = st.selectbox("Select an option", ["Create Record ➕", "Update Record 📝", "Delete ❌"],label_visibility="collapsed")
    if fuel__record_form_choice == "Create Record ➕":
        fuel_record, fuel_calculation = render_fuel_record_form()
    elif fuel__record_form_choice == "Update Record 📝":
        fuel_record_updated = render_update_fuel_record_form()
    elif fuel__record_form_choice == "Delete ❌":
        fuel_record_deleted = render_delete_fuel_record_form()


    # Append data to session state after submission
    if fuel_record and fuel_calculation:
        st.session_state["fuel_record_list"].append(fuel_record)
        st.session_state["calculated_record_list"].append(fuel_calculation)

    # Display Fuel and Calculation Records
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
