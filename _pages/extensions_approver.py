import streamlit as st
import src.backend.database as db
from src.backend.Extension import Extension

current_extension: Extension = st.session_state.current_extension
extension_placeholder: Extension = st.session_state.extension_placeholder
extensions_iter = st.session_state.extensions_iter

def approve_extension():
    current_extension.approved = True
    database = db.DatabaseConnection()
    database.update_approval(current_extension, current_extension.approved)
    database.close()
    st.session_state.current_extension = next(extensions_iter, extension_placeholder)

def deny_extension():
    current_extension.approved = False
    database = db.DatabaseConnection()
    database.update_approval(current_extension, current_extension.approved)
    database.close()
    st.session_state.current_extension = next(extensions_iter, extension_placeholder)

def approver():
    st.header("Extensions Approver")

    with st.container():
        st.metric('Email', current_extension.email)
        st.metric('Assignment', current_extension.assignment)
        st.metric('Submitted On', current_extension.date_submitted)
        st.metric('New Deadline', current_extension.deadline)
        st.metric('Reason', current_extension.reason)

    with st.container(horizontal=True):
        st.button('Approve', on_click=approve_extension)
        st.button('Deny', on_click=deny_extension)

approver()
