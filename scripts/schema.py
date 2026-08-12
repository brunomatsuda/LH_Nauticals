from pathlib import Path
from config.path import RAW_PATH
from datetime import datetime
from itertools import islice
import csv


def is_bool(valor: list[str]) -> list[str]:
    if not valor:
        return None
    
    if all(str(v) in ("true", "false") for v in valor):
        return "BOOLEAN"


def is_int():
    pass

    
def verificar_dtype(valor: list[str]) -> str:
    #print(f"Verificando os valores: {valor}")
    return is_bool(valor)


def create_schema() -> Path:
    arquivos = list(Path(RAW_PATH).glob("*.csv"))

    for arquivo in arquivos:
        arquivo = arquivo.name
        caminho = RAW_PATH/arquivo

        print(f"-------------------------- \033[92m Lendo o arquivo {arquivo}\033[0m --------------------------")

        with open(caminho, newline="", encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            dict_schema = {}

            for linha in islice(leitor, 2):
                for chave, valor in linha.items():
                    if chave not in dict_schema:
                        dict_schema[chave] = [valor.strip().lower()]
                    else:
                        dict_schema[chave].append(valor.strip().lower())

            verificar_dtype(dict_schema) # Dicionário que irá armazena colunas(key) e valores(values) de todos os csv`s

            for coluna, valor in dict_schema.items(): 
                tipo = verificar_dtype(valor)

                print(coluna, tipo)