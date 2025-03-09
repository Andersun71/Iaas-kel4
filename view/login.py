import streamlit as st

def run():
    st.subheader("Login")
    st.text_input("IP Address")
    st.text_input("Username")
    st.text_input("Password", type="password")
    st.button("Submit")
