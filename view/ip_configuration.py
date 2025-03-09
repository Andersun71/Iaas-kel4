import streamlit as st
import time

def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.channel.recv_exit_status(), stdout.read().decode().strip(), stderr.read().decode().strip()

def get_interface(client):
    _, output, _ = execute_command(client, "/interface print terse")
    
    interfaces = []
    for line in output.split("\n"):
        parts = line.split()
        if len(parts) >= 3:
            interfaces.append(parts[2].replace("name=", ""))
            
    return interfaces

def rerun_after(timer):
    time.sleep(timer)
    st.rerun()

def subnet_mask_to_cidr(subnet_mask):
    return sum(bin(int(x)).count('1') for x in subnet_mask.split('.'))

def delete_ip(client, index, address):
    _, _, error = execute_command(client, f"/ip address remove numbers={index}")
    if error:
        st.error(f"Failed to delete {address}: {error}")
    else:
        st.success(f"Deleted IP {address}")
        rerun_after(3)
        
def get_ip(output):    
    col_headers = st.columns([3,2,1.5,1,1])
    with col_headers[0]: st.markdown("**Address**")
    with col_headers[1]: st.markdown("**Network**")
    with col_headers[2]: st.markdown("**Interface**")
    with col_headers[3]: st.markdown("**Status**")
    with col_headers[4]: st.markdown("**Action**")
    
    for line in output.split("\n"):
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 4:
            index = parts[0].split('=')[-1]  
            address = parts[1].split('=')[-1]
            network = parts[2].split('=')[-1]
            interface = parts[3].split('=')[-1]
            
            status_code = parts[0][0]
            status_text = {
                "D": "Dynamic",
                "X": "Disabled",
                "I": "Invalid"
            }.get(status_code, "Active")
            
            cols = st.columns([3,2,1.5,1,1])
            with cols[0]: st.write(address)
            with cols[1]: st.write(network)
            with cols[2]: st.write(interface)
            with cols[3]: st.write(status_text)
            with cols[4]:
                if st.button("Delete", key=f"del_{index}", use_container_width=True):
                    delete_ip(client, index, address)

def show_ip(client):
    st.subheader("IP Addresses")
    _, output, _ = execute_command(client, "/ip address print terse")
    get_ip(output)
    
def enable_disable_interface_btn(client, selected_interface):
    col1, _, col2 = st.columns([1,2,1])
    with col1:
        if st.button("Turn On Connection", use_container_width=True):
            _, _, error = execute_command(client, f"/interface enable {selected_interface}")
            if error:
                st.error(f"Unable to enable {selected_interface}: {error}")
            else:
                st.success(f"Enabled {selected_interface}")
    with col2:
        if st.button("Turn Off Connection", use_container_width=True):
            _, _, error = execute_command(client, f"/interface disable {selected_interface}")
            if error:
                st.error(f"Unable to disable {selected_interface}: {error}")
            else:
                st.success(f"Disabled {selected_interface}")

def apply_conf(client, selected_interface, ip_address, subnet_mask, remove_old):
    try:
        cidr = subnet_mask_to_cidr(subnet_mask)
        ip_with_subnet = f"{ip_address}/{cidr}"
        
        if remove_old:
            execute_command(client, f"/ip address remove [find interface={selected_interface}]")
            st.warning(f"Removing old IPs on {selected_interface}...")
        
        _, _, error = execute_command(client, f"/ip address add address={ip_with_subnet} interface={selected_interface}")
        if error:
            st.error(f"Error: {error}")
        else:
            st.success(f"New IP {ip_with_subnet} applied to {selected_interface}")
            rerun_after(3)
        
    except Exception as e:
        st.error(f"Failed to Set IP: {e}")

def run():
    st.header("Network Settings")
    
    # Retrieve SSH client from session state
    client = st.session_state.get("ssh_client")
    
    if not client:
        st.warning("❌ No connection detected. Please log in first.")
        return

    tab1, tab2 = st.tabs(["Current Addresses", "Set New Address"])

    with tab1:
        show_ip(client)

    with tab2:
        interfaces = get_interface(client)
        if not interfaces:
            st.warning("Interfaces not found")
            return
            
        selected_interface = st.selectbox("Choose Connection Port:", interfaces, index=None)
        enable_disable_interface_btn(client, selected_interface)
        
        ip_address = st.text_input("IP Address:", placeholder="Enter the IP address", help="Example: 192.168.88.1")
        subnet_mask = st.text_input("Subnetmask:", placeholder="Enter a subnet mask", help="Example: 255.255.255.0")
        remove_old = st.checkbox("Replace existing address", True)
        
        if st.button("Save Settings"):
            apply_conf(client, selected_interface, ip_address, subnet_mask, remove_old)