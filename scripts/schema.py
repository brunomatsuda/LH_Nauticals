from pathlib import Path
from config.path import RAW_PATH
from datetime import datetime
from itertools import islice
import csv


def is_bool(valor: list[str]) -> bool | None:
    if not valor:
        return None
    
    return all(str(v) in ("true", "false") for v in valor)
        

def is_int(valor: list[str]) -> bool | None:
    if not valor:
        return None

    for v in valor:
        if not v.isdigit():
            return False
        if len(v) > 9: # Para evitar leitura de colunas telefônicas
            return False
    return True


def is_float(valor: list[str]) -> bool | None:
    if not valor:
        return None

    for v in valor:
        try:
            float(v)
        except ValueError:
            return False
        
    return True


def _try_parse_date(valor: str, fmt: str) -> bool:
    try:
        datetime.strptime(valor, fmt)
        return True
    except ValueError:
        return False
    

def is_date(valor: list[str]) -> bool | None:
    if not valor:
        return None

    formatos_date = (
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%d.%m.%Y",
        "%Y.%m.%d",
    )

    formatos_datetime = (
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%d-%m-%Y %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M",
    )

    if all(any(_try_parse_date(str(v).strip(), fmt) for fmt in formatos_date) for v in valor):
        return "DATE"

    if all(any(_try_parse_date(str(v).strip(), fmt) for fmt in formatos_datetime) for v in valor):
        return "DATETIME"

    return None

    
def verificar_dtype(valor: list[str]) -> str:
    date_return=""
    if is_bool(valor):
        return "BOOLEAN"
    if is_int(valor):
        return "INTEGER"
    if is_float(valor):
        return "DOUBLE PRECISION"

    tipo_data = is_date(valor)
    if tipo_data:
        return tipo_data
    return None
    

def create_schema() -> Path:
    arquivos = list(Path(RAW_PATH).glob("*.csv"))

    for arquivo in arquivos:
        arquivo = arquivo.name
        caminho = RAW_PATH/arquivo

        print(f"-------------------------- \033[92m Lendo o arquivo {arquivo}\033[0m --------------------------")

        with open(caminho, newline="", encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            dict_schema = {} # Dicionário que irá armazena colunas(key) e valores(values) de todos os csv`s

            for linha in islice(leitor, 5):
                for chave, valor in linha.items():
                    if chave not in dict_schema:
                        dict_schema[chave] = [valor.strip().lower()]
                    else:
                        dict_schema[chave].append(valor.strip().lower())


            for coluna, valor in dict_schema.items(): 
                tipo = verificar_dtype(valor)

                print(coluna, tipo)