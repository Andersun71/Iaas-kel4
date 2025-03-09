import streamlit as st

def run():
    """Bandwidth Fix Page - Set bandwidth limits on MikroTik"""
    st.subheader("🚀 Bandwidth Fix")
    st.write("Manage bandwidth limits for a specific IP address.")

    # Check if SSH client exists in session state
    if "ssh_client" not in st.session_state or st.session_state["ssh_client"] is None:
        st.error("⚠️ Not connected to MikroTik. Please log in first.")
        return

    # User inputs
    target_ip = st.text_input("Target IP Address")
    upload_speed = st.number_input("Upload Speed (Mbps)", min_value=0.0)
    download_speed = st.number_input("Download Speed (Mbps)", min_value=0.0)

    col1, col2 = st.columns([1, 5])

    with col1:
        if st.button("Cancel"):
            st.warning("Input cancelled.")

    with col2:
        if st.button("Submit"):
            if not target_ip or upload_speed <= 0 or download_speed <= 0:
                st.warning("⚠️ Please provide valid inputs.")
                return
            
            # Convert Mbps to Kbps (MikroTik uses Kbps)
            upload_speed_kbps = int(upload_speed * 1024)
            download_speed_kbps = int(download_speed * 1024)

            # MikroTik queue command
            command = f"/queue simple add name={target_ip} target={target_ip}/32 max-limit={upload_speed_kbps}/{download_speed_kbps}"

            try:
                ssh_client = st.session_state["ssh_client"]
                stdin, stdout, stderr = ssh_client.exec_command(command)
                output = stdout.read().decode()
                error = stderr.read().decode()

                if error:
                    st.error(f"❌ Failed to apply limit: {error}")
                else:
                    st.success(f"✅ Bandwidth limit applied:\n{command}")

            except Exception as e:
                st.error(f"⚠️ Error executing command: {str(e)}")