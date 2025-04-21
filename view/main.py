import streamlit as st
import importlib

# Initialize session state
if "currentPage" not in st.session_state:
    st.session_state["currentPage"] = "Login"

if "connection_status" not in st.session_state:
    st.session_state["connection_status"] = "⚪ Not Connected"

# Function to switch pages
def change_page(page_name):
    st.session_state["currentPage"] = page_name

# Sidebar Navigation
st.sidebar.title("📌 Menu")

st.sidebar.markdown(f"**{st.session_state['connection_status']}**")

with st.sidebar.expander("🔒 Login", expanded=True):
    if st.button("Connect"):
        change_page("Login")

with st.sidebar.expander("⚙️ Basic Configuration"):
    if st.button("IP Configuration"):
        change_page("IP Configuration")
    if st.button("SSID & Password"):
        change_page("SSID & Password")
    if st.button("Firewall Filtering"):
        change_page("Firewall Filtering")
    if st.button("Bandwidth Fix"):
        change_page("Bandwidth Fix")
    if st.button("DNS Configuration"):
        change_page("DNS Configuration")
    # if st.button("Disable/Enable Interfaces"):
    #     change_page("Disable/Enable Interfaces")
    
with st.sidebar.expander("🗂️ Backup Configuration"):
    if st.button("Backup Configuration"):
        change_page("Backup Configuration")

with st.sidebar.expander("🚪 Logout"):
    if st.button("Disconnect"):
        st.session_state["connection_status"] = "⚪ Not Connected"
        change_page("Logout")

# Page Routing
PAGES = {
    "Login": "login",
    "SSID & Password": "ssid_password",
    "Firewall Filtering": "firewall_filtering",
    "Bandwidth Fix": "fix_bandwidth",
    # "Disable/Enable Interfaces": "disable_enable",
    "Backup Configuration": "backup_configuration",
    "Logout": "logout",
    "Welcome": "welcome",
    "IP Configuration": "ip_configuration",
    "DNS Configuration":"dns"
}

# Load the selected page dynamically
page_name = st.session_state["currentPage"]

if page_name in PAGES:
    st.header(f"NetEZ - {page_name}")
    try:
        module = importlib.import_module(PAGES[page_name])
        module.run()
    except ModuleNotFoundError:
        st.error(f"⚠️ Halaman **{page_name}** tidak ditemukan!")
else:
    st.header("You are at the **Main Page**")
    st.write("Klik tombol di sidebar untuk berpindah ke halaman lain.")