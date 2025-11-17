import streamlit as st
import requests

st.title("HAR Recorder")

url = st.text_input("Enter URL to record:", placeholder="https://www.example.com")

if st.button("Start Recording"):
    if not url:
        st.error("Please enter a URL.")
    else:
        res = requests.post(
            "http://localhost:5001/start",
            json={"url": url}
        )
        st.json(res.json())

if st.button("Stop Recording"):
    res = requests.post("http://localhost:5001/stop")
    st.json(res.json())
