import streamlit as st
import pandas as pd

def append_message_to_message_dataframe(varMessageData):
    new_row_messages = {
        "Role": varMessageData['role'],
        "Content": varMessageData['content'],
        "Thread Id": st.session_state.thread_id,
        "Message Id": varMessageData['messageid'],
        "Run Id": varMessageData['runid'],
        "Session Id": st.session_state.session_id,
        "Created At Unix": varMessageData['createdatunix'],
        "Created At Datetime": varMessageData['createdatdatetime']
    }

    st.session_state.dataframe_messages._append(new_row_messages, ignore_index=True)