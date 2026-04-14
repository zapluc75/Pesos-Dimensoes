import streamlit as st
import os
import glob
from utils import verificar_login

# --- Controle de login ---
if "login_realizado" not in st.session_state:
    verificar_login()
    st.session_state["login_realizado"] = True
    
# --- Funções auxiliares ---
def dividir_nome(nome):
    """Separa em prefixo (antes do 1º espaço) e sufixo (restante)."""
    base = os.path.splitext(nome)[0].replace("_", " ")
    partes = base.split(" ", 1)  # divide só no primeiro espaço
    prefixo = partes[0]
    sufixo = partes[1] if len(partes) > 1 else ""
    return prefixo, sufixo

# --- Cabeçalho ---
st.title("📄 Tipos de Caminhão")
st.info("⬅️ Use o menu lateral para navegar entre as funcionalidades.")

# --- Lista de imagens ---
lista_jpgs = sorted(glob.glob(os.path.join("imagens", "*.jpg")))
nomes_arquivos = [os.path.basename(f) for f in lista_jpgs]

# --- Grid de imagens (miniaturas clicáveis) ---
num_colunas = 6
selecionado = None #Variável para armazenar seleção

for i in range(0, len(nomes_arquivos), num_colunas):
    cols = st.columns(num_colunas)
    for j in range(num_colunas):
        if i + j < len(nomes_arquivos):
            nome_original = nomes_arquivos[i + j]
            prefixo, sufixo = dividir_nome(nome_original)
            with cols[j]:
                if st.button(prefixo, key=nome_original):
                    selecionado = nome_original
                if sufixo:  # só mostra legenda se existir
                    st.caption(sufixo)

st.success("🚚 Clique em um botão acima para visualizar em destaque abaixo! 👇")
if selecionado:
    caminho_img = os.path.join("imagens", selecionado)
    st.markdown("---")
    st.image(caminho_img, caption=selecionado, use_container_width=True)



