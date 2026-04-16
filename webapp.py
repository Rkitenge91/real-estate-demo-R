import streamlit as st

st.set_page_config(page_title="Home")

with open("welcome_page_format.md", "r") as text:
    markdown_text = text.read()
st.markdown(markdown_text)