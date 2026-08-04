import streamlit as st
import pandas as pd
import src.backend.database as db
from src.backend.Extension import Extension

extensions: dict[int, Extension] = st.session_state.extensions

@st.cache_data
def organize_extensions_by_student() -> dict[str, list[int]]:
    exts_by_student: dict[str, list[int]] = {}

    for id, ext in extensions.items():
        if not exts_by_student.get(ext.email):
            exts_by_student[ext.email] = []
        exts_by_student[ext.email].append(id)

    return exts_by_student

def update_extensions():
    changes = st.session_state["editor"]["edited_rows"]
    
    # Extract new boolean values
    toggled = {row: cols["Approved?"] for row, cols in changes.items() if "Approved?" in cols}

    # Update Extensions
    database = db.DatabaseConnection(st.secrets.instructor_id)
    for row, new_val in toggled.items():
        extension = next((extension for extension in extensions.values() if extension.id == row), None)
        if extension:
            extension.approved = new_val
            database.update_approval(extension, extension.approved)
    database.close()

def table():        
    st.header("Extension Table")

    data = {
        "Approved?": [ext.approved for ext in extensions.values()],
        "Email": [ext.email for ext in extensions.values()],
        "Assignment": [ext.assignment for ext in extensions.values()],
        "Submitted On": [ext.date_submitted for ext in extensions.values()],
        "New Deadline": [ext.deadline for ext in extensions.values()],
        "Reason": [ext.reason for ext in extensions.values()],
        }

    data = pd.DataFrame(data, index=list(extensions.keys()))

    disabled_cols = ["_index", "Email", "Assignment", "Submitted On", "New Deadline", "Reason"]

    column_config = {
        "Approved?": st.column_config.CheckboxColumn("Approved?",pinned=True)
    }

    st.data_editor(data, key="editor", width='stretch', disabled=disabled_cols, column_config=column_config)
    st.button('Save Changes', on_click=update_extensions)

def history():
    exts_by_student = organize_extensions_by_student()

    students = exts_by_student.keys()
    option = st.selectbox('Student Email', students)

    ids = exts_by_student[option]

    data = {
        "Approved?": [extensions[id].approved for id in ids],
        "Assignment": [extensions[id].assignment for id in ids],
        "Submitted On": [extensions[id].date_submitted for id in ids],
        "New Deadline": [extensions[id].deadline for id in ids],
        "Reason": [extensions[id].reason for id in ids],
    }

    data = pd.DataFrame(data, index=ids)
    
    disabled_cols = ["_index", "Approved?", "Assignment", "Submitted On", "New Deadline", "Reason"]

    column_config = {
        "Approved?": st.column_config.CheckboxColumn("Approved?",pinned=True)
    }

    st.data_editor(data, key="history", width='stretch', disabled=disabled_cols, column_config=column_config)

    
table()
history()
