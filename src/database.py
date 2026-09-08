"""
Módulo central de conexão com o banco de dados.
"""
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

_engine = None

def _montar_connection_string() -> str:
    # 1. Tenta usar a URL direta (Nuvem / Supabase)
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print("☁️ [Rede] Rota NUVEM (Supabase) detectada...")
        
        # Garante sslmode=require na URL de forma segura
        parsed = urlparse(database_url)
        query = parse_qs(parsed.query)
        query.setdefault("sslmode", ["require"])
        new_query = urlencode(query, doseq=True)
        return urlunparse(parsed._replace(query=new_query))

    # 2. Fallback para ambiente Local (Docker Compose)
    print("💻 [Rede] Rota LOCAL (Docker) ativada...")
    usuario = os.getenv('DB_USER')
    senha = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    porta = os.getenv('DB_PORT')
    banco = os.getenv('DB_NAME')

    faltando = [
        nome for nome, valor in {
            'DB_USER': usuario, 'DB_PASSWORD': senha, 'DB_HOST': host, 
            'DB_PORT': porta, 'DB_NAME': banco
        }.items() if not valor
    ]

    if faltando:
        raise ValueError(f"Variáveis locais faltando no .env: {', '.join(faltando)}")

    return f"postgresql://{usuario}:{quote_plus(senha)}@{host}:{porta}/{banco}"

def get_engine():
    global _engine
    if _engine is None:
        connection_string = _montar_connection_string()
        
        try:
            _engine = create_engine(
                connection_string,
                connect_args={'client_encoding': 'utf8', 'options': '-c lc_messages=C'}
            )
            # Força um teste de conexão rápido
            with _engine.connect() as conn:
                pass
            print("✅ [Banco] Conexão estabelecida com sucesso!")
            
        except Exception as e:
            print("\n❌ ERRO DE CONEXÃO: Verifique a senha ou a URL no seu .env!")
            raise e
            
    return _engine