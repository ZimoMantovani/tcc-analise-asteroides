# 🌍 NEO Monitor - Sistema de Monitoramento de Asteroides

<div align="center">
  <p><b>Monitorando o céu, protegendo a Terra</b></p>

  ![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python)
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg?style=for-the-badge&logo=postgresql)
  ![Streamlit](https://img.shields.io/badge/Streamlit-1.63-red.svg?style=for-the-badge&logo=streamlit)
  ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange.svg?style=for-the-badge&logo=scikit-learn)
  ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=for-the-badge&logo=docker)
  ![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)
</div>

<br>

Sistema automatizado de monitoramento e análise de asteroides próximos à Terra (NEOs - *Near Earth Objects*) utilizando dados da NASA NeoWs API, processamento ETL em Python, Machine Learning e visualização interativa com Streamlit.

**Desenvolvido como TCC de Engenharia de Computação - IFSP Câmpus Piracicaba**

---

## 🌐 Acesse Online

O sistema está no ar, com coleta de dados automatizada diariamente:

### 👉 **[neo-analyser.streamlit.app](https://neo-analyser.streamlit.app/)**

Hospedado no Streamlit Community Cloud, com banco de dados PostgreSQL gerenciado pelo Supabase.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#️-tecnologias)
- [Automação](#-automação)
- [Como Rodar Localmente](#-como-rodar-localmente)
- [Testes Automatizados](#-testes-automatizados)
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

### 🔄 Pipeline ETL Automatizado (`src/etl_completo.py`)
- Coleta diária automatizada da NASA NeoWs API, rodando de verdade via GitHub Actions (ver [Automação](#-automação)) — não depende de ninguém executar nada manualmente.
- Tratamento, limpeza de dados e padronização usando `pandas`.
- Armazenamento em PostgreSQL com **UPSERT real**: cada asteroide é atualizado quando reaparece numa nova varredura, preservando a data da primeira detecção e acumulando histórico de verdade.

### 📊 Dashboard Interativo (Streamlit)
O sistema foi modularizado em múltiplas páginas para melhor experiência de usuário:
- **🏠 Home** (`app.py`): Resumo rápido, próximas aproximações e status geral do céu.
- **📈 Estatísticas:** Visão analítica, com distribuições de tamanhos, distâncias e velocidades.
- **🔭 Explorador:** Busca detalhada de asteroides com filtros dinâmicos.
- **⚠️ Análise de Riscos:** Simulação de impacto, energia (Megatons), raio de destruição e predição de IA.
- **ℹ️ Sobre:** Informações do projeto, arquitetura e **Model Card** do modelo de Machine Learning (métricas, matriz de confusão, importância das features).

### 🤖 Machine Learning (`src/modelo_ml.py`)
- Classificador **Random Forest**, treinado com dados históricos (~90 mil asteroides) para prever a periculosidade (`hazardous`) de novos objetos com base em diâmetro, velocidade, distância e magnitude absoluta.
- **Validação cruzada estratificada (5-folds)** e `class_weight='balanced'`, já que apenas ~9,7% dos asteroides do dataset são classificados como perigosos — tratar esse desbalanceamento evita que a acurácia sozinha dê uma falsa sensação de qualidade do modelo.
- Métricas (precision, recall, F1, matriz de confusão, importância das features) são salvas em `models/metricas_modelo.json` e exibidas na aba Sobre.

### 📝 Geração de Insights (`src/gerador_insights.py`)
Textos interpretativos gerados por **NLG baseada em regras** (Natural Language Generation por templates, com variação determinística por asteroide) — deliberadamente sem depender de nenhuma LLM externa paga.

---

## 🛠️ Tecnologias

### Linguagem & Ferramentas
- **Python 3.10+**
- **Pandas e NumPy** (Manipulação e cálculos)
- **Scikit-Learn e Joblib** (Machine Learning e serialização de modelos)

### Backend e Dados
- **PostgreSQL 16**, hospedado no **Supabase** em produção (ou local via Docker)
- **SQLAlchemy** (ORM)
- **Requests** (Consumo da API REST da NASA)

### Frontend (Dashboard)
- **Streamlit** (Framework de UI) — hospedado no **Streamlit Community Cloud**
- **Plotly** (Gráficos interativos)

### Infraestrutura
- **Docker + Docker Compose** — ambiente local completo (app + Postgres) com um único comando
- **GitHub Actions** — automação da coleta diária e do "keep-alive" da aplicação (ver abaixo)
- **Pytest** — testes automatizados da lógica de cálculo de risco

---

## 🤖 Automação

Dois workflows do GitHub Actions rodam continuamente, sem depender de ninguém acessar o sistema manualmente:

| Workflow | Frequência | O que faz |
|---|---|---|
| `.github/workflows/etl-diario.yml` | 1x por dia | Executa `python -m src.etl_completo` direto contra o banco na nuvem (Supabase), coletando os asteroides mais recentes da NASA. |
| `.github/workflows/keep-alive.yml` | A cada 6h | Abre o app publicado com um navegador real (Playwright), acorda-o caso esteja hibernando (comportamento padrão do Streamlit Community Cloud após 12h sem tráfego) e aciona uma varredura adicional pela própria interface. |

---

## 💻 Como Rodar Localmente

Existem dois jeitos — escolha o que preferir.

### Opção A — Docker (recomendado, não precisa instalar PostgreSQL)

**Pré-requisitos:** [Docker](https://www.docker.com/) e Docker Compose.

1. Clone o repositório e entre na pasta:
   ```bash
   git clone https://github.com/ZimoMantovani/tcc-analise-asteroides.git
   cd tcc-analise-asteroides
   ```
2. Crie um arquivo `.env` na raiz com sua chave da NASA (o restante das variáveis já tem valores padrão para uso local):
   ```env
   NASA_API_KEY=SuaChaveAqui
   ```
3. Suba tudo (app + banco PostgreSQL) com um único comando:
   ```bash
   docker compose up --build
   ```
4. Acesse `http://localhost:8501` no navegador. Na primeira execução, clique em **"INICIAR VARREDURA (ATUALIZAR)"** na barra lateral para popular o banco com os dados mais recentes da NASA.

### Opção B — Manual (Python + PostgreSQL local)

**Pré-requisitos:**
- **Python 3.10+**: [Download](https://www.python.org/downloads/)
- **PostgreSQL 16+**: [Download](https://www.postgresql.org/download/)
- **Chave de API da NASA** (gratuita): [Obter em api.nasa.gov](https://api.nasa.gov/)

1. Clone o repositório, crie e ative um ambiente virtual, e instale as dependências:
   ```bash
   git clone https://github.com/ZimoMantovani/tcc-analise-asteroides.git
   cd tcc-analise-asteroides
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Crie o banco no PostgreSQL:
   ```sql
   CREATE DATABASE tcc_asteroides;
   ```
3. Crie um `.env` na raiz do projeto:
   ```env
   NASA_API_KEY=SuaChaveAqui

   DB_USER=postgres
   DB_PASSWORD=sua_senha
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=tcc_asteroides
   ```
   *(Em produção na nuvem, `DATABASE_URL` sozinha substitui essas 5 variáveis — veja `src/database.py`.)*
4. Rode o pipeline de coleta pela primeira vez para popular o banco:
   ```bash
   python -m src.etl_completo
   ```
5. **(Opcional)** Retreine o modelo de IA com os dados do CSV local (o modelo pré-treinado já vem no repositório em `models/`):
   ```bash
   python -m src.modelo_ml
   ```
6. Inicie o dashboard:
   ```bash
   streamlit run app.py
   ```
   O sistema abre automaticamente em `http://localhost:8501`.

> ⚠️ Sempre rode os scripts com `python -m src.<módulo>` (não `python src/<módulo>.py` direto) — os módulos importam uns aos outros como pacote (`src.database`, `src.etl_completo`...), e rodar o arquivo isolado quebra esse import.

---

## 🧪 Testes Automatizados

A lógica pura de cálculo de risco (`src/analise_riscos.py`) tem cobertura de testes com `pytest` — é a única parte do sistema que não depende de banco de dados ou da API da NASA para ser testada isoladamente.

```bash
pip install pytest  # já incluso em requirements.txt
pytest
```

---

## 📁 Estrutura do Projeto

```text
tcc-analise-asteroides/
│
├── 📄 app.py                        # Ponto de entrada (Home) do Streamlit
├── 📂 pages/                        # Páginas adicionais do Dashboard
│   ├── 2_Estatisticas.py
│   ├── 3_Explorador.py
│   ├── 4_Analise_Riscos.py
│   └── 5_Sobre.py                   # Inclui o Model Card do ML
│
├── 📂 src/                          # Todo o "backend": ETL, banco, ML, regras de negócio
│   ├── database.py                  # Conexão central (Supabase na nuvem / Postgres local)
│   ├── etl_completo.py              # Extração, transformação e carga (NASA API -> BD)
│   ├── modelo_ml.py                 # Treino (com validação cruzada) e inferência do Random Forest
│   ├── analise_riscos.py            # Cálculo de risco, energia de impacto e raio de destruição
│   ├── gerador_insights.py          # Geração de texto interpretativo (NLG baseada em regras)
│   ├── utils.py                     # Funções auxiliares (cache, sidebar, botão de atualização)
│   ├── estilo.py                    # Tema visual (CSS espacial/HUD) e capa com imagem APOD da NASA
│   └── keep_alive.py                # Script Playwright usado pelo workflow de keep-alive
│
├── 📂 tests/                        # Testes automatizados (pytest)
│   └── test_analise_riscos.py
│
├── 📂 data/
│   └── neo_v2.csv                   # Dataset de treinamento (histórico NASA, ~90k objetos)
├── 📂 models/
│   ├── modelo_asteroides.joblib     # Modelo de IA serializado
│   └── metricas_modelo.json         # Métricas do modelo (consumidas pelo Model Card)
├── 📂 assets/
│   └── logo.png
│
├── 📂 .github/workflows/            # Automação (ETL diário + keep-alive)
├── 📂 .streamlit/                   # Configuração de tema do Streamlit
├── 📂 .devcontainer/                # Configuração para GitHub Codespaces
│
├── 🐳 Dockerfile
├── 🐳 docker-compose.yml
├── 📄 .dockerignore
├── 📄 pytest.ini
├── 📄 requirements.txt
├── 📄 .env                          # Configurações locais (ignorado pelo Git)
├── 📄 LICENSE
└── 📄 README.md
```

---

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
