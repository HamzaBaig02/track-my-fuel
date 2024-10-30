import streamlit as st
from utils.auth import supabase

#setting user in session
# try:
#     response = supabase.auth.get_user()
#     st.session_state['user'] = response.user
# except Exception as e:
#     print(str(e))


pg = st.navigation([
    st.Page("page_functions/home.py", title="Home", icon="🏠"),
    st.Page("page_functions/auth.py", title="Login/Signup", icon="🔑"),
    st.Page("page_functions/logout.py", title="Logout", icon="🚪")
])
pg.run()





