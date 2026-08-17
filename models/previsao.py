from pathlib import Path
import pandas as pd
import numpy as np

from config.path import BASE_DIR, RAW_PATH, SCHEMA_SQL

# ============================================================
# 0. DIRETÓRIO DE SAÍDA (dentro do projeto, não mais /mnt/...)
# ============================================================
OUTPUT_DIR = BASE_DIR / 'data/processed'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. CARGA DOS DATASETS
# ============================================================
orders = pd.read_csv(RAW_PATH / 'orders.csv')
order_items = pd.read_csv(RAW_PATH / 'order_items.csv')
products = pd.read_csv(RAW_PATH / 'products.csv')
variants = pd.read_csv(RAW_PATH / 'product_variants.csv')

# ============================================================
# 2. FILTRAR O PRODUTO ALVO (atenção: nome duplicado no cadastro)
# ============================================================
target_products = products[products['name'] == 'Bússola de Bordo 702']
print("Produtos encontrados com esse nome:")
print(target_products[['id', 'name']])
print()

target_ids = target_products['id'].tolist()

# ============================================================
# 3. UNIFICAR O DATASET (cadeia de chaves)
#    order_items -> product_variants -> products
#    order_items -> orders (para pegar a data)
# ============================================================
variants_target = variants[variants['product_id'].isin(target_ids)]

df = order_items.merge(
    variants_target[['id', 'product_id']],
    left_on='product_variant_id', right_on='id',
    suffixes=('', '_variant')
)

df = df.merge(
    orders[['id', 'placed_at', 'status']],
    left_on='order_id', right_on='id',
    suffixes=('', '_order')
)

df['placed_at'] = pd.to_datetime(df['placed_at'])
df['ano_mes'] = df['placed_at'].dt.to_period('M')

print(f"Total de linhas no dataset unificado: {len(df)}")
print(f"Status de pedidos presentes: {df['status'].unique()}")
print()

df.to_csv(OUTPUT_DIR / 'dataset_unificado.csv', index=False)

# ============================================================
# 4. DECISÃO DE NEGÓCIO: quais status contam como venda real?
#    'cancelled' e 'draft' não representam demanda efetivada.
#    Mantemos 'paid' e 'confirmed'.
# ============================================================
df_valid = df[df['status'].isin(['paid', 'confirmed'])].copy()
print(f"Linhas após filtro de status válido: {len(df_valid)} (de {len(df)})")

# ============================================================
# 5. AGREGAÇÃO MENSAL DE VENDAS (soma de quantity por mês)
# ============================================================
vendas_mensais = df_valid.groupby('ano_mes')['quantity'].sum().reset_index()
vendas_mensais.columns = ['ano_mes', 'quantidade_vendida']
vendas_mensais = vendas_mensais.sort_values('ano_mes').reset_index(drop=True)

print("\nSérie mensal completa:")
print(vendas_mensais.to_string(index=False))

# ============================================================
# 6. COMPLETAR MESES SEM VENDA (gaps = 0)
# ============================================================
full_range = pd.period_range(
    start=vendas_mensais['ano_mes'].min(),
    end=vendas_mensais['ano_mes'].max(),
    freq='M'
)
serie_completa = vendas_mensais.set_index('ano_mes').reindex(full_range, fill_value=0)
serie_completa.index.name = 'ano_mes'
serie_completa = serie_completa.reset_index()

print(f"\nMeses no range: {len(full_range)} | Meses com venda registrada: {len(vendas_mensais)}")
print(f"Meses preenchidos com 0: {len(full_range) - len(vendas_mensais)}")

# ============================================================
# 7. SPLIT TREINO / TESTE
#    Treino: até 31/12/2025 | Teste: Q1 2026 (Jan, Fev, Mar)
# ============================================================
teste_periodos = [pd.Period('2026-01', 'M'), pd.Period('2026-02', 'M'), pd.Period('2026-03', 'M')]

serie_completa = serie_completa.set_index('ano_mes')

# ============================================================
# 8. BASELINE: MÉDIA MÓVEL DOS ÚLTIMOS 3 MESES
#    (usando apenas dados anteriores à data prevista)
# ============================================================
previsoes = []
for periodo_alvo in teste_periodos:
    janela = [periodo_alvo - i for i in range(1, 4)]  # 3 meses anteriores
    valores_janela = [serie_completa.loc[m, 'quantidade_vendida'] for m in janela if m in serie_completa.index]
    previsao = np.mean(valores_janela)
    real = serie_completa.loc[periodo_alvo, 'quantidade_vendida'] if periodo_alvo in serie_completa.index else np.nan
    previsoes.append({
        'mes': str(periodo_alvo),
        'meses_usados_na_media': [str(m) for m in janela],
        'valores_janela': valores_janela,
        'previsao': round(previsao, 2),
        'real': real
    })

resultado = pd.DataFrame(previsoes)
print("\n" + "="*70)
print("PREVISÃO Q1 2026 vs REAL")
print("="*70)
print(resultado[['mes', 'previsao', 'real']].to_string(index=False))
print()
for p in previsoes:
    print(f"{p['mes']}: média de {p['meses_usados_na_media']} = {p['valores_janela']} -> previsão = {p['previsao']}")

# ============================================================
# 9. MÉTRICA: MAE
# ============================================================
resultado['erro_absoluto'] = (resultado['previsao'] - resultado['real']).abs()
mae = resultado['erro_absoluto'].mean()
print(f"\nMAE (Q1 2026): {mae:.2f} unidades")
print(resultado[['mes','previsao','real','erro_absoluto']].to_string(index=False))

resultado.to_csv(OUTPUT_DIR / 'previsao_vs_real.csv', index=False)
serie_completa.to_csv(OUTPUT_DIR / 'serie_mensal_completa.csv')

print(f"\nArquivos salvos em: {OUTPUT_DIR}")