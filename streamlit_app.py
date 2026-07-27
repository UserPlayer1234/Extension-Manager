import streamlit as st

import authorize
import google_forms
import format

from Extension import Extension

# Define login state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "creds" not in st.session_state:
        st.session_state.creds = None

def login():
    if st.button("Login with Google"):
        st.session_state.creds = authorize.obtain_creds()
        st.session_state.logged_in = True
        st.rerun()

login_pg = st.Page(login, title="Login Page")
table_pg = st.Page("extensions_table.py", title="Extensions Table")
approver_pg = st.Page("extensions_approver.py", title="Extensions Approver")

if st.session_state.logged_in:
    form = google_forms.Form(creds=st.session_state.creds)
    form.formId = st.secrets.form_id
    responses = form.retrieve_form()
    extensions = format.format_requests(responses=responses)

    # Defining extension state variables
    if "extension_placeholder" not in st.session_state:
        st.session_state.extension_placeholder = Extension()
    
    if "extensions" not in st.session_state:
        st.session_state.extensions = {extension.id: extension for extension in extensions}

    if "extensions_iter" not in st.session_state:
        st.session_state.extensions_iter = iter(st.session_state.extensions.values())

    if "current_extension" not in st.session_state:
        st.session_state.current_extension = next(st.session_state.extensions_iter, st.session_state.extension_placeholder)

    pg = st.navigation([table_pg, approver_pg])
else:
    pg = st.navigation([login_pg])

pg.run()