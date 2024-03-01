import streamlit as st
from config import pagesetup as ps, sessionstates as ss
from config import pagesetup as ps

with open( "config/style.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# 0. Page Config
ps.get_st_page_config()

# 1. Page Title
ps.get_deans_assistant_title(0)

# 2. Page Overview
ps.get_overview(0)

# 3. Session State Initalization
ss.get_initial_session_states()

# 4. Page Links
link_container = st.container(border=True)
with link_container:
    link_columns = st.columns(2)
    with link_columns[0]:
        ps.get_page_link(1)
        ps.get_page_link(3)
    with link_columns[1]:
        ps.get_page_link(2)
        ps.get_page_link(4)

# 5. Set global Font
#ps.get_page_font()
