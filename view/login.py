import streamlit as st
import paramiko

def ssh_connect(ip_address, port, username, password):
    """Establish SSH connection to MikroTik."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip_address, port=int(port), username=username, password=password)
        return client
    except Exception as e:
        return str(e)

def run():
    """Login Page for MikroTik Connection"""
    st.subheader("🔒 Login to MikroTik")

    # Ensure session state variables exist
    if "ssh_client" not in st.session_state:
        st.session_state["ssh_client"] = None
    if "connection_status" not in st.session_state:
        st.session_state["connection_status"] = "🔴 Not connected"

    # Sidebar connection status display
    st.sidebar.info(st.session_state["connection_status"])

    # User input fields
    ip_address = st.text_input("IP Address")
    port = st.text_input("Port", value="22")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit", key="login_button"):
        if ip_address and port and username and password:
            st.write(f"Connecting to `{ip_address}` on port `{port}`...")
            connection = ssh_connect(ip_address, port, username, password)

            if isinstance(connection, paramiko.SSHClient):
                st.success("✅ Connected successfully!")
                st.session_state["ssh_client"] = connection  # Store connection in session
                st.session_state["connection_status"] = f"🟢 Connected to {ip_address} on port {port}"
                st.session_state["mikrotik_ip"] = ip_address
                st.session_state["mikrotik_port"] = port
                st.session_state["currentPage"] = "Welcome"  # Redirect to Welcome page
                st.rerun()  # Refresh UI
            else:
                st.session_state["connection_status"] = "🔴 Connection failed!"
                st.error(f"❌ Connection failed: {connection}")
        else:
            st.warning("⚠️ Please fill in all fields.")

if __name__ == "__main__":
    run()