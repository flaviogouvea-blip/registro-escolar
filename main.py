import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Limpa o layout para remover os blocos brancos vazios
st.set_page_config(page_title="SGE - Registro", layout="centered")

# Estilização para ficar idêntico à sua imagem de referência
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-form {
        background-color: white; padding: 30px; border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;
    }
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #f1f3f5 !important; border: none !important; border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# URL da sua planilha (Use o link da barra de endereços do navegador)
URL_PLANILHA = "COLE_AQUI_O_LINK_DA_SUA_PLANILHA"

# Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

st.write("Utilize o formulário abaixo para registrar incidentes ou observações.")

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
                # Tenta gravar diretamente
                novo_registro = pd.DataFrame([{
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Aluno": aluno,
                    "Tipo": tipo,
                    "Turma": turma,
                    "Descricao": descricao
                }])
                
                # Lê os dados atuais (ttl=0 evita que o app use dados antigos do "cache")
                existente = conn.read(spreadsheet=URL_PLANILHA, worksheet="Registros", ttl=0)
                df_final = pd.concat([existente, novo_registro], ignore_index=True)
                
                # Grava na planilha
                conn.update(spreadsheet=URL_PLANILHA, worksheet="Registros", data=df_final)
                
                st.success("✅ Sucesso! Ocorrência registrada.")
                st.balloons()
            except Exception as e:
                st.error(f"Erro técnico: {e}")
                st.info("Verifique se a planilha está aberta para 'Qualquer pessoa com link' como EDITOR.")
        else:
            st.warning("⚠️ Preencha o nome do aluno e a descrição.")
    st.markdown('</div>', unsafe_allow_html=True)
