import streamlit as st

import src.backend.authorize as authorize
import src.backend.google_forms as google_forms
import src.backend.format as format
import src.backend.database as db

from src.backend.Extension import Extension

# Define login state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "creds" not in st.session_state:
        st.session_state.creds = None

def login():
    if st.button("Login with Google"):
        creds = authorize.obtain_creds()
        st.session_state.creds = creds
        st.session_state.logged_in = True

        # Retrieve extension requests
        form = google_forms.Form(creds=creds)
        form.formId = st.secrets.form_id
        responses = form.retrieve_form()
        extensions = format.format_requests(responses=responses)

        # Connect to database and store/update extensions
        database = db.DatabaseConnection()
        extensions_dict = {extension.id: extension for extension in extensions}
        for extension in extensions:
            database.insert_ext(extension)
        for id, approval in database.get_all_exts():
            extensions_dict[id].approved = approval
        database.close()

        # Defining extension state variables
        if "extension_placeholder" not in st.session_state:
            st.session_state.extension_placeholder = Extension()
        
        if "extensions" not in st.session_state:
            st.session_state.extensions = extensions_dict

        if "extensions_iter" not in st.session_state:
            st.session_state.extensions_iter = iter(st.session_state.extensions.values())

        if "current_extension" not in st.session_state:
            st.session_state.current_extension = next(st.session_state.extensions_iter, st.session_state.extension_placeholder)

        st.rerun()

# Define pages
login_pg = st.Page(login, title="Login Page")
form_pg = st.Page("_pages/extensions_form.py", title="Extension Form")
table_pg = st.Page("_pages/extensions_table.py", title="Extension Table")
approver_pg = st.Page("_pages/extensions_approver.py", title="Extension Approver")

# Display pages based on logged in state
if st.session_state.logged_in:
    pg = st.navigation([form_pg, table_pg, approver_pg])
else:
    pg = st.navigation([login_pg])

pg.run()