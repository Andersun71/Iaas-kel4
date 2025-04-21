import streamlit as st
import re

def run():
    """Firewall Filtering Page - Block websites using MikroTik firewall rules"""
    st.subheader("🚫 Firewall Filtering")
    st.write("Block access to specific websites.")

    # Ensure SSH connection exists
    if "ssh_client" not in st.session_state or st.session_state["ssh_client"] is None:
        st.error("⚠️ Not connected to MikroTik. Please log in first.")
        return

    # User input: Websites to block
    common_sites = ["facebook.com", "youtube.com", "tiktok.com", "twitter.com", "instagram.com", "netflix.com", "reddit.com"]
    blocked_website = st.selectbox("Choose a common website to block or type your own", options=[""] + common_sites)
    custom_website = st.text_input("Or enter a custom website to block", placeholder="example.com (without http/https)")
    final_website = custom_website.strip() if custom_website.strip() else blocked_website.strip()

    col1, col2 = st.columns([1, 5])

    with col1:
        if st.button("Cancel"):
            st.warning("Input cancelled.")

    with col2:
        if st.button("Submit"):
            if not final_website:
                st.warning("⚠️ Please enter at least one website.")
                return

            if final_website and not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', final_website):
                st.warning("⚠️ Invalid domain format. Please enter a valid domain like 'example.com'.")
                return

            ssh_client = st.session_state["ssh_client"]
            try:
                # Generate MikroTik commands for Layer 7 filtering
                layer7_command = f'/ip firewall layer7-protocol add name=BlockWebsites regexp="{final_website}"'
                filter_command = '/ip firewall filter add chain=forward layer7-protocol=BlockWebsites action=drop'

                # Execute commands via SSH
                ssh_client.exec_command(layer7_command)
                ssh_client.exec_command(filter_command)

                st.success(f"✅ Website blocked successfully: {final_website}")

            except Exception as e:
                st.error(f"⚠️ Error executing command: {str(e)}")
    
    st.markdown("---")
    st.subheader("🗑️ Unblock Website")
    # Display currently blocked websites
    # st.markdown("### 🔒 Currently Blocked Websites")
    # try:
    #     ssh_client = st.session_state["ssh_client"]
    #     stdin, stdout, stderr = ssh_client.exec_command('/ip firewall layer7-protocol print without-paging')
    #     output = stdout.read().decode('utf-8')
    #     blocked_entries = []
    #     for line in output.splitlines():
    #         if "BlockWebsites" in line:
    #             parts = line.split("regexp=\"")
    #             if len(parts) > 1:
    #                 domain = parts[1].rstrip("\"")
    #                 blocked_entries.append(domain)
    #     if blocked_entries:
    #         st.write("Websites currently blocked:")
    #         for site in blocked_entries:
    #             col1, col2 = st.columns([4, 1])
    #             with col1:
    #                 st.markdown(f"- `{site}`")
    #             with col2:
    #                 if st.button(f"Unblock {site}", key=f"unblock_{site}"):
    #                     try:
    #                         ssh_client = st.session_state["ssh_client"]
    #                         remove_layer7 = f'/ip firewall layer7-protocol remove [find name=BlockWebsites and regexp="{site}"]'
    #                         remove_filter = f'/ip firewall filter remove [find chain=forward layer7-protocol=BlockWebsites]'
    #                         ssh_client.exec_command(remove_filter)
    #                         ssh_client.exec_command(remove_layer7)
    #                         st.success(f"✅ Unblocked website: {site}")
    #                     except Exception as e:
    #                         st.error(f"⚠️ Error removing block: {str(e)}")
    #     else:
    #         st.info("No websites are currently blocked.")
    # except Exception as e:
    #     st.error(f"⚠️ Failed to retrieve blocked websites: {str(e)}")

    unblock_website = st.text_input("Enter website to unblock", placeholder="example.com")
    if st.button("Unblock"):
        if not unblock_website.strip():
            st.warning("⚠️ Please enter a website to unblock.")
        elif not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', unblock_website.strip()):
            st.warning("⚠️ Invalid domain format.")
        else:
            try:
                ssh_client = st.session_state["ssh_client"]
                # Remove matching layer7 and firewall rules (assuming same name pattern)
                remove_layer7 = f'/ip firewall layer7-protocol remove [find name=BlockWebsites and regexp="{unblock_website.strip()}"]'
                remove_filter = f'/ip firewall filter remove [find chain=forward layer7-protocol=BlockWebsites]'
                ssh_client.exec_command(remove_filter)
                ssh_client.exec_command(remove_layer7)
                st.success(f"✅ Unblocked website: {unblock_website.strip()}")
            except Exception as e:
                st.error(f"⚠️ Error removing block: {str(e)}")