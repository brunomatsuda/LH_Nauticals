from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1] #/home/bruno/lh_nautical_csv
RAW_PATH = BASE_DIR/'data/raw'
print(BASE_DIR)