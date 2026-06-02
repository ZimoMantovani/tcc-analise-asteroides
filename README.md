# 🌍 NEO Monitor - Sistema de Monitoramento de Asteroides

<div align="center">
  <p><b>Monitorando o céu, protegendo a Terra</b></p>
  
  ![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python)
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg?style=for-the-badge&logo=postgresql)
  ![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg?style=for-the-badge&logo=streamlit)
  ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange.svg?style=for-the-badge&logo=scikit-learn)
  ![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)
</div>

<br>

Sistema automatizado de monitoramento e análise de asteroides próximos à Terra (NEOs - *Near Earth Objects*) utilizando dados da NASA NeoWs API, processamento ETL em Python, Machine Learning e visualização interativa com Streamlit.

**Desenvolvido como TCC de Engenharia de Computação - IFSP PRC**

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#️-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#️-configuração)
- [Como Executar](#-como-executar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Contribuição](#-contribuindo)
- [Licença](#-licença)
- [Contato](#-contato)

---

## 📖 Sobre o Projeto

O **NEO Monitor** é um sistema web analítico e preditivo para monitoramento de asteroides próximos à Terra. Desenvolvido com foco em Engenharia de Dados e Machine Learning, o sistema automatiza a coleta de dados da NASA, armazena o histórico em um banco PostgreSQL e fornece dashboards para análise de riscos, cenários de impacto e métricas astronômicas de forma intuitiva.

### Objetivo

Tornar o monitoramento de asteroides e o entendimento dos riscos associados acessível para a comunidade científica e para o público geral, através de:
- Acompanhamento interativo e atualizado.
- Análise aprofundada de periculosidade.
- Uso de IA (Machine Learning) para classificação e previsão de ameaças.

---

## ✨ Funcionalidades

### 🔄 Pipeline ETL Automatizado (`etl_completo.py`)
- Coleta diária automatizada da NASA NeoWs API.
- Tratamento, limpeza de dados e padronização usando `pandas`.
- Armazenamento em banco de dados relacional (PostgreSQL).

### 📊 Dashboard Interativo (Streamlit)
O sistema foi modularizado em múltiplas páginas para melhor experiência de usuário:
- **🏠 Home:** Resumo rápido, próximas aproximações e status geral do céu.
- **📈 Estatísticas:** Visão analítica, com distribuições de tamanhos, distâncias e velocidades.
- **🔭 Explorador:** Busca detalhada de asteroides com filtros dinâmicos.
- **⚠️ Análise de Riscos:** Módulo focado na simulação de impacto, energia (Megatons) e raio de destruição.
- **ℹ️ Sobre:** Informações sobre o projeto e metodologia TCC.

### 🤖 Machine Learning (`modelo_ia.py`)
- Modelo baseado em **Random Forest Classifier**.
- Treinado com dados históricos para determinar a periculosidade (`hazardous`) de novos asteroides detectados com base em suas características físicas e orbitais.

---

## 🛠️ Tecnologias

### Linguagem & Ferramentas
- **Python 3.10+**
- **Pandas e NumPy** (Manipulação e cálculos)
- **Scikit-Learn e Joblib** (Machine Learning e serialização de modelos)

### Backend e Dados
- **PostgreSQL 16** (Banco de dados)
- **SQLAlchemy** (ORM)
- **Requests** (Consumo da API REST)

### Frontend (Dashboard)
- **Streamlit** (Framework de UI)
- **Plotly** (Gráficos interativos)

---

## 📦 Pré-requisitos

Para executar este projeto localmente, você precisa ter:

- **Python 3.10+**: [Download](https://www.python.org/downloads/)
- **PostgreSQL 16+**: [Download](https://www.postgresql.org/download/)
- **Chave de API da NASA** (gratuita): [Obter em api.nasa.gov](https://api.nasa.gov/)

---

## 🚀 Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/tcc-analise-asteroides.git
   cd tcc-analise-asteroides
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
    pip install -r requirements.txt
   ```

---

## ⚙️ Configuração

1. **Configuração do Banco de Dados (PostgreSQL):**
   ```sql
   -- Conecte-se ao PostgreSQL e crie o banco
   CREATE DATABASE tcc_asteroides;
   ```

2. **Variáveis de Ambiente:**
   Crie um arquivo `.env` na raiz do projeto contendo suas credenciais:
   ```env
   # API da NASA
   NASA_API_KEY=SuaChaveAqui
   
   # Banco de Dados
   DB_USER=postgres
   DB_PASSWORD=sua_senha
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=tcc_asteroides
   ```
   *Certifique-se de que o `.env` esteja no `.gitignore`.*

---

## 🎮 Como Executar

### 1. Alimentação do Banco de Dados (ETL)
Antes de rodar o painel pela primeira vez, execute o pipeline de coleta para popular o banco de dados:
```bash
python etl_completo.py
```

### 2. Treinamento da Inteligência Artificial (Opcional)
O modelo pré-treinado (`modelo_asteroides.joblib`) já deve estar na pasta. Caso deseje retreinar com novos dados do arquivo CSV local:
```bash
python modelo_ia.py
```

### 3. Iniciar o Dashboard (Streamlit)
Execute a aplicação principal. O sistema abrirá automaticamente no navegador em `http://localhost:8501`.
```bash
streamlit run app.py
```

---

## 📁 Estrutura do Projeto

A estrutura foi reorganizada para suportar o formato *Multipage* do Streamlit e a integração com IA:

```text
tcc-analise-asteroides/
│
├── 📄 app.py                        # Ponto de entrada (Home) do Streamlit
├── 📂 pages/                        # Páginas adicionais do Dashboard
│   ├── 1_Home.py
│   ├── 2_Estatisticas.py
│   ├── 3_Explorador.py
│   ├── 4_Analise_Riscos.py
│   └── 5_Sobre.py
│
├── 📄 etl_completo.py               # Script de extração, transformação e carga (NASA API -> BD)
├── 📄 modelo_ia.py                  # Script para treino e inferência do modelo Random Forest
├── 📄 modelo_asteroides.joblib      # Modelo de IA serializado
├── 📄 analise_riscos.py             # Lógica de cálculo de risco e energia de impacto
├── 📄 utils.py                      # Funções auxiliares gerais
├── 📄 curiosidades_ia.py            # Geração de curiosidades astronômicas
│
├── 📄 neo_v2.csv                    # Dataset de backup/treinamento
├── 📄 .env                          # Configurações locais (Ignorado pelo Git)
└── 📄 README.md                     # Documentação principal
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Se você deseja ajudar:
1. Faça o *Fork* do projeto
2. Crie sua *branch* de feature (`git checkout -b feature/NovaAnalise`)
3. Faça o *commit* das suas alterações (`git commit -m 'Add: nova métrica de análise orbital'`)
4. Faça o *Push* para a branch (`git push origin feature/NovaAnalise`)
5. Abra um *Pull Request*

---

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para obter mais informações.

---

## 👤 Contato

**Symon O. Mantovani**
- 📧 Email: symonmantovani36@gmail.com
- 💼 LinkedIn: [Symon Mantovani](https://www.linkedin.com/in/symon-mantovani/)
- 🐙 GitHub: [Symon Mantovani](https://github.com/ZimoMantovani)

**Instituição:** Instituto Federal de São Paulo (IFSP) - Campus Piracicaba

---
*Referências da API: [NASA NeoWs (Near Earth Object Web Service)](https://api.nasa.gov/)*