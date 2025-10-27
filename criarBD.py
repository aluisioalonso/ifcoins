from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.modelosDB import Base, AlunoDB, AvaliadorDB, AcaoDB
import urllib.parse

# Configuração
USER = 'adminifcoins'
PASSWORD = 'GrandTheftAuto.30/10/2004'
PASSWORD_ESCAPED = urllib.parse.quote_plus(PASSWORD)  # Escapa caracteres especiais
HOST = 'localhost'
PORT = '5432'
DB_NAME = 'ifcoins'

# Conecta no postgres "geral" para criar banco
engine_temp = create_engine(
    f'postgresql+psycopg2://{USER}:{PASSWORD_ESCAPED}@{HOST}:{PORT}/postgres',
    isolation_level='AUTOCOMMIT',
    echo=True
)

# Apagar banco antigo e criar novo
with engine_temp.connect() as conn:
    conn.execute(text(f'DROP DATABASE IF EXISTS {DB_NAME};'))
    conn.execute(text(f'CREATE DATABASE {DB_NAME};'))
    print(f"Banco {DB_NAME} recriado com sucesso.")

# Conectar no banco criado
engine = create_engine(
    f'postgresql+psycopg2://{USER}:{PASSWORD_ESCAPED}@{HOST}:{PORT}/{DB_NAME}',
    echo=True
)

# Criar tabelas
Base.metadata.create_all(engine)
print("Estrutura do banco criada com sucesso.")

# Criar sessão
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    print("Banco pronto para uso.")
