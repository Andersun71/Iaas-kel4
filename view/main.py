import streamlit as st
import importlib

# Initiation_session_state
if "currentPage" not in st.session_state:
    st.session_state["currentPage"] = "main"

#switch_page
def change_page(page_name):
    st.session_state["currentPage"] = page_name

#sidebar
st.sidebar.title("Menu")

with st.sidebar.expander("🔒 Login", expanded=True):
    if st.button("Connect"):
        change_page("Login")

with st.sidebar.expander("⚙️ Basic Configuration", expanded=False):
    if st.button("SSIS & Password"):
        change_page("SSIS & Password")

    if st.button("Firewall Filtering"):
        change_page("Firewall Filtering")

    if st.button("Bandwidth Fix"):
        change_page("Bandwidth Fix")

    if st.button("Disable/Enable Interfaces"):
        change_page("Disable/Enable Interfaces")

with st.sidebar.expander("🗂️ Backup Configuration", expanded=False):
    if st.button("Backup Configuration"):
        change_page("Backup Configuration")

with st.sidebar.expander("🚪Logout", expanded=False):
    if st.button("Disconnect"):
        change_page("Logout")

#import_page
if st.session_state["currentPage"] == "main":
    st.header("You are at the **Main Page**")
    st.write("Klik tombol di sidebar untuk berpindah ke halaman lain.")

elif st.session_state["currentPage"] == "Login":
    st.header("NetEzz")
    try:
        login_module = importlib.import_module("login")
        login_module.run()
    except ModuleNotFoundError:
        st.write("Halaman **Login** tidak ditemukan!")

elif st.session_state["currentPage"] == "SSIS & Password":
    st.header("NetEzz")
    try:
        ssid_password_module = importlib.import_module("ssid_password")  
        ssid_password_module.run()  
    except ModuleNotFoundError:
        st.write("Halaman **SSIS & Password** tidak ditemukan!")

elif st.session_state["currentPage"] == "Firewall Filtering":
    st.header("NetEzz")
    try:
        firewall_filtering_module = importlib.import_module("firewall_filtering")
        firewall_filtering_module.run()
    except ModuleNotFoundError:
        st.write("Halaman **Firewall Filtering** tidak ditemukan!")

elif st.session_state["currentPage"] == "Bandwidth Fix":
    st.header("NetEzz")
    try:
        fix_bandwidth_module = importlib.import_module("fix_bandwidth")
        fix_bandwidth_module.run()
    except ModuleNotFoundError:
        st.write("Halaman **Fix Bandwith** tidak ditemukan!")

elif st.session_state["currentPage"] == "Disable/Enable Interfaces":
    st.header("NetEzz")
    try:
        disable_enable_module = importlib.import_module("disable_enable")
        disable_enable_module.run()
    except ModuleNotFoundError:
        st.write("Halaman **Disable/Enable Interface** tidak ditemukan!")

elif st.session_state["currentPage"] == "Backup Configuration":
    st.header("NetEzz")
    try:
        backup_configuration_module = importlib.import_module("backup_configuration")
        backup_configuration_module.run()
    except ModuleNotFoundError:
        st.write("Halaman **Backup_Configuration** tidak ditemukan!")

elif st.session_state["currentPage"] == "Logout":
    st.header("NetEzz")
    try:
        logout_module = importlib.import_module("logout")
        logout_module.run()
    except ModuleNotFoundError:
        st.write("Halaman **Logout** tidak ditemukan!")
