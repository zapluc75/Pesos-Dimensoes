import streamlit as st
import pandas as pd
from utils import verificar_login

if "login_realizado" not in st.session_state:
    verificar_login()
    st.session_state["login_realizado"] = True

st.info("⬅️ Utilize o menu lateral para navegar entre as funcionalidades.")
st.title("🔍 Pesquisa Avançada de Pesagens")

tabela = pd.read_csv("data/resultados.csv")
tabela["DataHora"] = pd.to_datetime(tabela["DataHora"], format="%d-%m-%Y %H:%M:%S")
tabela["Dia"] = tabela["DataHora"].dt.day
tabela["Mes"] = tabela["DataHora"].dt.month
usuario = st.session_state.get("usuario_logado")

# Admin vê tudo, outros veem só o que lançaram
if usuario != "admin":
    tabela = tabela[tabela["Usuario"] == usuario]

meses = sorted(tabela["Mes"].unique())
mes_escolhido = st.selectbox("Selecione o mês:", meses)
dias_disponiveis = sorted(tabela[tabela["Mes"] == mes_escolhido]["Dia"].unique())
dia_escolhido = st.selectbox("Selecione o dia:", dias_disponiveis)

filtro = (tabela["Mes"] == mes_escolhido) & (tabela["Dia"] == dia_escolhido)
dados_filtrados = tabela[filtro]

colunas = ["DataHora", "TipoCaminhao", "Placas", "TaraTotal", "PesoLiq", "Comprimento", "PBT", "LimiteLegal", "Excesso", "Usuario"]
st.dataframe(dados_filtrados[colunas].reset_index(drop=True))
