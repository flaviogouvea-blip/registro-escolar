import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Configura a página para evitar blocos vazios e manter o foco no formulário
st.set_page_config(page_title="SGE - Registro", layout="centered")

# CSS para limpar o visual e seguir a imagem original
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-form {
        background-color: white; 
        padding: 30px; 
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); 
        border: 1px solid #e0e0e0;
    }
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #f1f3f5 !important; 
        border: none !important; 
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Seu link direto da planilha
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/12XFFeXFt3Lx8dLUeZFw3LbJKnZ29pEuFkgTT9lLuLBA/edit#gid=0"

# Inicializa a conexão
conn = st.connection("gsheets", type=GSheetsConnection)

st.write("Utilize o formulário abaixo para registrar incidentes ou observações.")

# Início do formulário único
with st.container():
    st.markdown('<div class="main-form">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        aluno = st.text_input("Nome do Aluno")
    with col2:
        tipo = st.selectbox("Tipo de Ocorrência", ["Indisciplina", "Atraso", "Falta de Material", "Elogio"])
    
    col3, _ = st.columns(2)
    with col3:
        turma = st.selectbox("Turma", ["6º Ano A", "6º Ano B", "7º Ano A"])
    
    descricao = st.text_area("Descrição do ocorrido", height=150)
    
    st.write("")
    if st.button("Salvar Registro", type="primary"):
        if aluno and descricao:
            try:
                # Tenta ler os dados da aba "Registros" (ttl=0 garante leitura em tempo real)
                df_existente = conn.read(spreadsheet=URL_PLANILHA, worksheet="Registros", ttl=0)
                
                # Prepara a nova linha
                novo_registro = pd.DataFrame([{
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Aluno": aluno,
                    "Tipo": tipo,
                    "Turma": turma,
                    "Descricao": descricao
                }])
                
                # Une e salva
                df_final = pd.concat([df_existente, novo_registro], ignore_index=True)
                conn.update(spreadsheet=URL_PLANILHA, worksheet="Registros", data=df_final)
                
                st.success("✅ Registro realizado com sucesso!")
                st.balloons()
            except Exception as e:
                st.error("ERRO: Certifique-se de que o nome da aba na planilha é exatamente 'Registros'.")
        else:
            st.warning("⚠️ Preencha o nome do aluno e a descrição.")
    
    st.markdown('</div>', unsafe_allow_html=True)
