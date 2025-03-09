import streamlit as st

def run():
     st.subheader("SSID & Password")
     st.write("Manage SSID and password")
     st.text_input("SSID")
     st.text_input("Password")

     col1, col2= st.columns([1, 5])

     with col1:
        if st.button("Cancel"):
            st.success("Input dibatalkan.")

     with col2:
        if st.button("submit"):
            st.success("Konfigurasi berhasil disimpan.")
     
