import csv
import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg
from config.path import SCHEMA_SQL, RAW_PATH

# ---------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "erp")


SCHEMA_PATH = SCHEMA_SQL / "schema.sql"
CSV_FOLDER = RAW_PATH  

# ---------------------------------------------------------------------
# Criação do banco de dados
# ---------------------------------------------------------------------
def criar_banco():
    conn = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
    )
    conn.autocommit = True

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,)
        )
        existe = cursor.fetchone()
        if not existe:
            cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f"Banco '{DB_NAME}' criado.")
        else:
            print(f"Banco '{DB_NAME}' já existe, seguindo em frente.")
            exit

    conn.close()

# ---------------------------------------------------------------------
# exe schema.sql
# ---------------------------------------------------------------------
def criar_tabelas(conn):
    with open(SCHEMA_PATH, "r", encoding="utf-8") as arquivo:
        schema = arquivo.read()
 
    with conn.cursor() as cursor:
        cursor.execute(schema)
 
    conn.commit()
    print("Schema executado (tabelas criadas).")


# ---------------------------------------------------------------------
# verificação de colunas já existentes
# ---------------------------------------------------------------------
def tabela_tem_dados(conn, tabela: str) -> bool:
    with conn.cursor() as cursor:
        cursor.execute(f'SELECT EXISTS (SELECT 1 FROM "{tabela}" LIMIT 1)')
        (existe,) = cursor.fetchone()
    return existe
 
 
def carregar_csv(conn, tabela: str, caminho_csv: Path):
    if tabela_tem_dados(conn, tabela):
        print(f"  Tabela '{tabela}' já possui dados")
        return
 
    with open(caminho_csv, "r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        header = next(leitor)
 
    colunas = ", ".join(f'"{col.strip()}"' for col in header)
    copy_sql = f'COPY "{tabela}" ({colunas}) FROM STDIN WITH CSV HEADER'
 
    with conn.cursor() as cursor:
        with open(caminho_csv, "r", encoding="utf-8") as arquivo:
            with cursor.copy(copy_sql) as copy:
                while dados := arquivo.read(8192):
                    copy.write(dados)
 
    conn.commit()
    print("  OK.")



# ---------------------------------------------------------------------
# Mapeamento de colunas
# ---------------------------------------------------------------------
def carregar_csv(conn, tabela: str, caminho_csv: Path):
    if tabela_tem_dados(conn, tabela):
        print(f"  Tabela '{tabela}' já possui dados, pulando (evita duplicação).")
        return

    with open(caminho_csv, "r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        header = next(leitor)

    colunas = ", ".join(f'"{col.strip()}"' for col in header)
    copy_sql = f'COPY "{tabela}" ({colunas}) FROM STDIN WITH CSV HEADER'

    with conn.cursor() as cursor:
        with open(caminho_csv, "r", encoding="utf-8") as arquivo:
            with cursor.copy(copy_sql) as copy:
                while dados := arquivo.read(8192):
                    copy.write(dados)

    conn.commit()


# ---------------------------------------------------------------------
# Execução
# ---------------------------------------------------------------------
def carregar_todos_csvs(conn):
    csvs = sorted(CSV_FOLDER.glob("*.csv"))

    if not csvs:
        print(f"Nenhum CSV encontrado em {CSV_FOLDER}")
        return

    for caminho_csv in csvs:
        tabela = caminho_csv.stem  # nome do arquivo sem ".csv"
        print(f"Carregando {caminho_csv.name} -> tabela '{tabela}'...")
        try:
            carregar_csv(conn, tabela, caminho_csv)
            print(f"  OK.")
        except Exception as e:
            conn.rollback()
            print(f"  ERRO ao carregar {caminho_csv.name}: {e}")


# ---------------------------------------------------------------------
# main
# ---------------------------------------------------------------------
def gerar_banco():
    criar_banco()

    conn = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    criar_tabelas(conn)
    carregar_todos_csvs(conn)

    conn.close()
    print("Ingestão concluída.")


