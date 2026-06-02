import streamlit as st
from utils import render_sidebar

st.set_page_config(page_title="Sobre - NEO Monitor", page_icon="ℹ️", layout="wide")
render_sidebar()

st.title("Sobre o Projeto")
st.markdown("""
### NEO Monitor - Sistema de Monitoramento de Asteroides
    
#### Objetivo
Monitorar e analisar objetos próximos à Terra (NEOs - Near Earth Objects) utilizando 
dados da NASA NeoWs API, processamento ETL em Python.

#### Tecnologias
- **Backend:** Python, SQLAlchemy, Pandas
- **Frontend:** Streamlit, Plotly
- **Banco de Dados:** PostgreSQL
- **Machine Learning:** Scikit-learn 
- **API:** NASA NeoWs

#### Funcionalidades
- Coleta automatizada de dados da NASA
- Armazenamento histórico em banco de dados
- Análise estatística de asteroides
- Visualizações interativas
- Classificação de periculosidade matemática
- **Análise Inteligente e Educacional (IA Baseada em Random Forest)**

#### Fonte de Dados
- **Tempo Real:** [NASA NeoWs API](https://api.nasa.gov/)
- **Histórico (Treinamento da IA):** Dataset JPL Center for NEO Studies

---
**Desenvolvido por:** Symon O. Mantovani
**Instituição:** IFSP PRC
**Ano:** 2026
""")