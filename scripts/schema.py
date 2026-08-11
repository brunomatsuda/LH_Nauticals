from pathlib import Path
from config.path import RAW_PATH

def create_schema() -> Path:
    arquivos = list(Path(RAW_PATH).glob("*.csv"))
    for i in arquivos:
        print(i)