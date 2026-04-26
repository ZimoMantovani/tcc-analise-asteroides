"""
Apenas para teste
"""
import requests
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

# ========== CONFIGURAÇÃO ==========
print("🔧 Carregando configurações...")

# Banco
usuario = "postgres"
senha = os.getenv('DB_PASSWORD', 'postgres123')
host = "localhost"
porta = "5432"
banco = "tcc_asteroides"

connection_string = f"postgresql://{usuario}:{quote_plus(senha)}@{host}:{porta}/{banco}?client_encoding=utf8"
engine = create_engine(connection_string, connect_args={'client_encoding': 'utf8'})

# NASA API
API_KEY = os.getenv('NASA_API_KEY')  

if not API_KEY:
    print("❌ ERRO: NASA_API_KEY não encontrada no .env")
    exit()

# ========== FUNÇÕES ==========

def extrair_dados_nasa(dias=7):
    """
    Extrai dados da NASA API
    """
    print(f"\n📡 Buscando asteroides dos próximos {dias} dias...")
    
    hoje = datetime.now()
    fim = hoje + timedelta(days=dias)
    
    url = "https://api.nasa.gov/neo/rest/v1/feed"
    params = {
        'start_date': hoje.strftime('%Y-%m-%d'),
        'end_date': fim.strftime('%Y-%m-%d'),
        'api_key': API_KEY  # ⚠️ CORRIGIDO: agora usa api_key (sem underscore no meio)
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Levanta exceção se status != 200
        data = response.json()
        print(f"✅ API respondeu: {data['element_count']} asteroides encontrados")
        return data
    except Exception as e:
        print(f"❌ Erro ao acessar NASA API: {e}")
        return None

def transformar_dados(data):
    """
    Transforma JSON da NASA em DataFrame com TODOS os campos necessários
    """
    print("\n🔄 Processando dados...")
    
    asteroides = []
    
    for date, neos in data['near_earth_objects'].items():
        for neo in neos:
            try:
                # Pegar dados da primeira aproximação (a mais próxima)
                aproximacao = neo['close_approach_data'][0]
                
                asteroide = {
                    # Identificação
                    'id_neo': neo['id'],
                    'nome': neo['name'],
                    'referencia': neo['neo_reference_id'],
                    
                    # Tamanho (km)
                    'diametro_min_km': neo['estimated_diameter']['kilometers']['estimated_diameter_min'],
                    'diametro_max_km': neo['estimated_diameter']['kilometers']['estimated_diameter_max'],
                    
                    # Classificação NASA
                    'perigoso': neo['is_potentially_hazardous_asteroid'],
                    'sentry_object': neo.get('is_sentry_object', False),
                    
                    # Dados de aproximação
                    'data_aproximacao': datetime.strptime(aproximacao['close_approach_date'], '%Y-%m-%d'),
                    'data_hora_aproximacao': aproximacao['close_approach_date_full'],
                    
                    # Distância
                    'distancia_km': float(aproximacao['miss_distance']['kilometers']),
                    'distancia_lunar': float(aproximacao['miss_distance']['lunar']),
                    'distancia_astronomica': float(aproximacao['miss_distance']['astronomical']),
                    
                    # Velocidade
                    'velocidade_kmh': float(aproximacao['relative_velocity']['kilometers_per_hour']),
                    'velocidade_kms': float(aproximacao['relative_velocity']['kilometers_per_second']),
                    
                    # Metadados
                    'orbita_corpo': aproximacao['orbiting_body'],
                    'data_coleta': datetime.now(),
                    
                    # URL NASA (para referência)
                    'nasa_url': neo['nasa_jpl_url']
                }
                
                asteroides.append(asteroide)
                
            except (KeyError, IndexError) as e:
                print(f"⚠️ Asteroide {neo.get('name', 'desconhecido')} com dados incompletos: {e}")
                continue
    
    df = pd.DataFrame(asteroides)
    
    # Remover duplicatas (mesmo asteroide pode aparecer em múltiplas datas)
    df_limpo = df.drop_duplicates(subset=['id_neo'], keep='first')
    
    print(f"✅ {len(df)} registros extraídos")
    print(f"✅ {len(df_limpo)} asteroides únicos após limpeza")
    
    return df_limpo

def carregar_no_banco(df):
    """
    Salva DataFrame no PostgreSQL
    """
    print(f"\n💾 Salvando {len(df)} asteroides no banco...")
    
    try:
        # if_exists='replace' apaga e recria a tabela
        # Mude para 'append' depois quando quiser acumular histórico
        df.to_sql('asteroides', engine, if_exists='replace', index=False)
        print("✅ Dados salvos com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")
        return False

def exibir_resumo(df):
    """
    Mostra estatísticas dos dados coletados
    """
    print("\n" + "="*70)
    print("📊 RESUMO DA COLETA")
    print("="*70)
    print(f"\n📌 Total de asteroides: {len(df)}")
    print(f"🚨 Potencialmente perigosos: {len(df[df['perigoso'] == True])} ({len(df[df['perigoso'] == True])/len(df)*100:.1f}%)")
    print(f"\n📏 Tamanhos:")
    print(f"   Maior: {df['diametro_max_km'].max():.3f} km")
    print(f"   Menor: {df['diametro_min_km'].min():.3f} km")
    print(f"   Médio: {df['diametro_max_km'].mean():.3f} km")
    print(f"\n🏃 Velocidades:")
    print(f"   Máxima: {df['velocidade_kmh'].max():,.0f} km/h")
    print(f"   Mínima: {df['velocidade_kmh'].min():,.0f} km/h")
    print(f"   Média: {df['velocidade_kmh'].mean():,.0f} km/h")
    print(f"\n🌍 Distâncias:")
    print(f"   Mais próximo: {df['distancia_km'].min():,.0f} km ({df['distancia_lunar'].min():.2f} distâncias lunares)")
    print(f"   Mais distante: {df['distancia_km'].max():,.0f} km ({df['distancia_lunar'].max():.2f} distâncias lunares)")
    print("\n" + "="*70)

# ========== PIPELINE PRINCIPAL ==========

if __name__ == "__main__":
    print("🚀 INICIANDO PIPELINE ETL - Near Earth Objects")
    print("="*70)
    
    # 1. EXTRAIR
    dados_brutos = extrair_dados_nasa(dias=7)
    if not dados_brutos:
        print("❌ Pipeline interrompido: falha na extração")
        exit()
    
    # 2. TRANSFORMAR
    df_asteroides = transformar_dados(dados_brutos)
    if df_asteroides.empty:
        print("❌ Pipeline interrompido: nenhum dado processado")
        exit()
    
    # 3. CARREGAR
    sucesso = carregar_no_banco(df_asteroides)
    if not sucesso:
        print("❌ Pipeline interrompido: falha ao salvar")
        exit()
    
    # 4. RESUMO
    exibir_resumo(df_asteroides)
    
    print("\n🎉 PIPELINE COMPLETO!")
    print("="*70)