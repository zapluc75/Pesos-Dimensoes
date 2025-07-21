import streamlit as st
from utils import verificar_login

if "login_realizado" not in st.session_state:
    verificar_login()
    st.session_state["login_realizado"] = True

st.title("📦 Aplicação de Pesagem de Caminhões")
st.markdown("Utilize o menu lateral para navegar entre as funcionalidades.")
