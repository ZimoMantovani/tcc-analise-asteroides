import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
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
        st.markdown(f"{hud_tag('DATABASE', cor='#00FF9D')} PostgreSQL (Supabase)", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"{hud_tag('IA & ML', cor='#A200FF')} Scikit-learn (Random Forest)", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"{hud_tag('FONTES DE DADOS', cor='#FFE600')} NASA NeoWs API & JPL Center Dataset", unsafe_allow_html=True)

st.divider()

# ========== MODEL CARD (METRICS & ML) ==========
st.subheader("🤖 Model Card: Inteligência Artificial", divider="violet")
st.markdown("""
A detecção de asteroides ameaçadores trabalha com um **dataset inerentemente desbalanceado** (apenas cerca de 9,7% dos objetos monitorados pela NASA representam risco real). Por isso, avaliar o modelo apenas pela acurácia seria enganoso (o *Paradoxo da Acurácia*). 

Nosso classificador Random Forest utiliza **peso balanceado de classes** e é validado através de **Validação Cruzada Estratificada (5-Folds)** para garantir que as métricas abaixo reflitam a capacidade real do modelo de identificar ameaças verdadeiras.
""")

caminho_metricas = 'models/metricas_modelo.json'
if os.path.exists(caminho_metricas):
    with open(caminho_metricas, 'r') as f:
        metricas = json.load(f)
    
    # KPIs do Modelo
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("🎯 Acurácia Geral", f"{metricas['acuracia_geral']*100:.1f}%")
    col_m2.metric("⚠️ Precision (Perigosos)", f"{metricas['precisao_perigosos']*100:.1f}%")
    col_m3.metric("🚨 Recall (Perigosos)", f"{metricas['recall_perigosos']*100:.1f}%")
    col_m4.metric("⚖️ F1-Score", f"{metricas['f1_perigosos']*100:.1f}%")
    
    st.write("")
    
    col_chart, col_matrix = st.columns([2, 1])
    
    with col_chart:
        st.markdown("**Importância das Variáveis (Feature Importance)**")
        df_feat = pd.DataFrame({
            'Feature': list(metricas['importancia_features'].keys()),
            'Importância': list(metricas['importancia_features'].values())
        }).sort_values(by='Importância', ascending=True)
        
        # Traduzindo os nomes das features para o gráfico ficar mais amigável
        mapa_nomes = {
            'est_diameter_max': 'Diâmetro Máx.',
            'relative_velocity': 'Velocidade',
            'miss_distance': 'Distância',
            'absolute_magnitude': 'Magnitude (Brilho)'
        }
        df_feat['Feature'] = df_feat['Feature'].map(mapa_nomes)
        
        fig_feat = px.bar(
            df_feat, 
            x='Importância', 
            y='Feature', 
            orientation='h',
            color='Importância',
            color_continuous_scale=['#00F0FF', '#A200FF']
        )
        fig_feat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#E8E8E8',
            margin=dict(l=0, r=0, t=10, b=0),
            height=220,
            xaxis=dict(gridcolor='rgba(0,240,255,0.08)'),
            yaxis_title=None
        )
        st.plotly_chart(fig_feat, use_container_width=True)
    
    with col_matrix:
        st.markdown("**Matriz de Confusão (Dados de Teste)**")
        mc = metricas['matriz_confusao']
        # mc[0][0] = TN, mc[0][1] = FP
        # mc[1][0] = FN, mc[1][1] = TP
        st.markdown(f"""
        <div style="background-color: rgba(20, 27, 46, 0.5); padding: 1.2rem; border-radius: 0.5rem; border: 1px solid rgba(162, 0, 255, 0.3);">
            <table style="width:100%; text-align:center; color:#E8E8E8; font-size: 0.9rem;">
                <tr>
                    <th style="padding-bottom: 10px;"></th>
                    <th style="padding-bottom: 10px;">Prevê: Seguro</th>
                    <th style="padding-bottom: 10px;">Prevê: Perigo</th>
                </tr>
                <tr>
                    <th style="text-align:left; padding: 5px 0;">Real: Seguro</th>
                    <td style="color:#00F0FF; font-weight:bold; background-color: rgba(0, 240, 255, 0.1); border-radius: 4px;">{mc[0][0]}<br><small>V. Negativo</small></td>
                    <td style="color:#FFE600;">{mc[0][1]}<br><small>F. Positivo</small></td>
                </tr>
                <tr>
                    <th style="text-align:left; padding: 5px 0;">Real: Perigo</th>
                    <td style="color:#FF2A5F;">{mc[1][0]}<br><small>F. Negativo</small></td>
                    <td style="color:#00FF9D; font-weight:bold; background-color: rgba(0, 255, 157, 0.1); border-radius: 4px;">{mc[1][1]}<br><small>V. Positivo</small></td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("⚠️ Métricas do modelo não encontradas. O modelo ainda está sendo treinado no servidor.", icon="⏳")

st.divider()

# Seção do Desenvolvedor (Estilo "ID Card")
st.subheader("Sobre o Desenvolvedor", divider="blue")

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
        Projeto desenvolvido com foco na integração de pipelines de ETL, análise de dados e criação de interfaces analíticas. O sistema reflete a aplicação prática de engenharia de dados integrada a bancos de dados relacionais e visualização de métricas em tempo real.
        """)
        st.markdown("**Instituição:** IFSP - Câmpus Piracicaba")
        st.markdown("**Ano:** 2026")
        
    with c2:
        st.markdown("<div style='text-align: right; padding-top: 1rem;'>", unsafe_allow_html=True)
        st.markdown("🚀 **Status do Sistema:** `ONLINE`")
        st.markdown("V 1.0.0")
        st.markdown("</div>", unsafe_allow_html=True)