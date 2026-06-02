import streamlit as st

st.set_page_config(
    page_title="NEO Monitor - Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Bem-vindo ao NEO Monitor")
st.markdown("""
### Sistema de Monitoramento de Asteroides

Utilize o menu lateral para navegar entre as seções do aplicativo.

Este painel agora utiliza o formato de **Múltiplas Páginas** do Streamlit.
""")
