import streamlit as st
import base64
from pathlib import Path

pdf_path = Path("data/ficha.pdf")

if pdf_path.exists():
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.error("❌ Arquivo 'data/ficha.pdf' não encontrado.")
