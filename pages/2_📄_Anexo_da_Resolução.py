import streamlit as st
import os
import glob
from utils import verificar_login

if "login_realizado" not in st.session_state:
    verificar_login()
    st.session_state["login_realizado"] = True
    
def formatar_nome(nome):
    return os.path.splitext(nome)[0].replace("_").title()
    
st.info("⬅️ Utilize o menu lateral para navegar entre as funcionalidades.")
st.title("📄 Anexo da Resolução - Tipos de Caminhão")

lista_jpgs = sorted(glob.glob(os.path.join("imagens", "*.jpg")))
nomes_arquivos = [os.path.basename(f) for f in lista_jpgs]

selecionado = None #Variável para armazenar seleção
num_colunas = 6
st.success("🚚 Clique em um modelo para visualizar em destaque!")
nomes_arquivos_formatados = [formatar_nome(f) for f in nomes_arquivos]
for i in range(0, len(nomes_arquivos), num_colunas): #Cria pares de elementos (2 por linha)
    cols = st.columns(num_colunas)

    for j in range (num_colunas):
        if i + j < len(nomes_arquivos):
            caminho_img = lista_jpgs[i + j]
            nome = nomes_arquivos[i + j]
            with cols[j]:
                if st.button("", key=nome):
                    selecionado = nome
                st.image(caminho_img, caption=nome, use_container_width=True)

if selecionado:
    caminho_img = os.path.join("imagens", selecionado)
    st.markdown("---")
    st.image(caminho_img, caption=formatar_nome(selecionado), use_container_width=True)
