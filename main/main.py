# Arquivo para chamar a execução de todos os outros
#1. schema.py
from scripts.schema import create_schema
from ingestion.database import gerar_banco

def main():
    create_schema()


if __name__=="__main__":
    main()
    gerar_banco()