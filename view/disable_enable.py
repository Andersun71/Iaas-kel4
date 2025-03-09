import streamlit as st
from login import ssh_connect

def get_interfaces(ssh_client):
    """Mengambil daftar interface dan statusnya dari Mikrotik."""

    try:
        command = "/interface print terse"
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            st.error(f"Error mengambil interface: {error}")
            return []
        
        interfaces = []
        for line in output.split("\n"):
            if line.strip():
                parts = line.split()
                name = parts[0]
                status = "enabled" if "X" not in line else "disabled"
                interfaces.append((name, status))
        
        return interfaces
    
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        return []

def change_interfaces_status(ssh_client, interface, action):
    """Mengaktifkan atau menonaktifkan interface."""
    try:
        command = f"/interface set {interface} disabled={'yes' if action == 'Disable' else 'no'}"
        stdin, stdout, stderr = ssh_client.exec_command(command)
        error = stderr.read().decode()

        if error:
            st.error(f"Error mengubah status interface: {error}")
        else:
            st.success(f"Interface {interface} berhasil di{action.lower()}d!")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

def run():
    st.subheader("Disable/Enable Interfaces")
    st.write("Manage nterfaces")

    ssh_client = ssh_connect()
    if ssh_client:
        interfaces = get_interfaces(ssh_client)

        if interfaces:
            interface_names = [iface[0] for iface in interfaces]
            selected_interface = st.selectbox("Select Interface", interface_names)

        #cek status interface yang dipilih
        status = next(status for name, status in interfaces if name == selected_interface)
        action_options = ["Disable"] if status == "enabled" else ["Enabled"]
        selected_action = st.selectbox("Action", action_options)
        
        col1, col2= st.columns([1, 5])

        with col1:
            if st.button("Cancel"):
                st.success("Input dibatalkan.")

        with col2:
            if st.button("submit"):
                change_interfaces_status(ssh_client, selected_interface, selected_action)
                st.success("Konfigurasi berhasil disimpan.")


