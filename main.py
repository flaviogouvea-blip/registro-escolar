import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Configuração da página para remover blocos vazios
st.set_page_config(page_title="SGE - Registro", layout="centered")

# CSS para manter o visual limpo da imagem
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-container {
        background-color: white; padding: 30px; border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;
    }
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #f1f3f5 !important; border: none !important; border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# URL da sua planilha (Substitua pelo seu link real)
URL_PLANILHA = "COLE_AQUI_O_LINK_DA_SUA_PLANILHA"

# Inicializa conexão
conn = st.connection("gsheets", type=GSheetsConnection)

st.write("Utilize o formulário abaixo para registrar incidentes ou observações.")

# Início do formulário dentro de um container branco
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        aluno = st.text_input("Nome do Aluno")
    with col2:
        tipo = st.selectbox("Tipo de Ocorrência", ["Indisciplina", "Atraso", "Falta de Material", "Elogio"])
    
    # Campo de Turma ocupando metade da largura como na imagem
    col3, _ = st.columns(2)
    with col3:
        turma = st.selectbox("Turma", ["6º Ano A", "6º Ano B", "7º Ano A"])
    
    descricao = st.text_area("Descrição do ocorrido", height=150)
    
    st.write("")
    if st.button("Salvar Registro", type="primary"):
        if aluno and descricao:
            try:
                # Criar nova linha de dados
                novo_registro = pd.DataFrame([{
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Aluno": aluno,
                    "Tipo": tipo,
                    "Turma": turma,
                    "Descricao": descricao
                }])
                
                # Tenta ler dados existentes para anexar (ou cria novo se estiver vazio)
                try:
                    existente = conn.read(spreadsheet=URL_PLANILHA, worksheet="Registros")
                    df_final = pd.concat([existente, novo_registro], ignore_index=True)
                except:
                    df_final = novo_registro
                
                # Atualiza a planilha
                conn.update(spreadsheet=URL_PLANILHA, worksheet="Registros", data=df_final)
                
                st.success("✅ Registro salvo com sucesso!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar: Verifique se a aba se chama 'Registros' e o link está correto.")
        else:
            st.warning("⚠️ Preencha o nome do aluno e a descrição.")
            
    st.markdown('</div>', unsafe_allow_html=True)
