import streamlit as st
import pandas as pd

def append_message_to_log(varMessageData):
    temp_dataframe = pd.DataFrame([varMessageData])
    temp_dataframe.to_csv(st.secrets.streamlit.data_message_log_path, mode="a", index=False, header=False)
    temp_dataframe = pd.DataFrame(columns=temp_dataframe.columns)
    