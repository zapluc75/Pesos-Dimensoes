import os
import re
import pandas as pd
import streamlit as st
import hashlib

def verificar_login():
    if st.session_state.get("autenticado"):
        return True

    st.title("🔐 Autenticação Necessária")

    usuario = st.text_input("Usuario")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if autenticar(usuario, senha):
            st.session_state.autenticado = True
            st.session_state.usuario_logado = usuario
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")
    st.stop()

def autenticar(usuario, senha):
    usuarios = st.secrets["usuarios"]
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    if usuario in usuarios and usuarios[usuario] == senha_hash:
        st.session_state.usuario_logado = usuario  # <- Aqui armazena o login ativo
        return True
    return False

@st.cache_data
def carregar_tabela(nome_arquivo):
    return pd.read_csv(nome_arquivo)

def validar_placa(placa: str) -> bool:
    padrao = r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$'
    return re.fullmatch(padrao, placa.upper()) is not None

def calcular_excesso(linha, taras, nota_fiscal, comprimento):
    pbt = sum(taras) + nota_fiscal
    limite = linha["Pbt1"] if comprimento <= linha["Tam"] else linha["Pbt2"]
    excesso = max(0, pbt - limite)
    return pbt, limite, excesso

def salvar_csv(dados, nome_arquivo="data/resultados.csv"):
    try:
        df = pd.DataFrame([dados])
        if os.path.exists(nome_arquivo):
            df.to_csv(nome_arquivo, mode='a', header=False, index=False)
        else:
            df.to_csv(nome_arquivo, index=False)
    except Exception as e:
        st.error(f"Erro ao salvar arquivo: {e}")

def limpar_estado():
    for key in list(st.session_state.keys()):
        if key != "login_realizado":
            del st.session_state[key]