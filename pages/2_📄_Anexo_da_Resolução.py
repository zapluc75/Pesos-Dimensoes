import streamlit as st
import base64
from pathlib import Path
from utils import verificar_login

st.set_page_config(page_title="Anexo da Resolução", page_icon="📄", layout="centered")

# --- Controle de login ---
if "login_realizado" not in st.session_state:
    verificar_login()
    st.session_state["login_realizado"] = True

# --- Cabeçalho ---
st.title("📄 Anexo da Resolução - Tipos de Caminhão")
st.info("⬅️ Use o menu lateral para navegar entre as funcionalidades.")
st.markdown("---")
    
# Lista de arquivos PDF (pode adicionar quantos quiser)
pdf_files = [
    "imagens/C0_Cam.pdf",
    "imagens/CR0_Cam_Rbq.pdf",
    "imagens/CR0+_Cam_Rbq+.pdf",
    "imagens/CRR+_Cam_2-Rbq+.pdf",
    "imagens/CTS0_CamTrtr_SemiRbq.pdf",
    "imagens/CTSR+_CamTrtr_SemiRbq_Rbq+.pdf",
    "imagens/CTSR0_CamTrtr_SemiRbq_Rbq.pdf",
    "imagens/CTSRr+_CamTrtr_SemiRbq_Rbp_Rala+.pdf",
    "imagens/CTSS+_CamTrtr_2-SemiRbq.pdf",
    "imagens/CTSS0_CamTrtr_2-SemiRbq.pdf",
    "imagens/CTSSS+_CamTrtr_3-SemiRbq+.pdf",
]

# --- Cria layout em 3 colunas ---
cols = st.columns(3)

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
               📄 {nome}
            </a>
            """
            st.markdown(link_html, unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ Arquivo não encontrado: {path.name}")

