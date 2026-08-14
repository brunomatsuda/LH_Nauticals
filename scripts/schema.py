from pathlib import Path
from config.path import RAW_PATH
from datetime import datetime
from itertools import islice
import csv


def is_special(valor: list[str], coluna: list[str]) -> bool | None: # captura valores 'extraodinários' como telefone, cpf.....
    if not valor:
        return None
    
    special = {
        "cpf",
        "cnpj",
        "telefone",
        "celular",
        "cep",
        "sku",
        "codigo_barras",
        "ean",
        "matricula",
        "phone",
        "state_registration"
    }
    if coluna in special:
        return True


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


def is_text(valor: list[str]) -> bool | None:
    if not valor:
        return None
    return True

    
def verificar_dtype(valor: list[str], coluna:list[str]) -> str:
    if is_special(valor, coluna):
        return "TEXT"
    if is_bool(valor):
        return "BOOLEAN"
    if is_int(valor):
        return "INTEGER"
    if is_float(valor):
        return "DOUBLE PRECISION"

    tipo_data = is_date(valor)
    if tipo_data:
        return tipo_data

    if is_text(valor):
        return "TEXT"
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

            for linha in islice(leitor, 2):
                for chave, valor in linha.items():
                    chave = chave.strip().lower()
                    valor = valor.strip().lower()
                    if not valor:
                        continue

                    if chave not in dict_schema:
                        dict_schema[chave] = [valor]
                    else:
                        dict_schema[chave].append(valor)

            for coluna, valor in dict_schema.items(): 
                tipo = verificar_dtype(valor, coluna)

                print(coluna, tipo)