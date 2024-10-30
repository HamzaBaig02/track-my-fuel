import streamlit as st

pg = st.navigation([st.Page("page_functions/home.py",title="Home"), st.Page("page_functions/auth.py",title="Login/Signup")])
pg.run()





