import streamlit as st
from datetime import datetime

st.title("Track My Fuel 😩💦")

st.markdown(
    "<p style='color:gray; font-size:20px;'>This App tracks relevant fuel related metrics</p>",
    unsafe_allow_html=True
)

todays_date = datetime.now().strftime("%d-%m-%Y")
st.markdown(
    f"<p style='font-size:24px; color:gray;'>📅 Date: <span style='color:#4CAF50;'>{todays_date}</span></p>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='font-size:24px; color:gray; margin-bottom:0px;'>🚗 Day Start Mileage</p>",
    unsafe_allow_html=True
)

day_start_mileage = st.number_input("Enter mileage in kilometers (e.g., 12.5):", min_value=0.0, step=0.1, format="%.2f",label_visibility='collapsed')

#Fuel record section

st.divider()

st.header("Fuel Record")

# Fuel Added component
st.markdown(
    "<p style='font-size:24px; color:gray; margin-bottom:0px;'>⛽ Fuel Added</p>",
    unsafe_allow_html=True
)
fuel_added = st.number_input("Enter fuel added in liters", min_value=0.0, step=0.1, format="%.2f", label_visibility='collapsed')

# Fuel Rate component
st.markdown(
    "<p style='font-size:24px; color:gray; margin-bottom:0px;'>💲 Fuel Rate</p>",
    unsafe_allow_html=True
)
fuel_rate = st.number_input("Enter fuel rate per liter", min_value=0.0, step=0.1, format="%.2f", label_visibility='collapsed')

# Fueling Station component
st.markdown(
    "<p style='font-size:24px; color:gray; margin-bottom:0px;'>🏢 Fueling Station</p>",
    unsafe_allow_html=True
)
fueling_station = st.text_input("Enter fueling station name", label_visibility='collapsed')

# Reserve Switch component
st.markdown(
    "<p style='font-size:24px; color:gray; margin-bottom:0px;'>🔄 Reserve Switch</p>",
    unsafe_allow_html=True
)
reserve_switch = st.selectbox("Select reserve switch status", ["On", "Off"], label_visibility='collapsed')

# Fuel Mileage component
st.markdown(
    "<p style='font-size:24px; color:gray; margin-bottom:0px;'>📊 Fuel Mileage</p>",
    unsafe_allow_html=True
)
fuel_mileage = st.number_input("Enter fuel mileage (km per liter)", min_value=0.0, step=0.1, format="%.2f", label_visibility='collapsed')

