import streamlit as st


try:
    st.markdown(
    "<h1 style='font-size:clamp(24px,2vw,40px);text-align:center;'>⛽ Track My Fuel 😩💧</h1>",
    unsafe_allow_html=True,
)


    st.session_state['supabase'].auth.sign_out()
    st.session_state.clear()
    st.subheader("You've been logged out successfully!")

    st.switch_page("page_functions/auth.py")
except Exception as e:
    st.error(str(e))
    st.switch_page("page_functions/auth.py")