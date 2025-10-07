import streamlit as st
import pandas as pd

from utils import (
    validar_placa,
    limpar_estado,
    verificar_login,
)

def precisa_tacografo(placa: str, ano: int, cmt: int, pbt: int) -> bool:
    """
    Regras (do script original):
    - Se ANO <= 1998 e CMT >= 19000  -> precisa tacógrafo
    - Se ANO >= 1999 e PBT >= 4536   -> precisa tacógrafo
    - Caso contrário                  -> não precisa
    """
    if ano <= 1998 and cmt >= 19000:
        return True
    elif ano >= 1999 and pbt >= 4536:
        return True
    return False

if "login_realizado" not in st.session_state:
    verificar_login()
    st.session_state["login_realizado"] = True

st.set_page_config(page_title="Verificador de Tacógrafo", page_icon="🧭", layout="centered")
st.info("⬅️ Utilize o menu lateral para navegar entre as funcionalidades.")
st.title("🧭 Verificador de Tacógrafo para Caminhões")

with st.form("form_tacografo", clear_on_submit=False):
    placa = st.text_input("Placa do caminhão", placeholder="ABC1D23 / ABC-1234").strip().upper()
    col1, col2 = st.columns(2)
    with col1:
        ano = st.number_input("Ano de fabricação", min_value=1900, max_value=2100, step=1, value=1998)
        cmt = st.number_input("Capacidade Máxima de Tração (CMT) em kg", min_value=0, step=1, value=19000)
    with col2:
        pbt = st.number_input("Peso Bruto Total (PBT) em kg", min_value=0, step=1, value=4536)

    submitted = st.form_submit_button("Verificar")

if submitted:
    if not placa:
        st.error("Informe a **placa**.")
        st.stop()

    precisa = precisa_tacografo(placa, int(ano), int(cmt), int(pbt))

    if precisa:
        st.success(f"Caminhão **{placa}** --> PRECISA DO TACÓGRAFO.")
    else:
        st.info(f"Caminhão **{placa}** --> NÃO PRECISA DO TACÓGRAFO.")

st.markdown("""
### 🚚 [Cronotacógrafo](https://cronotacografo.rbmlq.gov.br/certificados/consultar)
""")

st.markdown("---")

col_l, col_c, col_r = st.columns([1, 1, 1])  # Botão centralizado usando colunas
with col_c:
    reset_click = st.button(" 🔁 N O V A - A P U R A Ç Ã O", use_container_width=True)

if reset_click:
    limpar_estado()
    st.rerun()
