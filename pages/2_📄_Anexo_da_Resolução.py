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

# --- Selectbox para navegação rápida ---
selecionado = st.selectbox("🔎 Escolha um caminhão:", nomes_formatados, index=0)

# --- Grid de imagens (miniaturas clicáveis) ---
num_colunas = 6
img_clicada = None

for i in range(0, len(nomes_arquivos), num_colunas):
    cols = st.columns(num_colunas)
    for j in range(num_colunas):
        if i + j < len(nomes_arquivos):
            caminho_img = lista_jpgs[i + j]
            nome_original = nomes_arquivos[i + j]
            nome_formatado = nomes_formatados[i + j]
            with cols[j]:
                if st.button("", key=nome_original):
                    img_clicada = nome_original
                st.image(caminho_img, caption=nome_formatado, use_container_width=True)
# --- Determinar seleção final ---
if img_clicada:
    escolhido = img_clicada
else:
    # Pega pelo selectbox se nenhum botão for clicado
    escolhido = nomes_arquivos[nomes_formatados.index(selecionado)]
    
# --- Exibição em destaque ---
caminho_final = os.path.join("imagens", escolhido)
st.markdown("---")
st.image(caminho_final, caption=formatar_nome(escolhido), use_container_width=True)
