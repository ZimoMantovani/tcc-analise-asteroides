# 📄 **README.md COMPLETO PARA GITHUB**

Crie um arquivo `README.md` na raiz do projeto:

```markdown
# 🌍 NEO Monitor - Sistema de Monitoramento de Asteroides

Sistema automatizado de monitoramento e análise de asteroides próximos à Terra (NEOs - Near Earth Objects) utilizando dados da NASA NeoWs API, processamento ETL em Python e visualização interativa.

**Desenvolvido como TCC de Engenharia de Computação - IFSP PRC**

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como Executar](#como-executar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Screenshots](#screenshots)
- [Questões de Pesquisa](#questões-de-pesquisa)
- [Roadmap](#roadmap)
- [Contribuindo](#contribuindo)
- [Licença](#licença)
- [Contato](#contato)

---

## 📖 Sobre o Projeto

O NEO Monitor é um sistema web completo para monitoramento de asteroides próximos à Terra, desenvolvido com foco em Engenharia de Dados. O sistema coleta dados diariamente da NASA, processa informações sobre objetos potencialmente perigosos, armazena em banco de dados PostgreSQL e disponibiliza dashboards interativos para visualização de riscos e métricas.

### Objetivo

Tornar acessível ao público geral informações científicas sobre asteroides próximos à Terra, permitindo:
- Acompanhamento visual de aproximações
- Análise de riscos e cenários de impacto
- Compreensão de conceitos astronômicos complexos de forma intuitiva

---

## ✨ Funcionalidades

### Pipeline ETL Automatizado
- ✅ Coleta diária de dados da NASA NeoWs API
- ✅ Processamento e limpeza de dados com Pandas
- ✅ Armazenamento histórico em PostgreSQL
- ✅ Sistema de logs e monitoramento

### Dashboard Interativo
- ✅ **Home:** Métricas em tempo real e próximas aproximações
- ✅ **Estatísticas:** Análises detalhadas com gráficos interativos
- ✅ **Explorador:** Filtros dinâmicos e busca personalizada
- ✅ **Análise de Riscos:** Cálculo de energia de impacto e cenários
- ✅ **Visualização 3D:** Representação espacial Terra-Asteroides (animada)

### Análise de Riscos
- ✅ Índice de periculosidade proprietário (0-100)
- ✅ Cálculo de energia de impacto (megatons TNT)
- ✅ Estimativa de raio de destruição
- ✅ Comparação com eventos históricos
- ✅ Classificação por categoria de impacto

---

## 🛠️ Tecnologias

### Backend
- **Python 3.10+** - Linguagem principal
- **Pandas** - Manipulação de dados
- **SQLAlchemy** - ORM para banco de dados
- **Requests** - Consumo de API REST

### Frontend
- **Streamlit** - Framework web Python
- **Plotly** - Visualizações interativas
- **NumPy** - Cálculos científicos

### Banco de Dados
- **PostgreSQL 16** - Banco relacional

### APIs Externas
- **NASA NeoWs API** - Dados de asteroides

---

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.10 ou superior**
  - Download: [python.org](https://www.python.org/downloads/)
  
- **PostgreSQL 16 ou superior**
  - Download: [postgresql.org](https://www.postgresql.org/download/)
  
- **Git** (para clonar o repositório)
  - Download: [git-scm.com](https://git-scm.com/downloads/)

- **Chave de API da NASA** (gratuita)
  - Obtenha em: [api.nasa.gov](https://api.nasa.gov/)

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/tcc-asteroides.git
cd tcc-asteroides
```

### 2. Crie e ative o ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

**Conteúdo do `requirements.txt`:**
```txt
streamlit==1.31.0
pandas==2.2.0
plotly==5.18.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
python-dotenv==1.0.0
requests==2.31.0
numpy==1.26.3
```

---

## ⚙️ Configuração

### 1. Configure o PostgreSQL

**Abra o pgAdmin ou terminal do PostgreSQL e execute:**

```sql
-- Criar banco de dados
CREATE DATABASE tcc_asteroides;

-- Conectar ao banco
\c tcc_asteroides

-- A tabela será criada automaticamente pelo ETL
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# API da NASA
NASA_API_KEY=SuaChaveAqui

# Banco de Dados
DB_PASSWORD=postgres123
DB_USER=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tcc_asteroides
```

**⚠️ IMPORTANTE:** Adicione `.env` no `.gitignore` para não expor credenciais!

### 3. Crie o arquivo `.gitignore`

```gitignore
# Ambientes virtuais
venv/
.venv/
env/

# Credenciais
.env
*.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Streamlit
.streamlit/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Dados temporários
dados/
*.csv
*.json

# OS
.DS_Store
Thumbs.db
```

---

## 🎮 Como Executar

### 1. Primeira execução - Coletar dados

```bash
python etl_completo.py
```

