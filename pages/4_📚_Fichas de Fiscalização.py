import streamlit as st
import base64
from pathlib import Path
from utils import verificar_login

st.set_page_config(page_title="📚 Fichas do Manual de Fiscalização", page_icon=", layout="centered")

if "login_realizado" not in st.session_state: # Gate de login (mantido do projeto original)
    verificar_login()
    st.session_state["login_realizado"] = True

st.info("⬅️ Utilize o menu lateral para navegar entre as funcionalidades.")
st.title("📚 Fichas do Manual de Fiscalização")
st.markdown("---")

# Lista de arquivos PDF (pode adicionar quantos quiser)
pdf_files = [
    "data/66450Art230X.pdf",
    "data/68231Art231IV.pdf",
    "data/68311Art231V.pdf",
]

col1, col2, col3 = st.columns(3)
with col1:
with col2:
    pdf_path = Path("data/68311Art231V.pdf") # Caminho do PDF
    if pdf_path.exists():# Verifica se o arquivo existe
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")

        # Cria um link clicável chamado "Ficha"
        pdf_link = f'<a href="data:application/pdf;base64,{base64_pdf}" target="_blank">📄 Excesso de Peso PBT/PTBC</a>'
        st.markdown(pdf_link, unsafe_allow_html=True)
    else:
        st.warning("⚠️ O arquivo 'data/ficha.pdf' não foi encontrado.")
with col3:


