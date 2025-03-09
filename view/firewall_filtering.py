import streamlit as st
import pandas as pd


def run():
    st.subheader("Firewall Filtering")
    st.write("Manage firewalls to block websites")

    col1, col2, col3 = st.columns(3)

    with col1:
        domain = st.text_input("Domain/Url")

    with col2:
        schedule = st.date_input("Schedule")

    with col3:
        st.text_input("Time duration")

    blocked_sites = pd.DataFrame({
        "Domain/Url": ["facebook.com", "youtube.com"],
        "Schedule": ["2025-02-19", "2025-02-20"],
        "Time duration": ["Permanen", "1 Jam"]
    })

    st.dataframe(blocked_sites, use_container_width=True)

    col1, col2= st.columns([1, 5])

    with col1:
        if st.button("Cancel"):
            st.success("Input dibatalkan.")

    with col2:
        if st.button("submit"):
            st.success("Konfigurasi berhasil disimpan.")

