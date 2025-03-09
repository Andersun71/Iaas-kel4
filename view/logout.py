import streamlit as st

def run():
    st.header("Logout")

    # Check if an SSH connection exists
    if "ssh_client" in st.session_state and st.session_state["ssh_client"]:
        try:
            # Close the SSH connection
            st.session_state["ssh_client"].close()
            st.session_state["ssh_client"] = None  # Reset SSH client
            st.session_state["connection_status"] = "⚪ Not Connected"
            st.success("Disconnected from MikroTik successfully.")
        except Exception as e:
            st.error(f"Failed to disconnect: {e}")
    else:
        st.warning("No active connection found.")

    # Redirect to login page
    st.session_state["currentPage"] = "Login"
    st.rerun()