import streamlit as st
import pandas as pd
import json
from login import ssh_connect
from datetime import datetime

FIREWALL_FILE = "firewall_data.json"

def load_blocked_sites():
    """Load daftar situs yang sudah diblokir dari JSON."""
    try:
        with open(FIREWALL_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_blocked_site(domain, schedule, duration):
    """Simpan situs yang diblokir ke file JSON."""
    blocked_sites = load_blocked_sites()

    # Cek apakah domain sudah ada
    if any(site["Domain/Url"] == domain for site in blocked_sites):
        st.warning(f"Domain {domain} sudah diblokir sebelumnya!")
        return

    blocked_sites.append({
        "Domain/Url": domain,
        "Schedule": schedule,
        "Time duration": duration
    })
    with open(FIREWALL_FILE, "w") as f:
        json.dump(blocked_sites, f, indent=4)

def block_site(ssh_client, domain, schedule, duration):
    """Menjalankan perintah firewall Mikrotik untuk memblokir domain."""
    try:
        if not ssh_client:
            st.error("SSH Client tidak tersedia. Periksa koneksi ke router.")
            return

        # Gunakan Layer 7 Filtering untuk blokir domain
        block_command = f"""/ip firewall layer7-protocol add name={domain} regexp={domain}
        /ip firewall filter add chain=forward layer7-protocol={domain} action=drop comment='Blocked {domain}'"""
        
        stdin, stdout, stderr = ssh_client.exec_command(block_command)
        error_output = stderr.read().decode()

        if error_output:
            st.error(f"Terjadi kesalahan: {error_output}")
        else:
            save_blocked_site(domain, schedule, duration)
            st.success(f"Domain {domain} berhasil diblokir!")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

def run():
    st.subheader("Firewall Filtering")
    st.write("Manage firewalls to block websites")

    col1, col2, col3 = st.columns(3)

    with col1:
        domain = st.text_input("Domain/Url")

    with col2:
        schedule = st.date_input("Schedule")

    with col3:
        duration = st.text_input("Time duration", placeholder="Permanen atau 1h, 1d")

    blocked_sites = load_blocked_sites()

    # Menampilkan daftar dalam bentuk DataFrame
    df = pd.DataFrame(blocked_sites)
    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns([1, 5])

    with col1:
        if st.button("Cancel"):
            st.warning("Input dibatalkan.")

    with col2:
        if st.button("Submit"):
            if domain and schedule and duration:
                ssh_client = ssh_connect()
                if ssh_client:
                    block_site(ssh_client, domain, str(schedule), duration)
                    ssh_client.close()
                    st.experimental_rerun()
                else:
                    st.error("Gagal menghubungkan ke SSH. Periksa koneksi.")
            else:
                st.warning("Harap isi semua kolom!")
