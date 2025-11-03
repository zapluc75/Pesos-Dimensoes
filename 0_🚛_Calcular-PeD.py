import streamlit as st # Calculo.py — versão unificada (Home + Cálculo)
import pandas as pd
from datetime import datetime
from st_copy import copy_button
import textwrap

from utils import (
    carregar_tabela,
    validar_placa,
    calcular_excesso,
    limpar_estado,
    verificar_login,
    gerar_tabela_formatada,
)

st.set_page_config(page_title="Apuração Pesos e Dimensões - DERDF", page_icon="📦", layout="centered")

if "login_realizado" not in st.session_state: # Gate de login (mantido do projeto original)
    verificar_login()
    st.session_state["login_realizado"] = True

# ÁREA DE CÁLCULO (migrada de pages/1_📦_Calculo.py)

# Variáveis auxiliares
pbt = limite = excesso = float(0.0)
r = {}

# Carrega a tabela de caminhões
tabela = carregar_tabela("data/Caminhoes.csv")

st.info("⬅️ Utilize o menu lateral para navegar entre as funcionalidades.")
st.title("📦 Apuração Pesos e Dimensões - DER DF")

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
st.info(f"Selecionado ----> **{nome_caminhao}**")

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
    if not all(placas) or sum(taras) <= 0 or peso_liqnf == 0:
        st.error("⚠️ Preencha corretamente todos os campos.")
    else:
        col_left, col_center, col_right = st.columns([1, 1, 1]) # Botão centralizado usando colunas
        with col_center:
            calc_click = st.button ("❌ C A L C U L A R ", use_container_width=True)
        if calc_click: 
            pbt, limite, excesso = calcular_excesso(linha, taras, peso_liqnf, comprimento)
            agora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            dados_exportar = {
                "DataHora": agora,
                "TipoCaminhao": tipo,
                "Placas": ";".join(placas),
                "TaraTotal": int(sum(taras)),
                "PesoLiqNF": peso_liqnf,
                "Comprimento": comprimento,
                "PBT-PBTC": float(pbt),
                "LimiteLegal": float(limite),
                "Excesso": float(excesso),
                "Usuario": st.session_state.get("usuario_logado", "desconhecido"),
            }
            
            st.session_state.calculado = True
            st.session_state.resultado = dados_exportar
            st.session_state["dados_tipo"] = {
                "TipoCam": tipo,
                "TamMaxPermit": f"{linha['Tamax']:.1f}",
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
    st.subheader("📘 Dados Complementares")
    st.table(pd.DataFrame([st.session_state["dados_tipo"]]))
    
    st.markdown("---")
    st.subheader("📊 Resultado da Apuração")
    st.markdown(gerar_tabela_formatada(r), unsafe_allow_html=True)
   
    if r["Excesso"] > 0:
        st.error(
            f"""
        🚨 **Excesso de Peso:** {r['Excesso']:.2f} Kg ----> **Infração:** Art. 231, V do CTB

        **Código de Enquadramento:** 68311 - Transitar com o veículo com excesso de peso PBT/PBTC.
        """
        )
           
        texto = textwrap.dedent(f"""\
        **Fiscalização por Nota Fiscal**  
        Classificação por eixos:  {tipo}  
        De acordo com a Portaria 268/2022 do Senatran  
        Veículo/Combinação: {r["Placas"]}  
        Comprimento Total: ( ) metros  
        Tara: {r["TaraTotal"]:.0f} kg - (conforme plaquetas)  
        Carga: {r["PesoLiqNF"]:.0f} kg - (produto)  NF nº xxxxxxx  
        PBTC apurado: {r["PBT-PBTC"]:.0f} kg  
        Limite regulamentar: {r["LimiteLegal"]:.0f} kg  
        Excesso apurado: {r["Excesso"]:.0f} kg  
        Transportador: (transportador)  |  CNPJ/CPF: (cnpj/cpf)  

        Autuação realizada conforme Resolução 882/21 do CONTRAN  
        Transbordo não realizado devido indisponibilidade de meios operacionais para tal fim.
        """)
            
        st.markdown(texto) # 1) Exibir na tela com formatação Markdown

        copy_button(texto, tooltip="Copiar", copied_label="✅ Copiado!") # 2) Botão para copiar
            
    else:
        st.success("✅ Peso dentro do limite.")
        st.markdown(r["Placas"])
        copy_button(r["Placas"], tooltip="Copias", copied_label=""✅ Copiado!") # 2) Botão para copiar

    if (comprimento - linha["Tamax"]) > 0 or linha["AET"] == "Sim":
        st.error(f"🚨 Combinação {tipo} de {comprimento}m *** Necessita AET *** Tamanho Máximo Permitido {linha['Tamax']:.1f}m.")
    else:
        st.success(f"✅ Combinação dentro do Tamanho Máximo Permitido")

    col_l, col_c, col_r = st.columns([1, 1, 1])  # Botão centralizado usando colunas
    with col_c:
        reset_click = st.button(" 🔁 N O V A - A P U R A Ç Ã O", use_container_width=True)

    if reset_click:
        limpar_estado()
        st.rerun()
