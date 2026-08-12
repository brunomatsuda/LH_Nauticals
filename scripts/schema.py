from pathlib import Path
from config.path import RAW_PATH
from datetime import datetime
from itertools import islice
import csv


def verificar_dtype(dicionario:dict) -> str:
    print(dicionario)


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

            verificar_dtype(dict_schema)  