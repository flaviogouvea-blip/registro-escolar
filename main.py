import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Estilo visual
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

st.title("SGE - Sistema de Gestão Escolar")
st.write("Utilize o formulário abaixo para registrar incidentes ou observações.")

# Nome do arquivo onde os dados serão salvos
ARQUIVO_DADOS = "registros.csv"

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
        if aluno and descricao:
            # Criar um novo dicionário com os dados
            novo_registro = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Aluno": aluno,
                "Turma": turma,
                "Tipo": tipo,
                "Descrição": descricao
            }
            
            # Converter para DataFrame
            df_novo = pd.DataFrame([novo_registro])
            
            # Salvar no CSV (se não existir, cria; se existir, adiciona no final)
            if not os.path.isfile(ARQUIVO_DADOS):
                df_novo.to_csv(ARQUIVO_DADOS, index=False, encoding='utf-8-sig')
            else:
                df_novo.to_csv(ARQUIVO_DADOS, mode='a', header=False, index=False, encoding='utf-8-sig')
            
            st.success(f"✅ Registro de {aluno} salvo com sucesso!")
        else:
            st.error("Por favor, preencha o nome do aluno e a descrição.")

# Área para visualizar/baixar os dados salvos
if os.path.isfile(ARQUIVO_DADOS):
    st.divider()
    df_exibir = pd.read_csv(ARQUIVO_DADOS)
    st.subheader("Registros Recentes")
    st.dataframe(df_exibir.tail(5)) # Mostra os últimos 5
    
    # Botão para baixar o arquivo completo
    csv_bytes = df_exibir.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button(
        label="📥 Baixar todos os registros (Excel/CSV)",
        data=csv_bytes,
        file_name=f"registros_sge_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
