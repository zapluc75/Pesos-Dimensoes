import streamlit as st
import base64
from pathlib import Path
from utils import verificar_login

st.set_page_config(page_title="Fichas do Manual de Fiscalização", page_icon="📚", layout="centered")

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

cols = st.columns(3) #Cria layout em 3 colunas

for i, pdf_path in enumerate(pdf_files): # Loop para exibir os links nas colunas
    path = Path(pdf_path)

    with cols[i % 3]:  # distribui nas 3 colunas
        if path.exists():
            with open(path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode("utf-8")
            
            nome = path.stem.capitalize() # Nome do arquivo sem caminho

            # Cria o link para abrir o PDF
            link_html = f"""
            <a href="data:application/pdf;base64,{base64_pdf}" 
               target="_blank" 
               style="text-decoration:none; font-size:16px;">
               📄 Abrir {nome}
            </a>
            """
            st.markdown(link_html, unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ Arquivo não encontrado: {path.name}")
