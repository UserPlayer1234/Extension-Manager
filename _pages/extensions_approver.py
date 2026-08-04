import streamlit as st
import src.backend.database as db
from src.backend.Extension import Extension

current_extension: Extension = st.session_state.current_extension
extension_placeholder: Extension = st.session_state.extension_placeholder
extensions_iter = st.session_state.extensions_iter

def update_extension(approval: bool):
    current_extension.approved = approval
    current_extension.note = st.session_state.notes
    database = db.DatabaseConnection(st.secrets.instructor_id)
    database.update_approval(current_extension, current_extension.approved, current_extension.note)
    database.close()

    st.session_state.current_extension = next(extensions_iter, extension_placeholder)

def approver():
    st.header("Extension Approver")
    
    with st.container():
        with st.container(horizontal=True):
            st.text_area('Email', current_extension.email, height="content", disabled=True)
            st.text_area('Assignment', current_extension.assignment, height="content", disabled=True)
        with st.container(horizontal=True):
            st.text_area('Submitted On', current_extension.date_submitted, height="content", disabled=True)
            st.text_area('New Deadline', current_extension.deadline, height="content", disabled=True)
        st.text_area('Reason', current_extension.reason, height="content", disabled=True)
        st.text_input('Instructor Notes', key='notes')

    with st.container(horizontal=True):
        st.button('Approve', on_click=update_extension, args=[True])
        st.button('Deny', on_click=update_extension, args=[False])

approver()
