import streamlit as st
from datetime import datetime
from utils import carregar_tabela, validar_placa, calcular_excesso, salvar_csv, limpar_estado, verificar_login
import pandas as pd
pbt = limite = excesso = 0
r = {}

if "login_realizado" not in st.session_state:
    verificar_login()
    st.session_state["login_realizado"] = True

st.title("📦 APURAÇÃO DE PESOS E DIMENSÕES - DER DF")

tabela = carregar_tabela("data/Caminhoes.csv")
col1, col2, col3 = st.columns(3)
with col1:
    tipo = st.selectbox("Selecione o Tipo de Caminhão", tabela["Codigo"].unique(), key="tipo")
with col2:
    comprimento = st.number_input("Comprimento (em metros)", min_value=0, key="comprimento")
with col3:
    nota_fiscal = st.number_input("Peso Líquido da Nota Fiscal (Kg)", min_value=0, key="nota_fiscal")

linha = tabela[tabela["Codigo"] == tipo].iloc[0]
qt_tara = linha["Qtara"]
nome_caminhao = linha["Nome"]
st.info(f"Tipo Selecionado: **{nome_caminhao}**")

placas = []
taras = []

st.subheader("🚛 Informações de cada unidade (Placa + Tara)")
for i in range(qt_tara):
    col1, col2 = st.columns(2)
    with col1:
        placa = st.text_input(f"Placa {i+1}", key=f"placa_{i}").strip().upper()
    with col2:
        tara = st.number_input(f"Tara {i+1} (Kg)", min_value=0.0, key=f"tara_{i}")
    placas.append(placa)
    taras.append(tara)

for key in ["calculado", "validado"]:
    st.session_state.setdefault(key, False)

if st.button("✅ Validar Dado(s)"):
    validado = True
    for i in range(qt_tara):
        placa = placas[i]
        if len(placa) != 7 or not validar_placa(placa):
            st.error(f"❌ Placa {i+1} inválida.")
            validado = False
        else:
            st.success(f"✅ Placa {i+1} válida: {placa} | Tara: {taras[i]} Kg")
    st.session_state.validado = validado

if st.session_state.validado:
    if st.button("Calcular"):
        if not all(placas) or any(t == 0 for t in taras) or nota_fiscal == 0:
            st.error("⚠️ Preencha corretamente todos os campos.")
        else:
            pbt, limite, excesso = calcular_excesso(linha, taras, nota_fiscal, comprimento)
            agora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            dados_exportar = {
                "DataHora": agora,
                "TipoCaminhao": tipo,
                "Placas": ";".join(placas),
                "TaraTotal": int(sum(taras)),
                "NotaFiscal": nota_fiscal,
                "Comprimento": comprimento,
                "PBT": int(pbt),
                "LimiteLegal": int(limite),
                "Excesso": int(excesso),
                "Usuario": st.session_state.get("usuario_logado", "desconhecido")
            }
            dados_exportar["Usuario"] = st.session_state.get("usuario_logado", "desconhecido")
            salvar_csv(dados_exportar)
            st.session_state.calculado = True
            st.session_state.resultado = dados_exportar
            st.rerun()

if st.session_state.calculado:
    r = st.session_state.resultado.copy()
    r.pop("DataHora")
    r.pop("Usuario")
    st.markdown("---")
    st.subheader("📊 Resultado da Apuração")
    # Converte o dicionário em DataFrame com uma linha
    df_resultado = pd.DataFrame([r])

    # Exibe em formato tabular e alinhado
    st.table(df_resultado)
    if r["Excesso"] > 0:
        st.error(f"🚨 Excesso de Peso: {r['Excesso']} Kg.")
        st.markdown(f"""
        **Fiscalização por Nota Fiscal**  
        Classificação por eixos:  {tipo}  
        De acordo com a Portaria 268/2022 do Senatran  
        Semirreboque: {r["Placas"]}  
        Configuração inferior a {r["Comprimento"]} metros  
        Tara: {r["TaraTotal"]:.0f} kg - (conforme plaquetas)  
        Carga: {r["NotaFiscal"]:.2f} kg - (produto)  NF nº xxxxxxx  
        PBTC apurado: {r["PBT"]:.2f} kg  
        Limite regulamentar: {r["LimiteLegal"]:.0f} kg  
        Excesso apurado: {r["Excesso"]:.2f} kg  
        Transportador: (transportador)  |  Expedidor: (expedidor) |  Embarcador: (embarcador)
        CNPJ: (cnpj)  
        \nAutuação realizada conforme Resolução 882/21 do CONTRAN  
        Transbordo não realizado devido indisponibilidade de meios operacionais para tal fim.
        """)
    else:
        st.success("✅ Peso dentro do limite.")
    if st.button("🔁 Nova Apuração"):
        limpar_estado()
        st.rerun()
