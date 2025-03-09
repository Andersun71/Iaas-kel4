import streamlit as st
import paramiko
import time
import os

def list_backup_files(client):
    """Retrieve a list of backup files from MikroTik via SFTP."""
    try:
        with client.open_sftp() as sftp:
            files = sftp.listdir("/")
            backup_files = [file for file in files if file.endswith('.backup')]
            return backup_files
    except Exception as e:
        st.error(f"Failed to get the list of backup files: {e}")
        return []

def create_backup(ssh_client, backup_name):
    """Create a new backup file on MikroTik."""
    try:
        command = f'/system backup save name={backup_name}'
        ssh_client.exec_command(command)
        time.sleep(2)  # Wait for backup to be created
        st.success(f"✅ Backup `{backup_name}.backup` created successfully!")
    except Exception as e:
        st.error(f"❌ Failed to create backup: {e}")

def download_backup(ssh_client, backup_name):
    """Download a backup file from MikroTik to the client device."""
    try:
        with ssh_client.open_sftp() as sftp:
            local_path = f"./{backup_name}"
            remote_path = f"/{backup_name}"
            sftp.get(remote_path, local_path)

        with open(local_path, "rb") as file:
            file_bytes = file.read()

        # Provide a download button
        st.download_button(
            label="⬇️ Download Backup File",
            data=file_bytes,
            file_name=backup_name,
            mime="application/octet-stream"
        )

        os.remove(local_path)  # Cleanup temporary file after download
        st.success(f"✅ Backup `{backup_name}` is ready to download!")
    except Exception as e:
        st.error(f"❌ Failed to download backup: {e}")

def run():
    """Backup Configuration Page"""
    st.subheader("📂 MikroTik Backup Configuration")

    # Ensure an active connection
    if "ssh_client" not in st.session_state or st.session_state["ssh_client"] is None:
        st.error("⚠️ No active MikroTik connection. Please log in first.")
        return

    ssh_client = st.session_state["ssh_client"]

    # Display backup files
    st.write("### 🔍 Available Backup Files")
    backup_files = list_backup_files(ssh_client)

    if backup_files:
        selected_file = st.selectbox("Select a backup file to download:", backup_files)

        if st.button("⬇️ Fetch Backup for Download"):
            download_backup(ssh_client, selected_file)
    else:
        st.warning("No backup files found.")

    # Create new backup
    st.write("### ✨ Create New Backup")
    backup_name = st.text_input("Enter backup name (without .backup extension):")

    if st.button("🛠️ Create Backup"):
        if backup_name:
            create_backup(ssh_client, backup_name)
            st.rerun()  # Refresh the file list
        else:
            st.warning("⚠️ Please enter a backup name.")

if __name__ == "__main__":
    run()