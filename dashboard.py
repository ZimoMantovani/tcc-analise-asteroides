import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
import numpy as np
# Importar módulo de análise
from analise_riscos import AnalisadorRiscos

load_dotenv()

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="NEO Monitor - Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== FUNÇÕES AUXILIARES (DEFINIR ANTES DE USAR!) ==========
@st.cache_resource
def get_database_connection():
    """Cria conexão com PostgreSQL"""
    try:
        usuario = "postgres"
        senha = os.getenv('DB_PASSWORD')
        connection_string = f"postgresql://{usuario}:{quote_plus(senha)}@localhost:5432/tcc_asteroides?client_encoding=utf8"
        engine = create_engine(connection_string, connect_args={'client_encoding': 'utf8'})
        
        # Testar conexão
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

# ========== SIDEBAR ==========
with st.sidebar:
    st.image("https://www.nasa.gov/wp-content/uploads/2023/03/nasa-logo-web-rgb.png", width=200)
    st.title("🌍 NEO Monitor")
    st.markdown("**Near Earth Objects**")
    
    st.divider()
    
    # Menu de navegação
    pagina = st.radio(
        "Navegação:",
        ["🏠 Home", "📊 Estatísticas", "🔍 Explorador", "⚠️ Análise de Riscos", "ℹ️ Sobre"]
    )
    
    st.divider()
    
    # Botão de atualização
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        with st.spinner("Baixando dados..."):
            import subprocess
            # Roda o arquivo ETL_Completo.py
            subprocess.run(["Python","etl_completo.py"])
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    # Status do Sistema 
    st.caption("**Status do Sistema:**")
    
    try:
        with st.spinner("Verificando..."):
            df_status = carregar_asteroides()
            st.success(f"✅ {len(df_status)} asteroides")
            st.caption(f"🕐 Última atualização: {pd.Timestamp.now().strftime('%H:%M:%S')}")
            
    except Exception as e:
        st.error("❌ Erro de conexão")
        st.caption(f"Detalhes: {str(e)[:50]}...")
        
        # Botão de diagnóstico
        if st.button("🔍 Diagnóstico", key="diagnostico"):
            st.write("**Checklist:**")
            
            # 1. PostgreSQL rodando?
            try:
                engine = get_database_connection()
                if engine:
                    st.write("✅ PostgreSQL: Conectado")
                else:
                    st.write("❌ PostgreSQL: Falha na conexão")
            except:
                st.write("❌ PostgreSQL: Não está rodando")
            
            # 2. Tabela existe?
            try:
                engine = get_database_connection()
                result = pd.read_sql("SELECT COUNT(*) FROM asteroides", engine)
                st.write(f"✅ Tabela 'asteroides': {result.iloc[0,0]} registros")
            except:
                st.write("❌ Tabela 'asteroides': Não existe ou está vazia")
            
            # 3. Credenciais corretas?
            senha_env = os.getenv('DB_PASSWORD')
            if senha_env:
                st.write(f"✅ Senha carregada: {senha_env[:3]}***")
            else:
                st.write("❌ Senha: Não encontrada no .env")

# ========== CARREGAR DADOS ==========
try:
    df = carregar_asteroides()
except Exception as e:
    st.warning("⚠️ Banco de dados vazio ou desatualizado. Iniciando primeira coleta...")
    
    with st.spinner("Executando ETL Completo (Isso pode levar de 10 a 30 segundos)..."):
        import subprocess
        # O capture_output ajuda a esconder os prints do ETL do terminal principal
        resultado = subprocess.run(["python", "etl_completo.py"], capture_output=True, text=True)
        
        if resultado.returncode == 0:
            st.success("✅ Coleta finalizada com sucesso! Inicializando painel...")
            st.rerun() # Recarrega a página agora com o banco cheio
        else:
            st.error("❌ Erro ao tentar baixar os dados automaticamente.")
            st.code(resultado.stderr) # Mostra o erro exato na tela
            st.stop()

# ========== PÁGINAS ==========

