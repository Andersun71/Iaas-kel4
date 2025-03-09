import streamlit as st
from login import ssh_connect

def get_wireless_interfaces(ssh_client):
    """Mengambil daftar interface wireless dari Mikrotik"""

    try:
        command = "/interface wireless print terse"
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            st.error(f"Error mengambil interface wireless: {error}")
            return []
        
        interfaces = []
        for line in output.split("\n"):
            if line.strip():
                parts = line.split()
                name = parts[0]
                interfaces.append(name)
        
        return interfaces
    
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

def change_ssid_password(ssh_client, interface, ssid, old_password, new_password):
    try:
        #ubah SSID
        command_ssid = f"/interface wireless set {interface} ssid={ssid}"
        stdin, stdout, stderr = ssh_client.exec_command(command_ssid)
        error_ssid = stderr.read().decode()

        if error_ssid:
            st.error(f"Error mengubah SSID: {error_ssid}")
            return
        
        #ubah password
        comamnd_password = f"/interface wireless security-profiles set default supplicant-identity={ssid} wpa2-pre-shared-key={new_password}"
        stdin, stdout, stderr = ssh_client.exec_command(comamnd_password)
        error_password = stderr.read().decode()

        if error_password:
            st.error(f"Error mengubah password: {error_password}")
        else:
            st.success("SSID dan Password berhasil diperbarui!")
        
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

def run():
     st.subheader("SSID & Password")
     st.write("Manage SSID and password")
     
     ssh_client = ssh_connect()
     if ssh_client:
         wireless_interfaces = get_wireless_interfaces(ssh_client)

         if not wireless_interfaces:
             st.error("Tidak ada interface wireless yang ditemukan")
             return

     selected_interface = st.selectbox("Pilih Interface Wireless", wireless_interfaces)

     ssid = st.text_input("SSID Baru")
     old_password = st.text_input("Password Lama", type="password")
     new_password = st.text_input("Password Baru", type="password")

     col1, col2= st.columns([1, 5])

     with col1:
        if st.button("Cancel"):
            st.success("Input dibatalkan.")

     with col2:
        if st.button("submit"):
            if ssid and old_password and new_password:
                change_ssid_password(ssh_client,selected_interface, ssid, old_password, new_password)
                ssh_client.close()
            else:
                st.warning("Harap isi semua kolom!")
     
