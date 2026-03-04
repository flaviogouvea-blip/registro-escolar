import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Estilo visual idêntico à imagem
st.set_page_config(page_title="Registro de Incidentes", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: white; padding: 30px; border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;
    }
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #f1f3f5 !important; border: none !important; border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- COLOQUE O LINK DA SUA PLANILHA AQUI EMBAIXO ---
URL_PLANILHA = "COLE_AQUI_O_LINK_DA_SUA_PLANILHA"

# Conexão direta
conn = st.connection("gsheets", type=GSheetsConnection)

st.write("Utilize o formulário abaixo para registrar incidentes ou observações.")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        aluno = st.text_input("Nome do Aluno")
    with col2:
        tipo = st.selectbox("Tipo de Ocorrência", ["Indisciplina", "Atraso", "Falta de Material", "Elogio"])
    
    turma = st.selectbox("Turma", ["6º Ano A", "6º Ano B", "7º Ano A"])
    descricao = st.text_area("Descrição do ocorrido", height=150)

    st.write("")
    if st.button("Salvar Registro", type="primary"):
        if aluno and descricao:
            try:
                # Lê os dados atuais
                df_existente = conn.read(spreadsheet=URL_PLANILHA, worksheet="Registros")
                
                # Cria a nova linha
                nova_linha = pd.DataFrame([{
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Aluno": aluno,
                    "Tipo": tipo,
                    "Turma": turma,
                    "Descricao": descricao
                }])
                
                # Junta e atualiza
                df_atualizado = pd.concat([df_existente, nova_linha], ignore_index=True)
                conn.update(spreadsheet=URL_PLANILHA, worksheet="Registros", data=df_atualizado)
                
                st.success("✅ Sucesso! Ocorrência registrada na planilha.")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar: Verifique se o link da planilha está correto e se a aba se chama 'Registros'.")
        else:
            st.warning("⚠️ Preencha o nome do aluno e a descrição.")
