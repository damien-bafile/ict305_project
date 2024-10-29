import streamlit as st

# Constants
DEFAULT_ICON = "📈"

def create_page(page_path, title, icon=DEFAULT_ICON, default=False):
    return st.Page(
        page=page_path,
        title=title,
        icon=icon,
        default=default
    )