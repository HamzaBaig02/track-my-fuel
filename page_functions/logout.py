import streamlit as st


try:
    st.session_state['supabase'].auth.sign_out()
    st.session_state.clear()
    st.subheader("You've been logged out successfully!")

    st.switch_page("page_functions/auth.py")
except Exception as e:
    st.error(str(e))
    st.switch_page("page_functions/auth.py")