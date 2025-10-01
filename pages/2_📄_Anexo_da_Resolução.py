import streamlit as st
import os
import glob
from utils import verificar_login

# --- Controle de login ---
if "login_realizado" not in st.session_state:
    verificar_login()
    st.session_state["login_realizado"] = True
    
# --- Funções auxiliares ---
def formatar_nome(nome):
    """Remove extensão e ajusta underscores para exibir bonito."""
    return os.path.splitext(nome)[0].replace("_", " ").title()

# --- Cabeçalho ---
st.title("📄 Anexo da Resolução - Tipos de Caminhão")
st.info("⬅️ Use o menu lateral para navegar entre as funcionalidades.")
st.success("🚚 Clique em um modelo ou use a lista suspensa para visualizar em destaque!")

# --- Lista de imagens ---
lista_jpgs = sorted(glob.glob(os.path.join("imagens", "*.jpg")))
nomes_arquivos = [os.path.basename(f) for f in lista_jpgs]
nomes_formatados = [formatar_nome(f) for f in nomes_arquivos]

# --- Grid de imagens (miniaturas clicáveis) ---
num_colunas = 6
selecionado = None #Variável para armazenar seleção

for i in range(0, len(nomes_arquivos), num_colunas):
    cols = st.columns(num_colunas)
    for j in range(num_colunas):
        if i + j < len(nomes_arquivos):
           with cols[j]:
               if st.button(nomes_formatados[i + j]):
                   selecionado = nomes_arquivos[i + j]

if selecionado:
    caminho_img = os.path.join("imagens", selecionado)
    st.markdown("---")
    st.image(caminho_img, caption=selecionado, use_container_width=True)

