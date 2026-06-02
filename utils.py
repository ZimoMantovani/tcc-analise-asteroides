import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def get_database_connection():
    """Cria conexão com PostgreSQL"""
    try:
        usuario = "postgres"
        senha = os.getenv('DB_PASSWORD')
        connection_string = f"postgresql://{usuario}:{quote_plus(senha)}@localhost:5432/tcc_asteroides?client_encoding=utf8"
        engine = create_engine(connection_string, connect_args={'client_encoding': 'utf8'})
        
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        return engine
    except Exception as e:
        st.error(f"Erro ao conectar no banco: {e}")
        return None

@st.cache_data(ttl=300)
def carregar_asteroides():
    """Carrega asteroides do banco de dados"""
    engine = get_database_connection()
    
    if engine is None:
        raise Exception("Conexão com banco falhou")
    
    query = text("SELECT * FROM asteroides ORDER BY data_aproximacao")
    df = pd.read_sql(query, engine.connect())
    
    if df.empty:
        raise Exception("Nenhum dado encontrado no banco")
    
    return df

def render_sidebar():
    """Renderiza a barra lateral padrão para todas as páginas."""
    with st.sidebar:
        st.image("https://www.nasa.gov/wp-content/uploads/2023/03/nasa-logo-web-rgb.png", width=200)
        st.title("🌍 NEO Monitor")
        st.markdown("**Near Earth Objects**")
        
        st.divider()
        
        if st.button("🔄 Atualizar Dados", width='stretch'):
            with st.spinner("Baixando dados..."):
                env = os.environ.copy()
                env["PYTHONIOENCODING"] = "utf-8"
                
                resultado = subprocess.run([sys.executable, "etl_completo.py"], capture_output=True, text=True, encoding="utf-8", env=env)
                if resultado.returncode != 0:
                    st.error("❌ Falha ao atualizar dados!")
                    st.code(resultado.stderr)
                    st.stop()
            st.cache_data.clear()
            st.rerun()
        
        st.divider()
        st.caption("**Status do Sistema:**")
        
        try:
            with st.spinner("Verificando..."):
                df_status = carregar_asteroides()
                st.success(f"✅ {len(df_status)} asteroides")
                ultima_coleta = pd.to_datetime(df_status['data_coleta'].max()).strftime('%d/%m/%Y %H:%M:%S')
                st.caption(f"🕐 Última coleta: {ultima_coleta}")
                
        except Exception as e:
            st.error("❌ Erro de conexão")
            st.caption(f"Detalhes: {str(e)[:50]}...")
            
            if st.button("🔍 Diagnóstico", key="diagnostico"):
                st.write("**Checklist:**")
                try:
                    engine = get_database_connection()
                    if engine:
                        st.write("✅ PostgreSQL: Conectado")
                    else:
                        st.write("❌ PostgreSQL: Falha na conexão")
                except:
                    st.write("❌ PostgreSQL: Não está rodando")
                
                try:
                    engine = get_database_connection()
                    result = pd.read_sql("SELECT COUNT(*) FROM asteroides", engine)
                    st.write(f"✅ Tabela 'asteroides': {result.iloc[0,0]} registros")
                except:
                    st.write("❌ Tabela 'asteroides': Não existe ou está vazia")
                
                senha_env = os.getenv('DB_PASSWORD')
                if senha_env:
                    st.write(f"✅ Senha carregada: {senha_env[:3]}***")
                else:
                    st.write("❌ Senha: Não encontrada no .env")
