import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Registro de Incidentes", layout="centered")

# --- CSS PARA REPRODUZIR O LAYOUT DA IMAGEM ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: white;
        padding: 40px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    label { font-weight: 500 !important; color: #444 !important; }
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #f1f3f5 !important;
        border: none !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Carregar dados dos alunos (de uma aba chamada 'Alunos')
try:
    df_alunos = conn.read(worksheet="Alunos")
except:
    df_alunos = pd.DataFrame({'NOME': ['Exemplo'], 'SERIE': ['6º Ano A']})

# --- INTERFACE ---
st.markdown("Utilize o formulário abaixo para registrar incidentes ou observações.")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        aluno_sel = st.text_input("Nome do Aluno")
    with col2:
        tipos = ["Indisciplina", "Falta de Material", "Atraso", "Elogio"]
        tipo_sel = st.selectbox("Tipo de Ocorrência", tipos)

    col3, _ = st.columns(2)
    with col3:
        series = sorted(df_alunos['SERIE'].unique())
        serie_sel = st.selectbox("Turma", series)
    
    relato = st.text_area("Descrição do ocorrido", height=150)

    st.write("")
    if st.button("Registrar Incidente", type="primary"):
        if aluno_sel and relato:
            # Criar nova linha de dados
            nova_linha = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Aluno": aluno_sel,
                "Tipo": tipo_sel,
                "Turma": serie_sel,
                "Descricao": relato
            }])
            
            # Adicionar à planilha (aba chamada 'Registros')
            dados_existentes = conn.read(worksheet="Registros")
            dados_atualizados = pd.concat([dados_existentes, nova_linha], ignore_index=True)
            conn.update(worksheet="Registros", data=dados_atualizados)
            
            st.success("✅ Incidente registrado com sucesso na planilha!")
            st.balloons()
        else:
            st.error("⚠️ Preencha o nome e a descrição.")
