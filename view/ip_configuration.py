import streamlit as st
import paramiko
import time
import pandas as pd
import re

def get_interfaces(ssh_client):
    """Retrieve a list of interfaces from MikroTik."""
    try:
        stdin, stdout, stderr = ssh_client.exec_command("/interface print without-paging")
        output = stdout.read().decode()

        interfaces = []
        for line in output.split("\n"):
            match = re.match(r"^\s*(\d+)\s+([\w-]+)", line)  # Extracts ID and Name
            if match:
                interfaces.append({"ID": match.group(1), "Name": match.group(2)})
        
        return interfaces
    except Exception as e:
        st.error(f"Failed to retrieve interfaces: {e}")
        return []

def get_ip_addresses(ssh_client):
    """Retrieve a list of IP addresses assigned to interfaces."""
    try:
        stdin, stdout, stderr = ssh_client.exec_command("/ip address print without-paging")
        output = stdout.read().decode()

        ip_list = []
        for line in output.split("\n"):
            match = re.match(r"^\s*(\d+)\s+([\d./]+)\s+\S+\s+(\S+)", line)  # Extracts ID, IP, and Interface
            if match:
                ip_list.append({
                    "ID": match.group(1),
                    "Address": match.group(2),
                    "Interface": match.group(3),
                })
        
        return ip_list
    except Exception as e:
        st.error(f"Failed to retrieve IP addresses: {e}")
        return []

def add_ip(ssh_client, ip_address, interface):
    """Assign a new IP address to an interface."""
    try:
        command = f"/ip address add address={ip_address} interface={interface}"
        ssh_client.exec_command(command)
        time.sleep(2)
        st.success(f"✅ IP {ip_address} added to {interface} successfully!")
    except Exception as e:
        st.error(f"❌ Failed to add IP: {e}")

def edit_ip(ssh_client, ip_id, new_ip):
    """Edit an existing IP address."""
    try:
        command = f"/ip address set {ip_id} address={new_ip}"
        ssh_client.exec_command(command)
        time.sleep(2)
        st.success(f"✅ IP modified to {new_ip} successfully!")
    except Exception as e:
        st.error(f"❌ Failed to edit IP: {e}")

def delete_ip(ssh_client, ip_id):
    """Remove an IP address from an interface."""
    try:
        command = f"/ip address remove {ip_id}"
        ssh_client.exec_command(command)
        time.sleep(2)
        st.success(f"✅ IP removed successfully!")
    except Exception as e:
        st.error(f"❌ Failed to delete IP: {e}")

def run():
    """IP Configuration Page"""
    st.subheader("🌐 MikroTik IP Configuration")

    # Ensure active connection
    if "ssh_client" not in st.session_state or st.session_state["ssh_client"] is None:
        st.error("⚠️ No active MikroTik connection. Please log in first.")
        return

    ssh_client = st.session_state["ssh_client"]

    # Show list of interfaces as table
    st.write("### 🔗 Available Interfaces")
    interfaces = get_interfaces(ssh_client)
    if interfaces:
        df_interfaces = pd.DataFrame(interfaces)
        st.table(df_interfaces)
    else:
        st.warning("No interfaces found.")

    # Show list of IP addresses as table
    st.write("### 📋 Assigned IP Addresses")
    ip_addresses = get_ip_addresses(ssh_client)
    if ip_addresses:
        df_ips = pd.DataFrame(ip_addresses)
        st.table(df_ips)
    else:
        st.warning("No IP addresses found.")

    # Add new IP address section
    st.write("### ➕ Add New IP Address")
    with st.expander("Add New IP"):
        new_ip = st.text_input("Enter IP Address (e.g., 192.168.1.10/24):")
        selected_interface = st.selectbox("Select Interface:", [i["Name"] for i in interfaces])

        if st.button("✅ Add IP"):
            if new_ip and selected_interface:
                add_ip(ssh_client, new_ip, selected_interface)
                st.experimental_rerun()
            else:
                st.warning("⚠️ Please fill in all fields.")

    # Edit existing IP section
    st.write("### ✏️ Edit Existing IP")
    if ip_addresses:
        with st.expander("Edit IP Address"):
            selected_ip = st.selectbox("Select IP to Edit:", ip_addresses, format_func=lambda ip: f"{ip['Address']} on {ip['Interface']}")
            new_ip_value = st.text_input("Enter new IP Address:")

            if st.button("✏️ Update IP"):
                if new_ip_value:
                    edit_ip(ssh_client, selected_ip['ID'], new_ip_value)
                    st.experimental_rerun()
                else:
                    st.warning("⚠️ Please enter a new IP address.")

    # Delete IP section
    st.write("### ❌ Delete IP Address")
    if ip_addresses:
        with st.expander("Delete IP Address"):
            selected_ip_to_delete = st.selectbox("Select IP to Delete:", ip_addresses, format_func=lambda ip: f"{ip['Address']} on {ip['Interface']}")

            if st.button("❌ Remove IP"):
                delete_ip(ssh_client, selected_ip_to_delete['ID'])
                st.experimental_rerun()

if __name__ == "__main__":
    run()