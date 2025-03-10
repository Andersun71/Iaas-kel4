import streamlit as st

def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.channel.recv_exit_status(), stdout.read().decode().strip(), stderr.read().decode().strip()

def change_ssid(client, new_ssid):
    command = f"/interface wireless set wlan1 ssid={new_ssid}"
    _, _, error = execute_command(client, command)
    if error:
        st.error(f"❌ Failed to change SSID: {error}")
    else:
        st.success(f"✅ SSID changed to {new_ssid}")

def change_password(client, new_password):
    command = f"/interface wireless security-profiles set [find default=yes] mode=dynamic-keys authentication-types=wpa2-psk wpa2-pre-shared-key={new_password}"
    _, _, error = execute_command(client, command)
    if error:
        st.error(f"❌ Failed to change WiFi password: {error}")
    else:
        st.success("✅ WiFi password changed successfully!")

def restart_wireless(client):
    disable_cmd = "/interface wireless disable wlan1"
    enable_cmd = "/interface wireless enable wlan1"
    execute_command(client, disable_cmd)
    execute_command(client, enable_cmd)
    st.success("🔄 Wireless restarted to apply changes.")

def run():
    st.header("🔧 Change WiFi SSID & Password")
    
    client = st.session_state.get("ssh_client")
    if not client:
        st.warning("❌ No connection detected. Please log in first.")
        return
    
    new_ssid = st.text_input("Enter New SSID:", placeholder="New WiFi Name")
    new_password = st.text_input("Enter New WiFi Password:", placeholder="New Password", type="password")
    
    if st.button("Apply Changes"):
        if new_ssid:
            change_ssid(client, new_ssid)
        if new_password:
            change_password(client, new_password)
        restart_wireless(client)
        st.success("✅ Changes applied successfully!")

if __name__ == "__main__":
    run()