if pagina == "🏠 Home":
    st.title("🌍 Painel de Monitoramento de Asteroides")
    st.markdown("### Sistema de Análise de Objetos Próximos à Terra (NEOs)")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total de NEOs", len(df))
    
    with col2:
        perigosos = len(df[df['perigoso'] == True])
        st.metric("🚨 Perigosos", perigosos, delta=f"{perigosos/len(df)*100:.1f}%")
    
    with col3:
        st.metric("📏 Maior", f"{df['diametro_max_km'].max():.2f} km")
    
    with col4:
        st.metric("⚡ Mais Rápido", f"{df['velocidade_kmh'].max():,.0f} km/h")
    
    st.divider()
    
    # Gráfico de pizza: Perigosos vs Seguros
    col_esq, col_dir = st.columns(2)
    
    with col_esq:
        st.subheader("📊 Classificação de Periculosidade")
        contagem = df['perigoso'].value_counts()
        fig_pizza = px.pie(
            values=contagem.values,
            names=['Seguro', 'Perigoso'],
            color_discrete_sequence=['#00cc66', '#ff4444']
        )
        st.plotly_chart(fig_pizza, use_container_width=True)
    
    with col_dir:
        st.subheader("🏆 Top 5 Maiores Asteroides")
        top5 = df.nlargest(5, 'diametro_max_km')[['nome', 'diametro_max_km', 'perigoso']]
        for idx, row in top5.iterrows():
            icone = "🚨" if row['perigoso'] else "✅"
            st.write(f"{icone} **{row['nome']}** - {row['diametro_max_km']:.3f} km")
    
    st.divider()
    
    # Próximas aproximações
    st.subheader("📅 Próximas Aproximações (7 dias)")
    proximos = df.head(10)[['nome', 'data_aproximacao', 'distancia_lunar', 'perigoso']]
    st.dataframe(proximos, use_container_width=True, hide_index=True)

