import streamlit as st
import os
import glob
from utils import verificar_login

if "login_realizado" not in st.session_state:
    verificar_login()
    st.session_state["login_realizado"] = True

st.title("📄 Anexo da Resolução - Tipos de Caminhão")

lista_jpgs = sorted(glob.glob(os.path.join("imagens", "*.jpg")))
nomes_arquivos = [os.path.basename(f) for f in lista_jpgs]

selecionado = st.selectbox("Selecione a imagem:", nomes_arquivos)

if selecionado:
    caminho_img = os.path.join("imagens", selecionado)
    st.image(caminho_img, caption=selecionado, use_container_width=True)
