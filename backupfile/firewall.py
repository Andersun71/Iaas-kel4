import streamlit as st

def run():
    """Firewall Filtering Page - Block websites using MikroTik firewall rules"""
    st.subheader("🚫 Firewall Filtering")
    st.write("Block access to specific websites.")

    # Ensure SSH connection exists
    if "ssh_client" not in st.session_state or st.session_state["ssh_client"] is None:
        st.error("⚠️ Not connected to MikroTik. Please log in first.")
        return

    # User input: Websites to block
    blocked_websites = st.text_area("Enter websites to block (separate with commas)", placeholder="example.com, anotherwebsite.com")

    col1, col2 = st.columns([1, 5])

    with col1:
        if st.button("Cancel"):
            st.warning("Input cancelled.")

    with col2:
        if st.button("Submit"):
            if not blocked_websites.strip():
                st.warning("⚠️ Please enter at least one website.")
                return

            website_list = [site.strip() for site in blocked_websites.split(",") if site.strip()]
            if not website_list:
                st.warning("⚠️ Invalid input.")
                return

            ssh_client = st.session_state["ssh_client"]
            try:
                # Generate MikroTik commands for Layer 7 filtering
                regex_pattern = "|".join(website_list)
                layer7_command = f'/ip firewall layer7-protocol add name=BlockWebsites regexp="{regex_pattern}"'
                filter_command = '/ip firewall filter add chain=forward layer7-protocol=BlockWebsites action=drop'

                # Execute commands via SSH
                ssh_client.exec_command(layer7_command)
                ssh_client.exec_command(filter_command)

                st.success(f"✅ Websites blocked successfully: {', '.join(website_list)}")

            except Exception as e:
                st.error(f"⚠️ Error executing command: {str(e)}")