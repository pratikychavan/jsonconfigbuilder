import streamlit as st
import json
import os

st.set_page_config(page_title="JSON Config Builder", layout="wide")

if "config" not in st.session_state:
    st.session_state.config = {}

def add_entry(path, key, value):
    current = st.session_state.config
    for p in path:
        current = current.setdefault(p, {})
    current[key] = value

def remove_entry(path, key):
    if not path:  
        st.session_state.config.pop(key, None)
        return

    current = st.session_state.config
    for p in path[:-1]:
        current = current.get(p, {})
    if isinstance(current, dict):
        current.pop(key, None)

st.sidebar.header("Configuration Options")

st.sidebar.subheader("Add Entry")
path_input = st.sidebar.text_input("Path (dot-separated, e.g., parent.child)")
key = st.sidebar.text_input("Key")
value = st.sidebar.text_input("Value")

path = path_input.split(".") if path_input else []

if st.sidebar.button("Add/Update"):
    if key and value:
        add_entry(path, key, value)
        st.sidebar.success(f"Added/Updated: {'.'.join(path + [key])}")
    else:
        st.sidebar.error("Path, Key, and Value cannot be empty")

st.sidebar.subheader("Remove Entry")
remove_path_input = st.sidebar.text_input("Path to Key (dot-separated)")

if st.sidebar.button("Remove"):
    remove_path = remove_path_input.split(".") if remove_path_input else []
    if remove_path:
        *parent_path, key_to_remove = remove_path
        remove_entry(parent_path, key_to_remove)
        st.sidebar.success(f"Removed: {remove_path_input}")
    else:
        st.sidebar.error("Path cannot be empty")

st.sidebar.subheader("Upload JSON Config")
uploaded_file = st.sidebar.file_uploader("Choose a JSON file", type="json")

if uploaded_file:
    try:
        uploaded_config = json.load(uploaded_file)
        st.session_state.config.update(uploaded_config)
        st.sidebar.success("Configuration file uploaded successfully.")
    except Exception as e:
        st.sidebar.error(f"Error loading JSON: {e}")

st.title("JSON Config Builder")

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("Current JSON Configuration")
with col2:
    if st.session_state.config:
        json_data = json.dumps(st.session_state.config, indent=4)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="config.json",
            mime="application/json",
        )
    else:
        st.info("No configuration to download.")

st.json(st.session_state.config)
