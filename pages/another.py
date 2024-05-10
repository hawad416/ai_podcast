
import streamlit as st

st.title("🍭 Hawa's Creative Studio 🍭")
st.subheader("my episodes 🎞️")

st.sidebar.header("🍭 p o d s 🍭")

st.sidebar.page_link("main.py", label="🎙️ Create New Podcast")
st.sidebar.page_link("./pages/another.py", label="▶️ My Episodes")