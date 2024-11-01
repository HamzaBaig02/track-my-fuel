import streamlit as st
from components.field_label import render_field_label
from datetime import datetime
from utils.auth import protected
from utils.validation import clean_number_input


@protected()
def render_home(user=None):

    locations = {
        "Total": ["FC College", "Barkat Market", "Central Park", "Jinnah Hospital"],
        "GO": ["Pekhewal Morr", "Gajjumatta"],
        "PSO": ["Karim Market", "Muslim Town", "Barkat Market"],
        "Shell": ["Karim Market"],
    }

    # Initialize the dictionary to collect all variables
    fuel_data = {}

    st.markdown(
        "<h1 style='font-size:clamp(24px,2vw,40px);'>Track My Fuel 😩💦</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<p style='color:gray; font-size:20px;'>Welcome to the <b>Ultimate Fuel Tracker 🚗💨 </b>! This app helps you keep an eye on all things fuel-related!
        Let's hit the road and make every kilometer count! 🚀</p>""",
        unsafe_allow_html=True,
    )

    # Date variable
    fuel_data["date"] = datetime.now().strftime("%d-%m-%Y")
    st.markdown(
        f"<p style='font-size:24px; color:gray;'>📅 Date: <span style='color:#4CAF50;'>{fuel_data['date']}</span></p>",
        unsafe_allow_html=True,
    )

    # Divider and Section Header
    st.divider()
    st.markdown(
        "<h2 style='font-size:clamp(22px,1.7vw,35px);'>Fuel Record</h2>",
        unsafe_allow_html=True,
    )

    # day start mileage
    render_field_label(text="🚗 Day Start Mileage")
    fuel_data["day_start_mileage"] = clean_number_input(
        st.number_input(
            "Enter mileage in kilometers (e.g., 12.5):",
            min_value=0.0,
            step=0.1,
            format="%.2f",
            label_visibility="collapsed",
        )
    )

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
    col1, col2 = st.columns(2)

    with col1:
        render_field_label(text="🏢 Fueling Station Name")
        fuel_data["fueling_station_name"] = st.selectbox(
            "Enter fueling station name",
            list(locations.keys()),
            label_visibility="collapsed",
        )
    with col2:
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
            min_value=0.0,
            step=0.1,
            format="%.2f",
            label_visibility="collapsed",
        )
    )

    # Display the dictionary (optional for debugging or confirmation)
    st.write("Fuel Data:", fuel_data)


render_home()
