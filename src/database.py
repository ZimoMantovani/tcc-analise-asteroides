"""
Módulo central de conexão com o banco de dados.

Usado por etl_completo.py, utils.py e qualquer outro script do projeto,
para garantir que exista um único lugar de configuração da string de
conexão e das opções da engine (encoding, etc). Antes, essa lógica
estava duplicada em dois arquivos, com valores diferentes entre eles
(um lia tudo do .env, o outro tinha host/banco fixos no código).
"""
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

_engine = None  # cache simples em nível de módulo, reaproveitado entre chamadas


def _montar_connection_string() -> str:
    usuario = os.getenv('DB_USER')
    senha = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    porta = os.getenv('DB_PORT')
    banco = os.getenv('DB_NAME')

    faltando = [
        nome for nome, valor in {
            'DB_USER': usuario,
            'DB_PASSWORD': senha,
            'DB_HOST': host,
            'DB_PORT': porta,
            'DB_NAME': banco,
        }.items()
        if not valor
    ]

    if faltando:
        raise ValueError(
            f"Variáveis de ambiente faltando: {', '.join(faltando)}. "
            "Confira se o arquivo .env existe na raiz do projeto e está "
            "preenchido (ou se o script está sendo executado a partir da "
            "pasta correta, já que load_dotenv() procura o .env no diretório atual)."
        )

    return f"postgresql://{usuario}:{quote_plus(senha)}@{host}:{porta}/{banco}"


def get_engine():
    """
    Retorna a engine SQLAlchemy do projeto (criada uma única vez e reaproveitada).

    client_encoding='utf8' evita o erro de decode que aparecia ao salvar
    dados com acentuação (bytes fora de UTF-8 vindos de mensagens do servidor).
    """
    global _engine
    if _engine is None:
        connection_string = _montar_connection_string()
        _engine = create_engine(
            connection_string,
            connect_args={
                'client_encoding': 'utf8',
                'options': '-c lc_messages=C',
            },
        )
    return _engine