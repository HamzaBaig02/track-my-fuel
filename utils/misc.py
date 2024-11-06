import streamlit as st
from api.queries.fuel_calculation_table import *
from api.queries.fuel_record_table import *
from api.queries.sql_functions import *
from api.queries.daily_fuel_mileage_table import *

def refresh():
        try:
            refresh_toast = st.toast('Refreshing tables...', icon='⌛')
            st.session_state["fuel_record_list"] = get_all_fuel_records()
            st.session_state["calculated_record_list"] = get_all_fuel_calculation_records()
            st.session_state["day_start_mileage_list"] = get_all_daily_fuel_mileage_records()
            refresh_toast.toast('Tables refreshed!', icon='🎉')
        except:
              st.toast('Failed to refresh one or more tables', icon='⚠️')