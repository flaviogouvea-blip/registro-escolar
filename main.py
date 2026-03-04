import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Estilo visual da imagem
st.set_page_config(page_title="SGE - Registro", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: white; padding: 40px; border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;
    }
    label { font-weight: 500; color: #444; }
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #f1f3f5 !important; border: none !important; border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Conexão com a Planilha
conn = st.connection("gsheets", type=GSheetsConnection)

st.write("Utilize o formulário abaixo para registrar incidentes ou observações.")

with st.container():
    c1, c2 = st.columns(2)
    with c1:
        aluno_sel = st.text_input("Nome do Aluno")
    with c2:
        tipo_sel = st.selectbox("Tipo de Ocorrência", ["Indisciplina", "Atraso", "Elogio", "Tarefa Incompleta"])
    
    turma_sel = st.selectbox("Turma", ["6º Ano A", "6º Ano B", "7º Ano A"])
    relato = st.text_area("Descrição do ocorrido", height=150)
    
    if st.button("Salvar Registro", type="primary"):
        if aluno_sel and relato:
            # Lógica para salvar na planilha
            df_existente = conn.read(worksheet="Registros")
            novo_dado = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Aluno": aluno_sel,
                "Tipo": tipo_sel,
                "Turma": turma_sel,
                "Descricao": relato
            }])
            df_final = pd.concat([df_existente, novo_dado], ignore_index=True)
            conn.update(worksheet="Registros", data=df_final)
            
            st.success("✅ Registrado com sucesso na Planilha Google!")
            st.balloons()
