import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Estilo visual idêntico à imagem
st.set_page_config(page_title="SGE - Registro", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: white; padding: 40px; border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;
    }
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #f1f3f5 !important; border: none !important; border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.write("Utilize o formulário abaixo para registrar incidentes ou observações.")

# Formulário
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        aluno = st.text_input("Nome do Aluno")
    with c2:
        tipo = st.selectbox("Tipo de Ocorrência", ["Indisciplina", "Atraso", "Falta de Material"])
    
    turma = st.selectbox("Turma", ["6º Ano A", "6º Ano B", "7º Ano A"])
    descricao = st.text_area("Descrição do ocorrido", height=150)
    
    if st.button("Salvar Registro"):
        st.success(f"Registrado: {aluno} - {turma}")
