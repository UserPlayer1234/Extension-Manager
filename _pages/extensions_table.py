import streamlit as st
import pandas as pd
import src.backend.database as db
from src.backend.Extension import Extension

extensions: dict[int, Extension] = st.session_state.extensions

def retrieve_data() -> dict:
    data = {
        "Approved?": [ext.approved for ext in extensions.values()],
        "Email": [ext.email for ext in extensions.values()],
        "Assignment": [ext.assignment for ext in extensions.values()],
        "Submitted On": [ext.date_submitted for ext in extensions.values()],
        "New Deadline": [ext.deadline for ext in extensions.values()],
        "Reason": [ext.reason for ext in extensions.values()],
    }
    return data

def table():        
    st.header("Extensions Table")

    data = retrieve_data()

    data = pd.DataFrame(data, index=list(extensions.keys()))

    disabled_cols = ["_index", "Email", "Assignment", "Submitted On", "New Deadline", "Reason"]

    column_config = {
        "Approved?": st.column_config.CheckboxColumn("Approved?",pinned=True)
    }

    edited_data = st.data_editor(data, key="editor", width='stretch', disabled=disabled_cols, column_config=column_config)

def update_extensions():
    changes = st.session_state["editor"]["edited_rows"]
    
    # Extract new boolean values
    toggled = {row: cols["Approved?"] for row, cols in changes.items() if "Approved?" in cols}

    # Update Extensions
    database = db.DatabaseConnection()
    for row, new_val in toggled.items():
        extension = next((extension for extension in extensions.values() if extension.id == row), None)
        if extension:
            extension.approved = new_val
            database.update_approval(extension, extension.approved)
    database.close()

def update_button():
    update = st.button('Save Changes', on_click=update_extensions)

table()
update_button()