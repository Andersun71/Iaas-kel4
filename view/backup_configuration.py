import streamlit as st
import pandas as pd

def run():
    st.subheader("Backup Configuration")

    st.text_input("Backup name")

    data = {
        "Name": ["Backup_1", "Backup_2", "Backup_3"],
        "Type": ["Backup", "Backup", "Backup"],
        "Size": ["2GB", "1GB", "500MB"],
        "Created At": ["2025-02-18 10:00", "2025-02-17 09:30", "2025-02-16 08:45"]
    }
    
    df = pd.DataFrame(data)

    st.dataframe(df, use_container_width=True)

    col1, col2, col3 = st.columns([0.9, 1, 4.5])

    with col1:
        if st.button("Backup"):
            st.success("Konfigurasi berhasil disimpan.")

    with col2:
        if st.button("Download"):
            st.success("File berhasil diunduh.")

    with col3:
        if st.button("Cancel"):
            st.warning("Input dibatalkan.")