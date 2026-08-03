import streamlit as st
import src.backend.database as db
from src.backend.google_forms import Form

def form():
    st.header("Extension Form")

    with st.form('google_form'):
        st.text_input('Document Title', key="doc_title")
        st.text_input('Form Title', key="form_title")
        st.text_input('Description', key="desc")
        st.multiselect('Assignments', key="assignments", options=[], placeholder='Add assignments', accept_new_options=True)
        st.form_submit_button('Create Google Form', on_click=create_form)

    st.text_area('Form ID', st.session_state.form_id, height="content", disabled=True)
    st.text_area('Form URL', st.session_state.form_url, height="content", disabled=True)

def create_form():
    form_data = {
        "title": st.session_state.form_title,
        "documentTitle": st.session_state.doc_title,
        "description": st.session_state.desc,
        "assignments": st.session_state.assignments,
        }
    
    form = Form(st.session_state.creds)
    form.create_form(form_data)
    st.session_state.form_id = form.form_id
    st.session_state.form_url = form.form_url

    database = db.DatabaseConnection(st.secrets.instructor_id)
    database.insert_instructor(form.form_id, form.form_url)
    database.close()

form()