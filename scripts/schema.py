from pathlib import Path
from config.path import RAW_PATH
from datetime import datetime
from itertools import islice
import csv


def is_bool(valor: list[str]) -> list[str] | None:
    if not valor:
        return None
    
    return all(str(v) in ("true", "false") for v in valor)
        

def is_int(valor: list[str]) -> list[str] | None:
    if not valor:
        return None

    for v in valor:
        if not v.isdigit():
            return False
        if len(v) > 9: # Para evitar leitura de colunas telefônicas
            return False
    return True


def is_float(valor: list[str]) -> list[str] | None:
    if not valor:
        return None

    for v in valor:
        try:
            float(v)
        except ValueError:
            return False
        
    return True


def is_date(valor: list[str]) -> list[str] | None:
    if not valor:
        return None

    formatos_date = (
        "%Y-%m-%d", "%d/%m/%Y",
        "%d-%m-%Y", "%Y/%m/%d",
        "%d.%m.%Y","%Y.%m.%d",
    )
    for v in valor:
        for dt_formato in formatos_date:
            try:
                datetime.strptime(v, dt_formato)
                return True
            except ValueError:
                pass
    return False

    
def verificar_dtype(valor: list[str]) -> str:
    if is_bool(valor):
        return "BOOLEAN"
    if is_int(valor):
        return "INTEGER"
    if is_float(valor):
        return "DOUBLE PRECISION"
    if is_date(valor):
        return "DATE"
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