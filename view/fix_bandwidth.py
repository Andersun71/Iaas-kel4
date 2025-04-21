import streamlit as st
import socket

def get_local_ip():
    """Retrieve the local machine's IP address."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        return f"Error: {e}"

def get_assigned_bandwidths():
    """Fetch IPs with bandwidth limits from MikroTik."""
    if "ssh_client" not in st.session_state or st.session_state["ssh_client"] is None:
        return []
    
    try:
        ssh_client = st.session_state["ssh_client"]
        stdin, stdout, stderr = ssh_client.exec_command("/queue simple print terse")
        output = stdout.read().decode()
        
        assigned_ips = []
        ip_name_map = {}
        
        for line in output.split("\n"):
            if "target=" in line and "max-limit=" in line:
                parts = line.split()
                ip = next((p.split("=")[1] for p in parts if p.startswith("target=")), None)
                name = next((p.split("=")[1] for p in parts if p.startswith("name=")), None)
                limit = next((p.split("=")[1] for p in parts if p.startswith("max-limit=")), None)
                
                if ip and name and limit:
                    assigned_ips.append(f"{ip} (Limit: {limit})")
                    ip_name_map[ip] = name
        
        return assigned_ips, ip_name_map
    
    except Exception as e:
        st.error(f"⚠️ Error fetching assigned bandwidths: {str(e)}")
        return [], {}

def delete_bandwidth_limit(target_ip, ip_name_map):
    """Delete bandwidth limit for a given IP address in MikroTik."""
    if "ssh_client" not in st.session_state or st.session_state["ssh_client"] is None:
        st.error("⚠️ Not connected to MikroTik. Please log in first.")
        return

    if target_ip not in ip_name_map:
        st.warning("⚠️ Selected IP not found in queue.")
        return

    queue_name = ip_name_map[target_ip]
    command = f"/queue simple remove [find name={queue_name}]"

    try:
        ssh_client = st.session_state["ssh_client"]
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            st.error(f"❌ Failed to delete limit: {error}")
        else:
            st.success(f"✅ Bandwidth limit removed for {target_ip}")

    except Exception as e:
        st.error(f"⚠️ Error executing command: {str(e)}")

def run():
    """Bandwidth Fix Page - Set or Remove bandwidth limits on MikroTik"""
    st.subheader("🚀 Bandwidth Management")
    st.write("Manage bandwidth limits for a specific IP address.")

    # Display local IP
    # local_ip = get_local_ip()
    # st.info(f"📌 **Local IP:** {local_ip}")

    # Fetch assigned IPs with bandwidth limits
    assigned_ips, ip_name_map = get_assigned_bandwidths()

    # Check SSH connection
    if "ssh_client" not in st.session_state or st.session_state["ssh_client"] is None:
        st.error("⚠️ Not connected to MikroTik. Please log in first.")
        return

    # Allow user to select an existing IP or enter a new one
    st.subheader("🛠 Set Bandwidth Limit")
    target_ip = st.selectbox("Select Target IP", options=["Enter New IP"] + assigned_ips)
    
    if target_ip == "Enter New IP":
        target_ip = st.text_input("New Target IP Address")

    upload_speed = st.number_input("Upload Speed (Mbps)", min_value=0.0)
    download_speed = st.number_input("Download Speed (Mbps)", min_value=0.0)

    col1, col2, col3 = st.columns([1, 2, 5])

    with col1:
        if st.button("Cancel"):
            st.warning("Input cancelled.")
    
    with col2:
        if st.button("Delete"):
            ip = target_ip.split(" ")[0]  # Extract only the IP from the display text
            delete_bandwidth_limit(ip, ip_name_map)
            st.rerun()
            
    with col3:
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
                    st.rerun()

            except Exception as e:
                st.error(f"⚠️ Error executing command: {str(e)}")

    # Delete Bandwidth Limit Section
    # st.subheader("🗑 Remove Bandwidth Limit")
    # if assigned_ips:
    #     delete_ip = st.selectbox("Select IP to Remove", options=assigned_ips)
    #     if st.button("Delete"):
    #         ip = delete_ip.split(" ")[0]  # Extract only the IP from the display text
    #         delete_bandwidth_limit(ip, ip_name_map)
    #         st.rerun()
    # else:
    #     st.info("No assigned bandwidth limits found.")