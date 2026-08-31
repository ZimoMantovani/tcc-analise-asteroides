import streamlit as st
import pandas as pd
from sqlalchemy import text
import os

# Importa as funções do seu ETL para o botão funcionar
from etl_completo import extrair_dados_nasa, transformar_dados, carregar_no_banco
from database import get_engine


@st.cache_resource
def get_database_connection():
    """Retorna a engine compartilhada (cacheada pelo Streamlit para esta sessão)."""
    try:
        return get_engine()
    except Exception as e:
        st.error(f"Erro ao conectar no banco: {e}")
        return None


@st.cache_data(ttl=300)
def carregar_asteroides():
    """Carrega asteroides do banco de dados ordenados pela aproximação"""
    engine = get_database_connection()

    if engine is None:
        raise Exception("Conexão com banco falhou ou variáveis de ambiente ausentes")

    query = text("SELECT * FROM asteroides ORDER BY data_aproximacao")
    df = pd.read_sql(query, engine.connect())

    if df.empty:
        raise Exception("Nenhum dado encontrado no banco")

    return df


def render_sidebar():
    """Renderiza a barra lateral padrão para todas as páginas."""

    # 1. Esconde o menu nativo do Streamlit
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # --- BLOCO 1: LOGO E TÍTULOS ---
        st.image("https://www.nasa.gov/wp-content/uploads/2023/03/nasa-logo-web-rgb.png", width=200)
        st.markdown("### 🌍 NEO Monitor")
        st.markdown("**Near Earth Objects**")
        st.markdown("---")

        # --- BLOCO 2: LINKS DE NAVEGAÇÃO ---
        st.caption("Navegação")
        st.page_link("app.py", label="Home")
        st.page_link("pages/2_Estatisticas.py", label="Estatisticas")
        st.page_link("pages/3_Explorador.py", label="Explorador")
        st.page_link("pages/4_Analise_Riscos.py", label="Analise de Riscos")
        st.page_link("pages/5_Sobre.py", label="Sobre")
        st.markdown("---")

        # --- BLOCO 3: BOTÃO DE ATUALIZAÇÃO (ETL) ---
        if st.button("Atualizar Dados", use_container_width=True):
            with st.spinner("Buscando dados na NASA..."):
                dados_brutos = extrair_dados_nasa(dias=7)
                if dados_brutos:
                    df_novos = transformar_dados(dados_brutos)
                    if not df_novos.empty:
                        sucesso = carregar_no_banco(df_novos)
                        if sucesso:
                            carregar_asteroides.clear()
                            st.success("✅ Dados atualizados com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao salvar no banco de dados.")
                    else:
                        st.warning("⚠️ A API não retornou novos asteroides.")
                else:
                    st.error("❌ Falha na conexão com a NASA.")

        st.markdown("---")

        # --- BLOCO 4: STATUS DO SISTEMA E DIAGNÓSTICO ---
        st.caption("**Status do Sistema:**")

        try:
            with st.spinner("Verificando..."):
                df_status = carregar_asteroides()

            ultima_coleta = pd.to_datetime(df_status['data_coleta'].max()).strftime('%d/%m %H:%M')
            st.markdown(
                "<div style=\""
                "font-family: 'JetBrains Mono', monospace; "
                "font-size: 0.78rem; "
                "color: #00F0FF; "
                "letter-spacing: 0.03em;"
                "\">"
                f"● SISTEMA ONLINE // {len(df_status)} OBJETOS // ATUALIZADO {ultima_coleta}"
                "</div>",
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.markdown(
                "<div style=\""
                "font-family: 'JetBrains Mono', monospace; "
                "font-size: 0.78rem; "
                "color: #FF2A5F; "
                "letter-spacing: 0.03em;"
                "\">● SISTEMA OFFLINE // ERRO DE CONEXÃO</div>",
                unsafe_allow_html=True,
            )
            st.caption(f"Detalhes: {str(e)[:50]}...")

            if st.button("Diagnóstico", key="diagnostico"):
                st.write("**Checklist:**")

                engine = get_database_connection()
                if engine:
                    st.write("✅ PostgreSQL: Conectado")
                else:
                    st.write("❌ PostgreSQL: Falha na conexão")

                try:
                    result = pd.read_sql("SELECT COUNT(*) FROM asteroides", engine)
                    st.write(f"✅ Tabela 'asteroides': {result.iloc[0, 0]} registros")
                except Exception:
                    st.write("❌ Tabela 'asteroides': Não existe ou está vazia")

                # 🔒 Removido: antes exibia os 3 primeiros caracteres da senha.
                # Nunca exponha nem um fragmento de credencial numa interface pública.
                if os.getenv('DB_PASSWORD'):
                    st.write("✅ Senha carregada")
                else:
                    st.write("❌ Senha: Não encontrada no .env")