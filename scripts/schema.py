from pathlib import Path
from config.path import RAW_PATH, SCHEMA_SQL
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
        "state_registration",
        "tax_id",
        "nfe_access_key",
        "barcode_ean"
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
        
    if len(valor) <10:
        return True
    else:
        return False


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
        return "TIMESTAMP"

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
    

def nome_tabela(arquivo: str) -> str:
    return Path(arquivo).stem.strip().lower().replace(" ", "_").replace("-", "_")


def create_schema(output_file: Path | str = None, sample_size: int = 10) -> Path:
    arquivos = list(Path(RAW_PATH).glob("*.csv"))
 
    if output_file is None:
        output_file = Path(SCHEMA_SQL) / "schema.sql"
    else:
        output_file = Path(output_file)
 
    output_file.parent.mkdir(parents=True, exist_ok=True)
 
    with open(output_file, "w", encoding="utf-8") as sql_file:
        for arquivo_path in arquivos:
            arquivo = arquivo_path.name
            caminho = RAW_PATH / arquivo
 
            #print(f"-------------------------- \033[92m Lendo o arquivo {arquivo}\033[0m --------------------------")
            sql_file.write(f"-- Lendo o arquivo {arquivo}\n")
 
            with open(caminho, newline="", encoding="utf-8") as f:
                leitor = csv.DictReader(f)
                dict_schema = {}  # Dicionário que irá armazena colunas(key) e valores(values) de todos os csv`s
 
                for linha in islice(leitor, sample_size):
                    for chave, valor in linha.items():
                        chave = chave.strip().lower()
                        valor = valor.strip().lower() if valor else valor
                        if not valor:
                            dict_schema[chave] = [valor]
 
                        if chave not in dict_schema:
                            dict_schema[chave] = [valor]
                        else:
                            dict_schema[chave].append(valor)
 
            tabela = nome_tabela(arquivo)
            sql_file.write(f"CREATE TABLE IF NOT EXISTS {tabela} (\n")
 
            colunas_sql = []
            for coluna, valor in dict_schema.items():
                tipo = verificar_dtype(valor, coluna)
                #print(coluna, tipo)
                colunas_sql.append(f'    "{coluna}" {tipo}')
 
            sql_file.write(",\n".join(colunas_sql))
            sql_file.write("\n);\n\n")
 
    print(f"\nArquivo gerado com sucesso: {output_file.resolve()}")
    return output_file
