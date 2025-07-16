import streamlit as st

st.set_page_config(
    page_title="Cash In App",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Cash In App")
st.write("Welcome to your Cash In application!")

name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello {name}! 👋")

amount = st.number_input("Enter amount:", min_value=0.0)
if st.button("Cash In"):
    if amount > 0:
        st.success(f"Cashed in ")
    else:
        st.error("Enter valid amount")
