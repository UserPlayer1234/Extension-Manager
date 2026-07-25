import streamlit as st
import pandas as pd

from Extension import Extension

extensions: dict[int, Extension] = st.session_state.extensions

def change_handler():
    changes = st.session_state["editor"]["edited_rows"]

    # Extract new boolean values
    toggled = {row: cols["Approved?"] for row, cols in changes.items() if "Approved?" in cols}

    # Update Extensions
    for row, new_val in toggled.items():
        extension = next((extension for extension in extensions.values() if extension.id == row), None)
        extension.approved = new_val
        
st.header("Extensions Table")

data = {
    "Email": [ext.email for ext in extensions.values()],
    "Assignment": [ext.assignment for ext in extensions.values()],
    "Submitted On": [ext.date_submitted for ext in extensions.values()],
    "New Deadline": [ext.deadline for ext in extensions.values()],
    "Reason": [ext.reason for ext in extensions.values()],
    "Approved?": [ext.approved for ext in extensions.values()],
}

data = pd.DataFrame(data, index=list(extensions.keys()))

disabled_cols = ["_index", "Email", "Assignment", "Submitted On", "New Deadline", "Reason"]

edited_data = st.data_editor(data, key="editor", width='stretch', disabled=disabled_cols, on_change=change_handler)