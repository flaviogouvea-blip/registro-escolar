import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configuração da Página
st.set_page_config(page_title="SGE - Registro", layout="centered")

# 2. Estilo Visual (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-form { background-color: white; padding: 30px; border-radius: 10px; border: 1px solid #e0e0e0; }
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #f1f3f5 !important; border: none !important; border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Seu link da planilha (Já inserido abaixo)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/12XFFeXFt3Lx8dLUeZFw3LbJKnZ29pEuFkgTT9lLuLBA/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

st.write("Utilize o formulário abaixo para registrar incidentes ou observações.")

with st.container():
    st.markdown('<div class="main-form">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        aluno = st.text_input("Nome do Aluno")
    with col2:
        tipo = st.selectbox("Tipo de Ocorrência", ["Indisciplina", "Atraso", "Falta de Material", "Elogio"])
    
    turma = st.selectbox("Turma", ["6º Ano A", "6º Ano B", "7º Ano A"])
    descricao = st.text_area("Descrição do ocorrido", height=150)
    
    if st.button("Salvar Registro", type="primary"):
        if aluno and descricao:
            try:
                # Tenta ler a aba 'Registros'
                df_existente = conn.read(spreadsheet=URL_PLANILHA, worksheet="Registros", ttl=0)
                
                novo_registro = pd.DataFrame([{
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Aluno": aluno,
                    "Tipo": tipo,
                    "Turma": turma,
                    "Descricao": descricao
                }])
                
                df_final = pd.concat([df_existente, novo_registro], ignore_index=True)
                conn.update(spreadsheet=URL_PLANILHA, worksheet="Registros", data=df_final)
                
                st.success("✅ Registro realizado com sucesso!")
                st.balloons()
            except Exception as e:
                st.error("Erro: Verifique se o nome da aba na sua planilha é 'Registros' e se o acesso está como EDITOR.")
        else:
            st.warning("⚠️ Preencha o nome do aluno e a descrição.")
    st.markdown('</div>', unsafe_allow_html=True)
