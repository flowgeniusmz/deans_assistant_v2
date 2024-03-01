import streamlit as st
from config import pagesetup as ps, toastalerts as ta, sessionstates as ss
from openai import OpenAI
import time
from datetime import datetime
from functions import append_to_dataframe_messages, append_to_log
import base64

# 0. Page Config
ps.get_st_page_config()
ps.get_global_page_font()

# 0. Set Instances
client = OpenAI(api_key=st.secrets.openai.api_key)

# 0. Check Session State
if "start_chat" not in st.session_state:
    ss.get_initial_session_states()


# 1. Page Title
ps.get_deans_assistant_title(1)

# 2. Page Overview
ps.get_overview(1)

# 3. Create Container to Display Chat Messages
chat_container = st.container(border=True, height=350)

# 4. Display Existing Messages in St.Session_State.Messages (will display initial message if no chat messages entered)
with chat_container:
    for existing_message in st.session_state.messages:
        existing_message_role = existing_message["role"]
        existing_message_content = existing_message["content"]
        with st.chat_message(existing_message_role):
            st.markdown(existing_message_content)

# 5. Set Chat_Input and Await User Input
if prompt := st.chat_input("Enter your question (Ex: A student has their third tardy. What consequences should be considered?)"):

# 6. Display Chat_Input (prompt) in chat container
    prompt_role = "user"
    prompt_content = prompt
    with chat_container:
        with st.chat_message(prompt_role):
            st.markdown(prompt_content)

# 7. Set Toast Alert (Start) and Chat Status (Start)
    ta.toast_alert_start("Initiating response...")
    with chat_container:
        status = st.status(
            label="Initiating response...",
            expanded=False,
            state="running"
        )

# 8. Create New Thread Message
    new_message = client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role=prompt_role,
        content=prompt_content
    )
    print(new_message)

# 9. Create New Run
    st.session_state.run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=st.secrets.openai.assistant_id,
        additional_instructions=st.session_state.run_instructions
    )

# 10. Create Full Message Object and Append to St.SessionState Messages
    prompt_message = {"role": prompt_role, "content": prompt_content, "messageid": new_message.id, "runid": st.session_state.run.id, "createdatunix": new_message.created_at, "createdatdatetime": datetime.utcfromtimestamp(new_message.created_at)}
    st.session_state.messages.append(prompt_message)
    append_to_log.append_message_to_log(prompt_message)
    append_to_dataframe_messages.append_message_to_message_dataframe(prompt_message)
    print(prompt_message)
    print(st.session_state.dataframe_messages)

# 11. Check run status loop until run.status = complete
    while st.session_state.run.status != "completed":
        time.sleep(3)
        st.session_state.run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread_id,
            run_id=st.session_state.run.id
        )

# 12. Toast Alert Update and Status Update During Loop
        ta.toast_alert_waiting("Awaiting response...")
        with chat_container:
            status.write(f"Checking response status...{st.session_state.run.status}")

# 13. Toast Alert Update and Status Update when COMPLETE
    ta.toast_alert_end("Reponse Recieved!")
    with chat_container:
        status.update(
            label="Response recieved!",
            expanded=False,
            state="complete"
        )

# 14. Retrieve Thread Message List
    thread_messages = client.beta.threads.messages.list(
        thread_id=st.session_state.thread_id
    )
    print(thread_messages)

# 15. Retrieve most recent assistant message by looping through each message in thread_messages and looking for the current run_id and role = "assistant"
    for thread_message in thread_messages:
        if thread_message.run_id == st.session_state.run.id and thread_message.role == "assistant":

# 16. Set Message Values
            thread_message_run_id = thread_message.run_id
            thread_message_role = thread_message.role
            thread_message_id = thread_message.id
            thread_message_unix = thread_message.created_at
            thread_message_datetime = datetime.utcfromtimestamp(thread_message_unix)
            thread_message_text = thread_message.content[0].text
            print(thread_message_text)
            thread_message_content = thread_message_text.value
            print(thread_message_content)
            thread_message_annotations = thread_message_text.annotations
            print(thread_message_annotations)
# 17. Get Citations from annotations
            citations = []
            thread_message_content_replace = thread_message_content
            print(thread_message_content_replace)
            for index, annotation in enumerate(thread_message_annotations):
                thread_message_content_replace = thread_message_content_replace.replace(annotation.text, f' [{index}]')
                print(thread_message_content_replace)
                if (file_citation:=getattr(annotation, 'file_citation', None)):
                    cited_file = client.files.retrieve(file_citation.file_id)
                    citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
                    print(cited_file)
                elif (file_path := getattr(annotation, 'file_path', None)):
                    cited_file = client.files.retrieve(file_path.file_id)
                    citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
                    print(cited_file)
                    # Note: File download functionality not implemented above for brevity
            thread_message_content_replace += "\n\nCitations:\n" + "\n".join(citations)
            print(thread_message_content_replace)

# 18. Add Message to St.SessionState Messages
            response_message = {"role": thread_message_role, "content": thread_message_content_replace, "messageid": thread_message_id, "runid": thread_message_run_id, "createdatunix": thread_message_unix, "createdatdatetime": thread_message_datetime}
            st.session_state.messages.append(response_message)
            append_to_log.append_message_to_log(response_message)
            append_to_dataframe_messages.append_message_to_message_dataframe(response_message)

#19. Display Assistant Response
            with chat_container:
                with st.chat_message(thread_message_role):
                    st.markdown(thread_message_content_replace)
