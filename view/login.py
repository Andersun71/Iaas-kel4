import streamlit as st
import paramiko
from getpass import getpass

def ssh_connect(ip_address, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip_address, port=int(port), username=username, password=password)
        return client
    except Exception as e:
        return str(e)

def run():
    st.subheader("Login to MikroTik")
    ip_address = st.text_input("IP Address")
    port = st.text_input("Port", value="22")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Submit"):
        if ip_address and port and username and password:
            st.write(f"Connecting to {ip_address} on port {port}...")
            connection = ssh_connect(ip_address, port, username, password)
            if isinstance(connection, paramiko.SSHClient):
                st.success("Connected successfully!")
            else:
                st.error(f"Connection failed: {connection}")
        else:
            st.warning("Please fill in all fields.")

if __name__ == "__main__":
    run()
