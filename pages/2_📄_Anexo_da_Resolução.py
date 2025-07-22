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

selecionado = None #Variável para armazenar seleção
num_colunas = 6

for i in range(0, len(nomes_arquivos), num_colunas): #Cria pares de elementos (2 por linha)
    cols = st.columns(num_colunas)

    for j in range (num_colunas):
        if i + j < len(nomes_arquivos):
            with cols[j]:
                if st.button(nomes_arquivos[i + j]):
                    selecionado = nomes_arquivos[i + j]
if selecionado:
    caminho_img = os.path.join("imagens", selecionado)
    st.image(caminho_img, caption=selecionado, use_container_width=True)