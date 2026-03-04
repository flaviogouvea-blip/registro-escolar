import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Configuração da página para remover blocos brancos extras
st.set_page_config(page_title="SGE - Registro", layout="centered")

# CSS para garantir o visual limpo e idêntico à imagem de referência
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    /* Container do formulário */
    .main-form {
        background-color: white; 
        padding: 30px; 
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); 
        border: 1px solid #e0e0e0;
    }
    /* Estilo dos campos cinzas */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #f1f3f5 !important; 
        border: none !important; 
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# URL da sua planilha - VERIFIQUE SE O LINK É O QUE APARECE NO NAVEGADOR
URL_PLANILHA = "COLE_AQUI_O_LINK_DA_SUA_PLANILHA"

# Inicializa conexão
conn = st.connection("gsheets", type=GSheetsConnection)

st.write("Utilize o formulário abaixo para registrar incidentes ou observações.")

# Início do formulário em um único bloco
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
                # 1. Tenta ler a planilha
                # O parâmetro 'ttl=0' força o app a ler o dado mais atualizado
                df_existente = conn.read(spreadsheet=URL_PLANILHA, worksheet="Registros", ttl=0)
                
                # 2. Prepara o novo dado
                novo_dado = pd.DataFrame([{
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Aluno": aluno,
                    "Tipo": tipo,
                    "Turma": turma,
                    "Descricao": descricao
                }])
                
                # 3. Une os dados
                df_final = pd.concat([df_existente, novo_dado], ignore_index=True)
                
                # 4. Salva de volta
                conn.update(spreadsheet=URL_PLANILHA, worksheet="Registros", data=df_final)
                
                st.success("✅ Registro salvo com sucesso na Planilha!")
                st.balloons()
            except Exception as e:
                st.error("ERRO: A aba 'Registros' não foi encontrada ou o link está incorreto.")
                st.info("Verifique se o nome da aba na sua planilha é exatamente 'Registros' (com R maiúsculo).")
        else:
            st.warning("⚠️ Preencha o nome do aluno e a descrição.")
    
    st.markdown('</div>', unsafe_allow_html=True)
