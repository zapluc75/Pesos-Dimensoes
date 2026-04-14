import os
import re
import pandas as pd
import streamlit as st
import hashlib
import time

def autenticar(usuario, senha): #validar o login
    usuarios = st.secrets["usuarios"]
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    return usuario in usuarios and usuarios[usuario] == senha_hash

def verificar_login(): #registra no sistema
    if "tentativas" not in st.session_state: # Inicializa controle
        st.session_state.tentativas = 0
    if "bloqueado_ate" not in st.session_state:
        st.session_state.bloqueado_ate = 0

    agora = time.time() # Verifica bloqueio
    if agora < st.session_state.bloqueado_ate:
        restante = int(st.session_state.bloqueado_ate - agora)
        st.error(f"🔒 Muitas tentativas. Aguarde {restante}s.")
        st.stop()
        
    if st.session_state.get("autenticado"): #se já autenticado
        return True

    st.title("🔐 Autenticação Necessária")

    usuario = st.text_input("Usuario")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if autenticar(usuario, senha): # Sucesso → reset
            st.session_state.autenticado = True
            st.session_state.usuario_logado = usuario
            st.session_state.tentativas = 0
            st.rerun()
        else: # Falha → incrementa
            st.session_state.tentativas += 1
            if st.session_state.tentativas >= 5:
                st.session_state.bloqueado_ate = agora + 60  # 60 segundos
                st.session_state.tentativas = 0
                st.error("🔒 Muitas tentativas. Bloqueado por 60s.")
            else:
                restante = 5 - st.session_state.tentativas
                st.error(f"❌ Usuário ou senha inválidos. Tentativas restantes: {restante}")
    
    st.stop()

@st.cache_data
def carregar_tabela(nome_arquivo):
    return pd.read_csv(nome_arquivo)

def validar_placa(placa: str) -> bool:
    padrao = r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$'
    return re.fullmatch(padrao, placa.upper()) is not None

def calcular_excesso(linha, taras, peso_liqnf, comprimento):
    pbt = sum(taras) + peso_liqnf
    limite = linha["Pbt2"] if comprimento >= linha["Tam"] else linha["Pbt1"]
    excesso = max(0, pbt - limite)
    return pbt, limite, excesso

def limpar_estado():
    manter = [
        "login_realizado",
        "autenticado",
        "usuario_logado",
        "tentativas",
        "bloqueado_ate"
    ]

    for key in list(st.session_state.keys()):
        if key not in manter:
            del st.session_state[key]

def gerar_tabela_formatada(dados):
    html = """
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 15px; /* opcional: diminui o tamanho da fonte */
        }
        th, td {
            text-align: center;
            padding: 2px 6px; /* padding vertical reduzido */
            border: 1px solid #ddd;
        }
        th {
            background-color: #808080;
        }
    </style>
    <table>
        <tr><th style="text-align: center;">Campo</th><th style="text-align: center;">Valor</th></tr>
    """
    for chave, valor in dados.items():
        html += f"<tr><td>{chave}</td><td>{valor}</td></tr>"
    html += "</table>"
    return html

def to_upper(key):
    st.session_state[key] = st.session_state[key].strip().upper()