**Saída esperada:**
```
🚀 INICIANDO PIPELINE ETL - Near Earth Objects
======================================================================
📡 Buscando asteroides dos próximos 7 dias...
✅ API respondeu: 88 asteroides encontrados
🔄 Processando dados...
✅ 88 asteroides únicos após limpeza
💾 Salvando 88 asteroides no banco...
✅ Dados salvos com sucesso!
🎉 PIPELINE COMPLETO!
```

### 2. Verificar dados salvos (opcional)

```bash
python verificar_dados.py
```

### 3. Iniciar o Dashboard

```bash
streamlit run dashboard.py
```

**O navegador abrirá automaticamente em:** `http://localhost:8501`

### 4. Visualização 3D (opcional - executar separadamente)

```bash
streamlit run visualizacao_3d_animada.py
```

---

## 📁 Estrutura do Projeto

```
tcc-asteroides/
│
├── 📂 src/                          # Código-fonte principal (opcional)
│
├── 📄 etl_completo.py               # Pipeline ETL (coleta de dados)
├── 📄 dashboard.py                  # Dashboard principal Streamlit
├── 📄 visualizacao_3d.py            # Visualização 3D estática
├── 📄 visualizacao_3d_animada.py    # Visualização 3D com animação
├── 📄 analise_riscos.py             # Módulo de cálculo de riscos
├── 📄 verificar_dados.py            # Script de validação
│
├── 📄 .env                          # Variáveis de ambiente (NÃO COMMITAR!)
├── 📄 .gitignore                    # Arquivos ignorados pelo Git
├── 📄 requirements.txt              # Dependências Python
├── 📄 README.md                     # Este arquivo
│
└── 📂 docs/                         # Documentação do TCC
    └── relatorio_parcial.md
```

---

## 📸 Screenshots

### Dashboard Principal
![Home](docs/screenshots/home.png)
*Painel principal com métricas e próximas aproximações*

### Análise de Riscos
![Riscos](docs/screenshots/riscos.png)
*Sistema de classificação de periculosidade e cenários de impacto*

### Visualização 3D
![3D](docs/screenshots/3d.png)
*Visualização espacial interativa Terra-Asteroides*

---

## 🔍 Questões de Pesquisa

Este projeto responde às seguintes questões de pesquisa do TCC:

### ✅ QP1: O que define periculosidade?
- Implementado sistema de classificação NASA + índice proprietário (0-100)
- Critérios: tamanho, distância, velocidade, classificação oficial

### ✅ QP2: Como acompanhar o percurso?
- Visualização 3D interativa com animação
- Posicionamento por distância real (distâncias lunares)
- Filtros e controles de exploração

### ✅ QP3: Quais são os riscos?
- Cálculo de energia de impacto (megatons TNT)
- Estimativa de raio de destruição
- Categorização por severidade (5 níveis)
- Comparação com eventos históricos

### 🔄 QP4: Processamento com IA
- **Status:** Em desenvolvimento
- **Planejado:** Modelo de classificação supervisionada ou análise temporal

---

## 🗓️ Roadmap

### Versão Parcial (Junho 2026) ✅
- [x] Arquitetura web completa
- [x] Pipeline ETL funcional
- [x] Dashboard interativo
- [x] Visualização 3D
- [x] Análise de riscos (QP1-QP3)
- [ ] Módulo de IA (QP4)

### Versão Final (Dezembro 2026)
- [ ] Automação ETL (GitHub Actions/Airflow)
- [ ] Sistema de notificações
- [ ] Testes automatizados
- [ ] Deploy em produção (Streamlit Cloud)
- [ ] Documentação completa (monografia)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Padrões de Código
- Siga PEP 8 para Python
- Adicione docstrings em funções
- Comente código complexo
- Teste antes de commitar

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Contato

**Symon O. Mantovani**

- 📧 Email: [seu-email@exemplo.com](mailto:seu-email@exemplo.com)
- 💼 LinkedIn: [seu-linkedin](https://linkedin.com/in/seu-usuario)
- 🐙 GitHub: [seu-usuario](https://github.com/seu-usuario)

**Instituição:** Instituto Federal de São Paulo - Campus Presidente Epitácio

**Orientador:** [Nome do Professor]

---

## 🙏 Agradecimentos

- **NASA** - Pelos dados abertos da NeoWs API
- **IFSP** - Pela estrutura e suporte acadêmico
- **Professor Orientador** - Pela orientação e feedback
- **Comunidade Python** - Pelas bibliotecas open-source

---

## 📚 Referências

1. NASA Near Earth Object Program - [https://cneos.jpl.nasa.gov/](https://cneos.jpl.nasa.gov/)
2. NASA NeoWs API Documentation - [https://api.nasa.gov/](https://api.nasa.gov/)
3. Streamlit Documentation - [https://docs.streamlit.io/](https://docs.streamlit.io/)
4. PostgreSQL Documentation - [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)

---

**⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!**

---

<div align="center">
  
  **🌍 Monitorando o céu, protegendo a Terra**
  
  ![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)
  ![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)
  ![License](https://img.shields.io/badge/License-MIT-green.svg)
  
</div>
```
