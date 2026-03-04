import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime
import io  # Necessário para o download do Excel

st.set_page_config(page_title="Sistema de Ocorrências", layout="wide")

# --- CARREGAMENTO DOS DADOS (Excel -> App) ---
@st.cache_data
def carregar_dados():
    try:
        # Lendo sem cabeçalho (A1 já é dado)
        df_a = pd.read_excel("alunos.xlsx", header=None)
        df_p = pd.read_excel("professores.xlsx", header=None)
        
        df_a.columns = ['NOME', 'SERIE']
        df_p.columns = ['PROFESSOR']
        
        df_a['NOME'] = df_a['NOME'].astype(str).str.strip()
        df_a['SERIE'] = df_a['SERIE'].astype(str).str.strip()
        df_p['PROFESSOR'] = df_p['PROFESSOR'].astype(str).str.strip()
        
        return df_a, df_p
    except Exception as e:
        st.error(f"Erro ao ler arquivos: {e}")
        return None, None

# --- BANCO DE DADOS (App -> Armazenamento) ---
def salvar_registro(prof, serie, aluno, tipo, relato):
    conn = sqlite3.connect('banco_escola.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS registros 
                 (data TEXT, prof TEXT, serie TEXT, aluno TEXT, tipo TEXT, relato TEXT)''')
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    c.execute("INSERT INTO registros VALUES (?,?,?,?,?,?)", (agora, prof, serie, aluno, tipo, relato))
    conn.commit()
    conn.close()

# --- INTERFACE PRINCIPAL ---
st.title("📝 Registro de Ocorrências Escolar")

df_alunos, df_profs = carregar_dados()

if df_alunos is not None:
    # 1. SELEÇÃO DO PROFESSOR
    st.subheader("1. Selecione o Professor")
    profs_lista = sorted(df_profs['PROFESSOR'].unique())
    professor_sel = st.selectbox("Quem está registrando?", [""] + profs_lista)

    if professor_sel:
        st.divider()
        # 2. BOTÕES DE SÉRIE
        st.subheader("2. Selecione a Série")
        series_lista = sorted(df_alunos['SERIE'].unique())
        serie_sel = st.radio("Turmas:", series_lista, horizontal=True)

        if serie_sel:
            st.divider()
            # 3. SELEÇÃO DO ALUNO
            st.subheader(f"3. Alunos da {serie_sel}")
            alunos_filtrados = sorted(df_alunos[df_alunos['SERIE'] == serie_sel]['NOME'].tolist())
            aluno_sel = st.selectbox("Nome do Aluno:", [""] + alunos_filtrados)

            if aluno_sel:
                st.divider()
                # 4. TIPO E RELATO
                st.subheader("4. Detalhes")
                c1, c2 = st.columns([1, 2])
                with c1:
                    tipos = ["Indisciplina", "Falta de Material", "Elogio", "Tarefa Incompleta", "Atraso"]
                    tipo_sel = st.radio("Tipo:", tipos)
                with c2:
                    relato = st.text_area("O que aconteceu?")
                    if st.button("💾 SALVAR REGISTRO", use_container_width=True):
                        if relato:
                            salvar_registro(professor_sel, serie_sel, aluno_sel, tipo_sel, relato)
                            st.success(f"Ocorrência de {aluno_sel} salva!")
                            st.balloons()
                        else:
                            st.error("Descreva o relato.")

# --- BARRA LATERAL (HISTÓRICO E EXPORTAÇÃO) ---
st.sidebar.title("📊 Gestão de Dados")

if st.sidebar.checkbox("Ver Histórico de Registros"):
    if os.path.exists('banco_escola.db'):
        conn = sqlite3.connect('banco_escola.db')
        df_historico = pd.read_sql_query("SELECT * FROM registros", conn)
        conn.close()

        if not df_historico.empty:
            st.sidebar.write("Registros encontrados:")
            st.sidebar.dataframe(df_historico)

            # --- BOTÃO DE EXPORTAR PARA EXCEL ---
            # Prepara o arquivo Excel na memória
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_historico.to_excel(writer, index=False, sheet_name='Ocorrências')
            
            # Cria o botão de download
            st.sidebar.download_button(
                label="📥 Baixar Relatório em Excel",
                data=output.getvalue(),
                file_name=f"relatorio_ocorrencias_{datetime.now().strftime('%d_%m_%Y')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.sidebar.info("Ainda não há ocorrências registradas.")