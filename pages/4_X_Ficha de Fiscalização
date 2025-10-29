import streamlit as st
import base64
from pathlib import Path

# Caminho do PDF
pdf_path = Path("data/ficha.pdf")

# Verifica se o arquivo existe
if pdf_path.exists():
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    # Cria um link clicável chamado "Ficha"
    pdf_link = f'<a href="data:application/pdf;base64,{base64_pdf}" target="_blank">📄 Abrir Ficha</a>'
    st.markdown(pdf_link, unsafe_allow_html=True)
else:
    st.warning("⚠️ O arquivo 'data/ficha.pdf' não foi encontrado.")
