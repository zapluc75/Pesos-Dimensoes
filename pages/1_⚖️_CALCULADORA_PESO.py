import streamlit as st
import pandas as pd
from st_copy import copy_button
from utils import verificar_login
total=0

if "login_realizado" not in st.session_state:
    verificar_login()
    st.session_state["login_realizado"] = True

# --------- Configuração da página ---------
st.set_page_config(
    page_title="Calculadora de Peso Líquido",
    page_icon="⚖️",
    layout="centered",
)

# --------- Estado da aplicação ---------
if "entradas" not in st.session_state:
    st.session_state.entradas = []  # lista de dicts: {nf, oper, peso}
if "tabela_key" not in st.session_state:
    st.session_state.tabela_key = 0

# --------- Funções utilitárias ---------

def _assina(oper: str) -> int:
    return 1 if oper == "+" else -1


def _calc_totais(df: pd.DataFrame) -> tuple[float, int]:
    if df.empty:
        return 0.0, 0
    total = (df["Peso (kg)"] * df["Sinal"]).sum()
    total = float(total) #garantir float, sem truncar
    cont_nf = int((df["Operação"] == "+").sum())  # segue a lógica do seu script: só soma NF quando é adição
    return total, cont_nf


def _get_dataframe() -> pd.DataFrame:
    if not st.session_state.entradas:
        return pd.DataFrame(columns=["NF", "Operação", "Peso (kg)", "Sinal"])
    df = pd.DataFrame(st.session_state.entradas)
    # Garante tipos e ordem
    df = df[["NF", "Operação", "Peso (kg)", "Sinal"]]
    return df


def _set_dataframe(df: pd.DataFrame) -> None:
    # Atualiza o estado a partir do DataFrame (pós-edição)
    entradas = []
    for _, row in df.iterrows():
        oper = "+" if str(row["Operação"]).strip() == "+" else "-"
        peso = float(row["Peso (kg)"]) if pd.notna(row["Peso (kg)"]) else 0.0
        nf = str(row["NF"]).strip()
        entradas.append({"NF": nf, "Operação": oper, "Peso (kg)": peso, "Sinal": _assina(oper)})
    st.session_state.entradas = entradas

# --------- Cabeçalho ---------
st.info("⬅️ Utilize o menu lateral para navegar entre as funcionalidades.")
st.title("⚖️ Calculadora de Peso Líquido de Notas Fiscais")
st.caption(
    "Adicione entradas de peso (+) ou subtrações (-). O contador de NFs segue o seu script original: **somente** entradas com operação `+` contam como NF."
)

# --------- Formulário de entrada ---------
with st.form("form_entrada", clear_on_submit=True):
    st.subheader("Nova entrada")
    c1, c2, c3 = st.columns([1.2, 1, 1.2])
    with c1:
        # Sugere NF sequencial (apenas sugestão; pode ser vazio)
        sugestao_nf = str(len([e for e in st.session_state.entradas if e["Operação"] == "+"]) + 1).zfill(3)
        nf = st.text_input("Nº da Nota Fiscal (opcional)", value=sugestao_nf)
    with c2:
        oper = st.radio("Operação", options=[":green[➕ ad]", ":red[➖ sb]"], horizontal=True)
        oper = "+" if "➕" in oper else "-"
    with c3:
        peso = st.number_input("Peso (kg)", min_value=0.0, step=0.01, format="%.2f")

    c_bot1, c_bot2, c_bot3 = st.columns([1, 1, 1])
    with c_bot2:
        submitted = st.form_submit_button("Registrar", use_container_width=True)

    if submitted:
        if peso <= 0:
            st.warning("Informe um peso maior que zero.")
        else:
            st.session_state.entradas.append({
                "NF": nf.strip(),
                "Operação": oper,
                "Peso (kg)": float(peso),
                "Sinal": _assina(oper),
            })
            st.session_state.tabela_key += 1
            st.success("Entrada registrada.")

# --------- Tabela (editável) ---------
st.subheader("Entradas")
df = _get_dataframe()

if df.empty:
    st.info("Nenhuma entrada ainda. Use o formulário acima para começar.")
else:
    st.caption("Você pode **editar** NF, operação (+/-) e peso diretamente na tabela. As métricas são recalculadas automaticamente.")
    # Data editor configurado
    edited_df = st.data_editor(
        df.drop(columns=["Sinal"]).assign(**{"Operação": df["Operação"].astype(str)}),
        num_rows="dynamic",
        key=f"editor_{st.session_state.tabela_key}",
        use_container_width=True,
        hide_index=True,
        column_config={
            "NF": st.column_config.TextColumn("NF", help="Identificação da nota (opcional)"),
            "Operação": st.column_config.SelectboxColumn("Operação", options=["+", "-"], help="+ adiciona, - subtrai"),
            "Peso (kg)": st.column_config.NumberColumn("Peso (kg)", min_value=0.0, step=0.01, format="%.2f"),
        },
    )

    # Reconstrói o estado a partir da edição
    edited_df = edited_df.assign(Sinal=edited_df["Operação"].apply(lambda x: 1 if str(x).strip()=="+" else -1))
    _set_dataframe(edited_df)

     # Botões de ação abaixo da tabela
    b1, b2 = st.columns([1, 1])
    with b1:
        if st.button("↩️ Desfazer última", use_container_width=True):
            if st.session_state.entradas:
                st.session_state.entradas.pop()
                st.session_state.tabela_key += 1
                if hasattr(st, "toast"):
                    st.toast("Última entrada removida.")
                else:
                    st.success("Última entrada removida.")
                st.rerun()  # força a página a redesenhar já limpa
        
    with b2:
        if st.button("🧹 Limpar tudo", use_container_width=True):
            st.session_state.entradas = []
            st.session_state.tabela_key += 1
            if hasattr(st, "toast"):
                st.toast("Tabela zerada.")
            else:
                st.success("Tabela zerada.")
            st.rerun()  # força a página a redesenhar já limpa        
    
   # --------- Métricas ---------
    df_atual = _get_dataframe()
    total, cont_nf = _calc_totais(df_atual)

    m1, m2 = st.columns([1, 1.2])
    m1.metric("Quantidade de NF(s)", cont_nf)
    sub_total, sub_copy = m2.columns([2, 2])
    sub_total.metric("Total Peso Líquido (kg)", total)

    with sub_copy: # garante que o botão fique pequeno e à esquerda do número
        st.markdown("<div style='text-align:left'>", unsafe_allow_html=True)
        copy_button(str(total), tooltip="Copiar total (pt-BR)", copied_label="✅ Copiado!")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------- Resumo ---------
    st.success(
        f"Resultado do Peso Líquido da(s) Nota(s) Fiscal(is): **{total:.2f} kg** — Quantidade NF(s): **{cont_nf}**"
    )

# --------- Rodapé ---------
st.caption("Dica: verifique os dados antes de finalizar o registro.")













