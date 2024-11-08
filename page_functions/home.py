import streamlit as st
from components.field_label import render_field_label
from components.fuel_record_form import render_fuel_record_form
from components.fuel_record_update_form import render_update_fuel_record_form
from components.fuel_record_delete import render_delete_fuel_record_form
from datetime import datetime as dt
import pytz
from utils.auth import protected
from utils.validation import clean_number_input
import pandas as pd
from utils.fuel_calculations import *
from api.queries.fuel_calculation_table import *
from api.queries.fuel_record_table import *
from api.queries.sql_functions import *
from api.queries.daily_fuel_mileage_table import *
from utils.misc import refresh


def arqum_birthday():
    if "balloons_shown" not in st.session_state:
        st.session_state.balloons_shown = False
    pakistan_tz = pytz.timezone("Asia/Karachi")
    current_time_in_pakistan = datetime.now(pakistan_tz)
    if current_time_in_pakistan.month == 12 and current_time_in_pakistan.day == 2:
        if not st.session_state.balloons_shown:
            st.balloons()
            st.session_state.balloons_shown = True
    else:
        logger.info(f"Today is {current_time_in_pakistan.strftime('%B %d')}, not Arqum's birthday.")


@protected()
def render_home():

    def init_page_session_state():
        import time

        if "fuel_record_list" not in st.session_state:
            st.session_state["fuel_record_list"] = []
        if "calculated_record_list" not in st.session_state:
            st.session_state["calculated_record_list"] = []
        if "day_start_mileage_list" not in st.session_state:
            st.session_state["day_start_mileage_list"] = []
        if "data_loaded" not in st.session_state:
            st.session_state["data_loaded"] = False

        if not st.session_state["data_loaded"]:
            loading_placeholder = st.empty()

            with loading_placeholder.container():
                st.markdown(
                    """
    <div style="display: flex; justify-content: center; align-items: center; height: 80vh;">
        <div style="text-align: center;">
            <p style="font-size: 28px; color: #4CAF50; font-weight: bold; margin-bottom: 20px;">
                ⛽ Loading data for <span style="color: #FFA726;">Track My Fuel</span>...
            </p>
            <div class="loader" style="font-size: 50px; margin: 0 auto;">🏍️</div>
            <p style="font-size: 16px; color: #9e9e9e; margin-top: 20px;">
                🚗 Fetching your latest fuel records... Hang tight! ⏳
            </p>
        </div>
    </div>
    <style>
    .loader {
        display: inline-block;
        position: relative;
        animation: ride 4s ease-in-out infinite;
    }
    @keyframes ride {
        0% { transform: translateX(100px) scaleX(1); }   /* Start from right, facing left */
        45% { transform: translateX(-100px) scaleX(1); } /* Move to left without flipping */
        50% { transform: translateX(-100px) scaleX(-1); } /* Pause at left, flip to face right */
        95% { transform: translateX(100px) scaleX(-1); } /* Move back to right without flipping */
        100% { transform: translateX(100px) scaleX(1); } /* Pause at right, flip to face left */
    }
    </style>
    """,
                    unsafe_allow_html=True,
                )
                st.session_state["fuel_record_list"] = get_all_fuel_records()
                st.session_state["calculated_record_list"] = (
                    get_all_fuel_calculation_records()
                )
                st.session_state["day_start_mileage_list"] = (
                    get_all_daily_fuel_mileage_records()
                )
                st.session_state["data_loaded"] = True
                st.rerun()

    init_page_session_state()

    day_start_mileage_data = {}
    fuel_record = {}
    fuel_calculation = {}

    st.markdown(
    "<h1 style='font-size:clamp(24px,2vw,40px);text-align:center;'>⛽ Track My Fuel 😩💧</h1>",
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
        st.dataframe(pd.DataFrame(st.session_state["day_start_mileage_list"]))

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
        st.dataframe(df_record)

        st.divider()
        st.markdown(
            "<h2 style='font-size:clamp(22px,1.7vw,35px);'>Fuel Calculation Records</h2>",
            unsafe_allow_html=True,
        )
        st.dataframe(df_calc)


render_home()
arqum_birthday()
