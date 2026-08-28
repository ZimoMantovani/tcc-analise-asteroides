import requests
import pandas as pd
from sqlalchemy import text
import os
from datetime import datetime, timedelta

from database import get_engine

# ⚠️ IMPORTANTE: nada de configuração roda aqui no nível do módulo.
# utils.py faz "from etl_completo import ..." e isso EXECUTA o arquivo
# inteiro no momento do import. Se a checagem de API_KEY (com exit())
# ou a criação da engine estivessem aqui fora, um problema de .env
# derrubaria o processo inteiro do Streamlit, não só essa função.

# ========== FUNÇÕES ==========

def extrair_dados_nasa(dias=7):
    """
    Extrai dados da NASA API
    """
    api_key = os.getenv('NASA_API_KEY')
    if not api_key:
        print("❌ ERRO: NASA_API_KEY não encontrada no .env")
        return None

    print(f"\n📡 Buscando asteroides dos próximos {dias} dias...")

    hoje = datetime.now()
    fim = hoje + timedelta(days=dias)

    url = "https://api.nasa.gov/neo/rest/v1/feed"
    params = {
        'start_date': hoje.strftime('%Y-%m-%d'),
        'end_date': fim.strftime('%Y-%m-%d'),
        'api_key': api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
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
                aproximacao = neo['close_approach_data'][0]

                asteroide = {
                    'id_neo': neo['id'],
                    'nome': neo['name'],
                    'referencia': neo['neo_reference_id'],

                    'diametro_min_km': neo['estimated_diameter']['kilometers']['estimated_diameter_min'],
                    'diametro_max_km': neo['estimated_diameter']['kilometers']['estimated_diameter_max'],

                    'perigoso': neo['is_potentially_hazardous_asteroid'],
                    'sentry_object': neo.get('is_sentry_object', False),

                    'data_aproximacao': datetime.strptime(aproximacao['close_approach_date'], '%Y-%m-%d'),
                    'data_hora_aproximacao': aproximacao['close_approach_date_full'],

                    'distancia_km': float(aproximacao['miss_distance']['kilometers']),
                    'distancia_lunar': float(aproximacao['miss_distance']['lunar']),
                    'distancia_astronomica': float(aproximacao['miss_distance']['astronomical']),

                    'velocidade_kmh': float(aproximacao['relative_velocity']['kilometers_per_hour']),
                    'velocidade_kms': float(aproximacao['relative_velocity']['kilometers_per_second']),

                    'orbita_corpo': aproximacao['orbiting_body'],
                    'data_coleta': datetime.now(),

                    'nasa_url': neo['nasa_jpl_url']
                }

                asteroides.append(asteroide)

            except (KeyError, IndexError) as e:
                print(f"⚠️ Asteroide {neo.get('name', 'desconhecido')} com dados incompletos: {e}")
                continue

    df = pd.DataFrame(asteroides)
    df_limpo = df.drop_duplicates(subset=['id_neo'], keep='first')

    print(f"✅ {len(df)} registros extraídos")
    print(f"✅ {len(df_limpo)} asteroides únicos após limpeza")

    return df_limpo


def carregar_no_banco(df):
    """
    Salva DataFrame no PostgreSQL usando lógica de UPSERT (acumula histórico).

    Mantém duas datas com significados diferentes:
    - data_coleta: sobrescrita a cada vez que o asteroide é visto de novo (= "última vez visto")
    - data_primeira_deteccao: preenchida automaticamente pelo Postgres SÓ no INSERT,
      nunca é tocada pelo UPDATE, então preserva o momento real da primeira detecção.
    """
    print(f"\n💾 Salvando {len(df)} asteroides no banco e acumulando histórico...")

    try:
        engine = get_engine()  # pega a engine só na hora de usar, não no import

        # 1. Garante que a tabela principal exista (útil para a 1ª execução)
        df.head(0).to_sql('asteroides', engine, if_exists='append', index=False)

        with engine.begin() as conn:
            conn.execute(text("SET client_min_messages TO WARNING;"))

            # 2. Garante a coluna data_primeira_deteccao (idempotente, não precisa de DO $$)
            conn.execute(text("""
                ALTER TABLE asteroides
                ADD COLUMN IF NOT EXISTS data_primeira_deteccao TIMESTAMP DEFAULT NOW();
            """))

            # 3. Garante que 'id_neo' é Chave Primária no PostgreSQL
            conn.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint WHERE conname = 'asteroides_pkey'
                    ) THEN
                        ALTER TABLE asteroides ADD CONSTRAINT asteroides_pkey PRIMARY KEY (id_neo);
                    END IF;
                END
                $$;
            """))

            # 4. Cria a tabela temporária (staging) e insere os novos dados nela
            df.to_sql('asteroides_staging', conn, if_exists='replace', index=False)

            # 5. Constrói a query de UPSERT dinamicamente baseada nas colunas do DataFrame
            #    (data_primeira_deteccao NÃO entra aqui de propósito — fica de fora do
            #    INSERT e do UPDATE, então o DEFAULT NOW() do Postgres cuida dela sozinho
            #    só na primeira vez que o id_neo aparece)
            colunas = [col for col in df.columns if col != 'id_neo']
            update_cols = ', '.join([f"{col} = EXCLUDED.{col}" for col in colunas])
            col_names = ', '.join(df.columns)

            upsert_query = text(f"""
                INSERT INTO asteroides ({col_names})
                SELECT {col_names} FROM asteroides_staging
                ON CONFLICT (id_neo) DO UPDATE SET
                {update_cols};
            """)

            conn.execute(upsert_query)
            conn.execute(text('DROP TABLE IF EXISTS asteroides_staging;'))

        print("✅ Dados salvos e histórico atualizado com sucesso!")
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
# Tudo que precisa acontecer só quando o script roda sozinho
# (python etl_completo.py) fica aqui dentro — nunca no nível do módulo.

if __name__ == "__main__":
    print("🚀 INICIANDO PIPELINE ETL - Near Earth Objects")
    print("="*70)

    dados_brutos = extrair_dados_nasa(dias=7)
    if not dados_brutos:
        print("❌ Pipeline interrompido: falha na extração")
        exit()

    df_asteroides = transformar_dados(dados_brutos)
    if df_asteroides.empty:
        print("❌ Pipeline interrompido: nenhum dado processado")
        exit()

    sucesso = carregar_no_banco(df_asteroides)
    if not sucesso:
        print("❌ Pipeline interrompido: falha ao salvar")
        exit()

    exibir_resumo(df_asteroides)

    print("\n🎉 PIPELINE COMPLETO!")
    print("="*70)