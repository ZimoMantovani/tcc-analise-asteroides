"""
Apenas para teste
"""
import streamlit as st

# Configuração da página (sempre primeiro!)
st.set_page_config(
    page_title="NEO Monitor",
    page_icon="🌍",
    layout="wide"  # Usa a tela toda
)

# Título principal
st.title("🌍 Monitoramento de Asteroides - NEO Watch")

# Subtítulo
st.subheader("Sistema de Análise de Objetos Próximos à Terra")

# Texto simples
st.write("Bem-vindo ao sistema de monitoramento de asteroides!")

# Métricas (números grandes)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total de Asteroides",
        value="88",
        delta="+5 desde ontem"
    )

with col2:
    st.metric(
        label="Potencialmente Perigosos",
        value="12",
        delta="-2 desde ontem",
        delta_color="inverse"  # Verde quando diminui
    )

with col3:
    st.metric(
        label="Maior Diâmetro",
        value="847 m"
    )

# Separador
st.divider()

# Mensagem de sucesso
st.success("✅ Sistema operacional!")

# Botão
if st.button("Atualizar Dados"):
    st.balloons()  # Animação de confete!
    st.write("Dados atualizados com sucesso!")