import streamlit as st

st.title("Monitoring Client")

client_id = st.selectbox("Pilih Client yang ingin dimonitor", ["Client 1", "Client 2", "Client 3", "Client 4"])

st.write(f"Monitoring status untuk {client_id}:")
st.write("Data monitoring ditampilkan di sini.")

if st.button("Refresh Data"):
    st.success(f"Data client {client_id} berhasil diperbarui.")