elif pagina == "📊 Estatísticas":
    st.title("📊 Estatísticas Detalhadas")
    
    tab1, tab2, tab3 = st.tabs(["Tamanhos", "Velocidades", "Distâncias"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig_hist = px.histogram(df, x='diametro_max_km', nbins=30, title="Distribuição de Tamanhos")
            st.plotly_chart(fig_hist, use_container_width=True)
        with col2:
            top10 = df.nlargest(10, 'diametro_max_km')
            fig_bar = px.bar(top10, x='nome', y='diametro_max_km', color='perigoso', title="Top 10 Maiores")
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab2:
        fig_scatter = px.scatter(df, x='diametro_max_km', y='velocidade_kmh', color='perigoso',
                                 title="Tamanho vs Velocidade", hover_data=['nome'])
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with tab3:
        fig_box = px.box(df, x='perigoso', y='distancia_lunar', color='perigoso',
                         title="Distribuição de Distâncias")
        st.plotly_chart(fig_box, use_container_width=True)

elif pagina == "🔍 Explorador":
    st.title("🔍 Explorador de Asteroides")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_perigoso = st.selectbox("Tipo:", ["Todos", "Perigosos", "Seguros"])
    with col2:
        tamanho_min = st.number_input("Diâmetro mín (km):", value=0.0, step=0.01)
    with col3:
        velocidade_min = st.number_input("Velocidade mín (km/h):", value=0.0, step=1000.0)
    
    # Aplicar filtros
    df_filtrado = df.copy()
    if filtro_perigoso == "Perigosos":
        df_filtrado = df_filtrado[df_filtrado['perigoso'] == True]
    elif filtro_perigoso == "Seguros":
        df_filtrado = df_filtrado[df_filtrado['perigoso'] == False]
    
    df_filtrado = df_filtrado[
        (df_filtrado['diametro_max_km'] >= tamanho_min) &
        (df_filtrado['velocidade_kmh'] >= velocidade_min)
    ]
    
    st.write(f"**{len(df_filtrado)} asteroides encontrados**")
    st.dataframe(df_filtrado[['nome', 'data_aproximacao', 'diametro_max_km', 'velocidade_kmh', 'distancia_lunar', 'perigoso']], 
                 use_container_width=True, height=500)

elif pagina == "⚠️ Análise de Riscos":
    st.title("Análise de Riscos dos Asteroides")
    
    # Gerar análise completa
    with st.spinner("Analisando riscos..."):
        df_riscos = AnalisadorRiscos.gerar_relatorio_completo(df.drop_duplicates(subset=['nome']))
        
        # Juntar dados Originais
        df_completo = df.merge(
            df_riscos[['nome', 'energia_megatons', 'raio_destruicao_km', 'indice_risco', 'nivel_indice', 'cor_indice', 'classificacao']],
            on='nome',
            how='left'
        )
    
    # ========== MÉTRICAS GERAIS ==========
    st.subheader("📊 Panorama Geral de Riscos")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        risco_alto = len(df_completo[df_completo['indice_risco'] >= 60])
        st.metric("🔴 Alto Risco", risco_alto, delta=f"{risco_alto/len(df)*100:.1f}%")
    
    with col2:
        energia_max = df_riscos['energia_megatons'].max()
        st.metric("💥 Maior Energia", f"{energia_max:.2f} MT")
    
    with col3:
        raio_max = df_riscos['raio_destruicao_km'].max()
        st.metric("📏 Maior Raio", f"{raio_max:.1f} km")
    
    with col4:
        indice_medio = df_riscos['indice_risco'].mean()
        st.metric("📈 Índice Médio", f"{indice_medio:.1f}/100")
    
    st.divider()
    
    # ========== DISTRIBUIÇÃO DE RISCOS ==========
    st.subheader("📊 Distribuição por Categoria de Risco")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de pizza - Níveis de risco
        contagem_niveis = df_riscos['nivel_indice'].value_counts()
        fig_pizza = px.pie(
            values=contagem_niveis.values,
            names=contagem_niveis.index,
            title="Distribuição por Nível de Risco",
            color_discrete_sequence=['#00ff00', '#88ff00', '#ffff00', '#ff8800', '#ff0000']
        )
        st.plotly_chart(fig_pizza, use_container_width=True)
    
    with col2:
        # Gráfico de barras - Categorias
        categorias = df_completo['classificacao'].apply(lambda x: x['categoria']).value_counts()
        fig_bar = px.bar(
            x=categorias.index,
            y=categorias.values,
            title="Distribuição por Categoria de Impacto",
            labels={'x': 'Categoria', 'y': 'Quantidade'},
            color=categorias.values,
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.divider()
    
    # ========== ESCALA DE IMPACTOS ==========
    st.subheader("📏 Escala de Severidade de Impactos")
    
    # Criar tabela de categorias
    categorias_info = []
    for size in [0.010, 0.050, 0.300, 2.0, 10.0]:
        info = AnalisadorRiscos.classificar_por_tamanho(size)
        categorias_info.append({
            'Diâmetro': f"~{size*1000:.0f}m",
            'Categoria': info['categoria'],
            'Nível': info['nivel_risco'],
            'Dano': info['dano_potencial'],
            'Área Afetada': info['area_afetada'],
            'Frequência': info['frequencia'],
            'Exemplo': info['exemplo_historico']
        })
    
    df_categorias = pd.DataFrame(categorias_info)
    st.dataframe(df_categorias, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # ========== TOP 10 MAIS PERIGOSOS ==========
    st.subheader("🚨 Top 10 Asteroides Mais Perigosos")
    
    top_perigosos = df_completo.nlargest(10, 'indice_risco')[
        ['nome', 'indice_risco', 'nivel_indice', 'diametro_max_km', 'energia_megatons', 'raio_destruicao_km', 'distancia_lunar']
    ].copy()
    
    # Formatar valores
    top_perigosos['diametro_max_km'] = top_perigosos['diametro_max_km'].apply(lambda x: f"{x:.3f}")
    top_perigosos['energia_megatons'] = top_perigosos['energia_megatons'].apply(lambda x: f"{x:.2f}")
    top_perigosos['raio_destruicao_km'] = top_perigosos['raio_destruicao_km'].apply(lambda x: f"{x:.1f}")
    top_perigosos['distancia_lunar'] = top_perigosos['distancia_lunar'].apply(lambda x: f"{x:.2f}")
    
    # Renomear colunas
    top_perigosos.columns = ['Nome', 'Índice de Risco', 'Nível', 'Diâmetro (km)', 'Energia (MT)', 'Raio Dest. (km)', 'Distância (Luas)']
    
    st.dataframe(
        top_perigosos,
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    
    # ========== DETALHES DE UM ASTEROIDE ==========
    st.subheader("🔍 Análise Detalhada de Asteroide")
    
    asteroide_selecionado = st.selectbox(
        "Selecione um asteroide:",
        options=df_completo['nome'].tolist()
    )
    
    if asteroide_selecionado:
        dados = df_completo[df_completo['nome'] == asteroide_selecionado].iloc[0]
        classificacao = dados['classificacao']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {dados['nome']}")
            st.markdown(f"**Índice de Risco:** {dados['indice_risco']:.1f}/100")
            st.markdown(f"**Nível:** {dados['nivel_indice']}")
            st.markdown(f"**Categoria:** {classificacao['categoria']}")
            st.markdown(f"**Perigoso (NASA):** {'🚨 SIM' if dados['perigoso'] else '✅ NÃO'}")
            
        with col2:
            st.markdown("### Características Físicas")
            st.markdown(f"**Diâmetro:** {dados['diametro_max_km']:.3f} km ({dados['diametro_max_km']*1000:.0f} metros)")
            st.markdown(f"**Velocidade:** {dados['velocidade_kmh']:,.0f} km/h")
            st.markdown(f"**Distância:** {dados['distancia_lunar']:.2f} distâncias lunares")
        
        st.divider()
        
        # Análise de impacto
        st.markdown("### 💥 Cenário de Impacto Hipotético")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Energia de Impacto", f"{dados['energia_megatons']:.2f} MT")
            
            # Comparação
            analise = AnalisadorRiscos.analisar_asteroide(dados)
            st.caption(analise['comparacao_energia'])
        
        with col2:
            st.metric("Raio de Destruição", f"{dados['raio_destruicao_km']:.1f} km")
            area_km2 = np.pi * (dados['raio_destruicao_km'] ** 2)
            st.caption(f"Área afetada: ~{area_km2:,.0f} km²")
        
        with col3:
            st.metric("Dano Potencial", classificacao['nivel_risco'])
            st.caption(classificacao['dano_potencial'])
        
        # Aviso importante
        st.warning(f"""
        ⚠️ **Importante:** Este é um cenário HIPOTÉTICO baseado em cálculos físicos. 
        A probabilidade real de impacto é **extremamente baixa** para a maioria dos asteroides monitorados.
        
        📏 **Distância atual:** {dados['distancia_lunar']:.2f} distâncias lunares 
        (~ {dados['distancia_km']:,.0f} km da Terra)
        """)
        
        # Frequência de eventos
        st.info(f"""
        📊 **Frequência estatística de eventos deste tipo:**  
        {classificacao['frequencia']}
        
        📖 **Exemplo histórico:** {classificacao['exemplo_historico']}
        """)
    
    st.divider()
    
    # ========== GRÁFICO: RISCO vs TAMANHO ==========
    st.subheader("📈 Relação: Índice de Risco vs Tamanho")
    
    fig_scatter = px.scatter(
        df_completo,
        x='diametro_max_km',
        y='indice_risco',
        color='nivel_indice',
        size='energia_megatons',
        hover_data=['nome', 'distancia_lunar', 'velocidade_kmh'],
        title="Índice de Risco vs Diâmetro do Asteroide",
        labels={
            'diametro_max_km': 'Diâmetro (km)',
            'indice_risco': 'Índice de Risco (0-100)',
            'nivel_indice': 'Nível'
        },
        color_discrete_map={
            'MUITO BAIXO': '#00ff00',
            'BAIXO': '#88ff00',
            'MÉDIO': '#ffff00',
            'ALTO': '#ff8800',
            'CRÍTICO': '#ff0000'
        }
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.divider()
    
    # ========== METODOLOGIA ==========
    with st.expander("📖 Metodologia de Cálculo"):
        st.markdown("""
        ### Como Calculamos o Risco
        
        #### 1. Índice de Risco Proprietário (0-100)
        Ponderação multifatorial:
        - **40% Tamanho:** Diâmetro do asteroide (normalizado até 1km)
        - **30% Distância:** Proximidade da Terra (quanto mais perto, maior o risco)
        - **20% Velocidade:** Velocidade de aproximação (normalizada até 100.000 km/h)
        - **10% Classificação NASA:** Se é potencialmente perigoso segundo a NASA
        
        #### 2. Energia de Impacto
        Fórmula: `E = 0.5 × m × v²`
        - Massa calculada assumindo densidade de 2.600 kg/m³ (rocha típica)
        - Velocidade de impacto real do asteroide
        - Resultado em megatons de TNT (1 MT = 4.184×10¹⁵ joules)
        
        #### 3. Raio de Destruição
        Fórmula empírica: `R ≈ 2.2 × E^0.33`
        - R: raio em km
        - E: energia em megatons
        
        #### 4. Categorias de Impacto
        Baseadas em estudos científicos e eventos históricos:
        - **< 25m:** Meteorito (queima na atmosfera)
        - **25-140m:** Impacto local
        - **140m-1km:** Impacto regional
        - **1-5km:** Impacto continental
        - **> 5km:** Evento de extinção
        
        **Fontes:**
        - NASA NEO Program
        - JPL Center for NEO Studies
        - Papers científicos sobre impactos históricos
        """)

else:  # Sobre
    st.title("Sobre o Projeto")
    st.markdown("""
    ### NEO Monitor - Sistema de Monitoramento de Asteroides
        
    #### Objetivo
    Monitorar e analisar objetos próximos à Terra (NEOs - Near Earth Objects) utilizando 
    dados da NASA NeoWs API, processamento ETL em Python e visualização interativa.
    
    #### Tecnologias
    - **Backend:** Python, SQLAlchemy, Pandas
    - **Frontend:** Streamlit, Plotly
    - **Banco de Dados:** PostgreSQL
    - **API:** NASA NeoWs
    
    #### Funcionalidades
    - Coleta automatizada de dados da NASA
    - Armazenamento histórico em banco de dados
    - Análise estatística de asteroides
    - Visualizações interativas
    - Classificação de periculosidade
    
    #### Fonte de Dados
    [NASA NeoWs API](https://api.nasa.gov/)
    
    ---
    **Desenvolvido por:** Symon O. Mantovani
    **Instituição:** IFSP PRC
    **Ano:** 2026
    """)