import streamlit as st

def run():
    st.subheader("Bandwidth Fix")
    st.write("Manage bandwitdth limits")
    st.text_input("Target IP Address")
    st.number_input("Upload Speed (Mbps)", min_value=0.0)
    st.number_input("Download Speed (Mbps)", min_value=0.0)
    
    col1, col2= st.columns([1, 5])

    with col1:
        if st.button("Cancel"):
            st.success("Input dibatalkan.")

    with col2:
        if st.button("submit"):
            st.success("Konfigurasi berhasil disimpan.")
