import streamlit as st
from config import pagesetup as ps

# 0. Page Config
ps.get_st_page_config()
ps.get_global_page_font()

# 1. Page Title
ps.get_deans_assistant_title(3)

# 2. Page Overview
ps.get_overview(3)

# 3. Page Warning

st.info(
    body="**IN PROGRESS: Actions Panel In Development:** The **Actions Panel** is currently under construction and unavailable. More information will be posted as it is available!",
            icon="⚠️"
)
