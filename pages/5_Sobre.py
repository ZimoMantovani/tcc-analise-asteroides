import streamlit as st
from src.utils import render_sidebar
from src.estilo import aplicar_tema_espacial, renderizar_hero, hud_tag
from PIL import Image
icone = Image.open("assets/logo.png")

st.set_page_config(page_title="Sobre - NEO Monitor", page_icon=icone, layout="wide")

# Aplica a identidade visual espacial
aplicar_tema_espacial()
render_sidebar()

# Capa padronizada
renderizar_hero(
    "Especificações do Sistema",
    "Arquitetura, tecnologias e informações sobre o projeto NEO Monitor"
)

st.divider()

col_esq, col_dir = st.columns([1.2, 1])

with col_esq:
    st.subheader("Objetivo da Missão", divider="blue")
    st.markdown("""
    O **NEO Monitor** é um sistema avançado de monitoramento e análise de objetos próximos à Terra (NEOs - *Near Earth Objects*). 
    
    A plataforma consome dados diretos da telemetria da NASA, processa essas informações através de pipelines de dados (ETL) e aplica cálculos físicos e modelos de Inteligência Artificial para classificar o grau de periculosidade matemática de cada corpo celeste em tempo real.
    """)
    
    st.write("")
    
    st.subheader("Funcionalidades Principais", divider="blue")
    st.markdown("""
    - 📡 **Telemetria:** Coleta automatizada de dados via API da NASA.
    - 💾 **Armazenamento:** Histórico estruturado em banco de dados relacional.
    - 📊 **Analytics:** Análise estatística e visualizações interativas em painéis HUD.
    - ⚠️ **Gestão de Risco:** Classificação de periculosidade física e simulação de impactos.
    - 🧠 **Módulo de IA:** Análise inteligente baseada em Machine Learning (Random Forest) para predição de riscos e geração de relatórios educacionais.
    """)

with col_dir:
    st.subheader("Stack Tecnológica", divider="blue")
    
# Injeta o CSS apontando para a key 'tech_stack'
    st.markdown("""
        <style>
        .st-key-tech_stack {
            border: 1px solid rgba(0, 240, 255, 0.25);
            border-radius: 0.75rem;
            padding: 1.5rem;
            background-color: rgba(20, 27, 46, 0.55);
            backdrop-filter: blur(6px);
            box-shadow: 0 0 16px rgba(0, 240, 255, 0.06);
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container(key="tech_stack"):
        st.markdown(f"{hud_tag('BACKEND', cor='#00F0FF')} Python, SQLAlchemy, Pandas", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"{hud_tag('FRONTEND', cor='#FF2A5F')} Streamlit, Plotly, HTML/CSS", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"{hud_tag('DATABASE', cor='#00FF9D')} PostgreSQL", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"{hud_tag('IA & ML', cor='#A200FF')} Scikit-learn (Random Forest)", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"{hud_tag('FONTES DE DADOS', cor='#FFE600')} NASA NeoWs API & JPL Center Dataset", unsafe_allow_html=True)

st.divider()

# Seção do Desenvolvedor (Estilo "ID Card")
st.subheader("Sobre o Desenvolvedor", divider="blue")

st.divider()

# Injeta o CSS apontando para a key 'dev_card'
st.markdown("""
    <style>
    .st-key-dev_card {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 4px solid #00F0FF;
        border-radius: 0.5rem;
        padding: 2rem;
        background: linear-gradient(90deg, rgba(0, 240, 255, 0.05) 0%, rgba(20, 27, 46, 0.5) 100%);
        backdrop-filter: blur(10px);
    }
    </style>
""", unsafe_allow_html=True)

with st.container(key="dev_card"):
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("### Symon Oliveira Mantovani")
        st.markdown("**Engenharia da Computação | Dados & Desenvolvimento**")
        st.write("""
        Projeto desenvolvido com foco na integração de pipelines de ETL, análise de dados e criação de interfaces analíticas. O sistema reflete a aplicação prática de engenharia de dados (Python, manipulação e transformação com Pandas) integrada a bancos de dados relacionais e visualização de métricas em tempo real.
        """)
        st.markdown("**Instituição:** IFSP - Câmpus Piracicaba")
        st.markdown("**Ano:** 2026")
        
    with c2:
        # Espaço reservado caso queira adicionar links do GitHub/LinkedIn com ícones
        st.markdown("<div style='text-align: right; padding-top: 1rem;'>", unsafe_allow_html=True)
        st.markdown("🚀 **Status do Sistema:** `ONLINE`")
        st.markdown("V 1.0.0")
        st.markdown("</div>", unsafe_allow_html=True)