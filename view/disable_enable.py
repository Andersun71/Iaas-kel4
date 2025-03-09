import streamlit as st

def run():
    st.subheader("Disable/Enable Interfaces")
    st.write("Manage nterfaces")
    st.selectbox("Select Interface", ["ether1", "ether2", "ether3", "wlan1", "wlan2"])
    st.selectbox("Action", ["Disable", "Enable"])
    
    col1, col2= st.columns([1, 5])

    with col1:
        if st.button("Cancel"):
            st.success("Input dibatalkan.")

    with col2:
        if st.button("submit"):
            st.success("Konfigurasi berhasil disimpan.")


