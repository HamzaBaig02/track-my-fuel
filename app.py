import streamlit as st
from page_functions.home import home_page
from page_functions.auth import auth_page

pg = st.navigation([st.Page(home_page,title="Home"), st.Page(auth_page,title="Login/Signup")])
pg.run()





