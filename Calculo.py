import streamlit as st # Calculo.py — versão unificada (Home + Cálculo)
import pandas as pd
from datetime import datetime

from utils import (
    carregar_tabela,
    validar_placa,
    calcular_excesso,
    salvar_csv,
    limpar_estado,
    verificar_login,
    gerar_tabela_formatada,
)

st.set_page_config(page_title="📦 Apuração de Pesos e Dimensões - DER DF", page_icon="📦", layout="wide")

if "login_realizado" not in st.session_state: # Gate de login (mantido do projeto original)
    verificar_login()
    st.session_state["login_realizado"] = True

# ÁREA DE CÁLCULO (migrada de pages/1_📦_Calculo.py)

# Variáveis auxiliares
pbt = limite = excesso = 0
r = {}

# Carrega a tabela de caminhões
tabela = carregar_tabela("data/Caminhoes.csv")

st.info("⬅️ Utilize o menu lateral para navegar entre as funcionalidades.")
st.title("📦 Apuração de Pesos e Dimensões - DER DF")

# Seletor do tipo + entradas principais
col1, col2, col3 = st.columns(3)
with col1:
    tipo = st.selectbox("Selecione o Tipo de Caminhão", tabela["Codigo"].unique(), key="tipo")
with col2:
    comprimento = st.number_input("Comprimento (em metros)", min_value=0.0, key="comprimento")
with col3:
    peso_liqnf = st.number_input("Peso Líquido da Nota Fiscal (Kg)", min_value=0.0, key="peso_liqnf")

# Linha selecionada e dados do tipo
linha = tabela[tabela["Codigo"] == tipo].iloc[0]
qt_tara = int(linha["Qtara"])
nome_caminhao = linha["Nome"]
st.info(f"Tipo Selecionado: **{nome_caminhao}**")

# Entradas por unidade (placa + tara)
placas = []
taras = []

st.subheader("🚛 Informações de cada unidade (Placa + Tara)")
for i in range(qt_tara):
    c1, c2 = st.columns(2)
    with c1:
        placa = st.text_input(f"Placa {i+1}", key=f"placa_{i}").strip().upper()
    with c2:
        tara = st.number_input(f"Tara {i+1} (Kg)", min_value=0.0, key=f"tara_{i}")
    placas.append(placa)
    taras.append(tara)

# Estados de controle
for key in ["calculado", "validado", "resultado", "dados_tipo"]:
    st.session_state.setdefault(key, False if key in ["calculado", "validado"] else None)

# Validação
if st.button("✅ Validar Dado(s)"):
    validado = True
    for i in range(qt_tara):
        placa_i = placas[i]
        if len(placa_i) != 7 or not validar_placa(placa_i):
            st.error(f"❌ Placa {i+1} inválida.")
            validado = False
        else:
            st.success(f"✅ Placa {i+1} válida: {placa_i} | Tara: {taras[i]} Kg")
    st.session_state.validado = validado

# Cálculo
if st.session_state.validado:
    if st.button("Calcular"):
        if not all(placas) or any(t == 0 for t in taras) or peso_liqnf == 0:
            st.error("⚠️ Preencha corretamente todos os campos.")
        else:
            pbt, limite, excesso = calcular_excesso(linha, taras, peso_liqnf, comprimento)
            agora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            dados_exportar = {
                "DataHora": agora,
                "TipoCaminhao": tipo,
                "Placas": ";".join(placas),
                "TaraTotal": int(sum(taras)),
                "PesoLiq": peso_liqnf,
                "Comprimento": comprimento,
                "PBT": int(pbt),
                "LimiteLegal": int(limite),
                "Excesso": int(excesso),
                "Usuario": st.session_state.get("usuario_logado", "desconhecido"),
            }
            salvar_csv(dados_exportar)

            st.session_state.calculado = True
            st.session_state.resultado = dados_exportar
            st.session_state["dados_tipo"] = {
                "TipoCam": tipo,
                "TamMaxPermitido": f"{linha['Tamax']:.1f}",
                "AET": linha["AET"],
                "OBS": linha["OBS"],
            }
            st.rerun()

# Exibição de resultados
if st.session_state.calculado:
    r = st.session_state.resultado.copy()
    r.pop("DataHora", None)
    r.pop("Usuario", None)

    st.markdown("---")
    st.subheader("📊 Resultado da Apuração")
    st.markdown(gerar_tabela_formatada(r), unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📘 Dados Complementares")
    st.table(pd.DataFrame([st.session_state["dados_tipo"]]))

    if r["Excesso"] > 0:
        st.error(f"🚨 Excesso de Peso: {r['Excesso']} Kg.")
        st.markdown(
            f"""
**Fiscalização por Nota Fiscal**  
Classificação por eixos:  {tipo}  
De acordo com a Portaria 268/2022 do Senatran  
Semirreboque: {r["Placas"]}  
Configuração inferior a {linha["Tam"]} metros  
Tara: {r["TaraTotal"]:.0f} kg - (conforme plaquetas)  
Carga: {r["PesoLiq"]:.2f} kg - (produto)  NF nº xxxxxxx  
PBTC apurado: {r["PBT"]:.2f} kg  
Limite regulamentar: {r["LimiteLegal"]:.0f} kg  
Excesso apurado: {r["Excesso"]:.2f} kg  
Transportador: (transportador)  |  Expedidor: (expedidor) |  Embarcador: (embarcador)
CNPJ: (cnpj)  

Autuação realizada conforme Resolução 882/21 do CONTRAN  
Transbordo não realizado devido indisponibilidade de meios operacionais para tal fim.
"""
        )
    else:
        st.success("✅ Peso dentro do limite.")

    if st.button("🔁 Nova Apuração"):
        limpar_estado()
        st.rerun()
