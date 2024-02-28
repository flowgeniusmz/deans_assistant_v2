import streamlit as st
import pandas as pd

def append_message_to_message_dataframe(varMessageData):
    new_row_messages = {
        "": varMessageData['role'],
        "": varMessageData['content'],
        "": st.session_state.thread_id,
        "": varMessageData['messageid'],
        "": varMessageData['runid'],
        "": st.session_state.session_id,
        "": varMessageData['createdatunix'],
        "": varMessageData['createdatdatetime']
    }

    st.session_state.dataframe_messages._append(new_row_messages, ignore_index=True)