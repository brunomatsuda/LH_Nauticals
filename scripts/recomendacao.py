import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
# 1. CARGA DOS DATASETS
# ============================================================
orders = pd.read_csv('/mnt/user-data/uploads/orders.csv')
order_items = pd.read_csv('/mnt/user-data/uploads/order_items.csv')
products = pd.read_csv('/mnt/user-data/uploads/products.csv')
variants = pd.read_csv('/mnt/user-data/uploads/product_variants.csv')

# ============================================================
# 2. UNIFICAR: order_items -> orders (customer_id) 
#               order_items -> product_variants -> products
# ============================================================
df = order_items.merge(
    orders[['id', 'customer_id', 'status']],
    left_on='order_id', right_on='id',
    suffixes=('', '_order')
)

df = df.merge(
    variants[['id', 'product_id']],
    left_on='product_variant_id', right_on='id',
    suffixes=('', '_variant')
)

# Filtro de negócio: só considerar vendas efetivadas (mesma lógica dos cases anteriores)
df = df[df['status'].isin(['paid', 'confirmed'])].copy()

print(f"Total de linhas (item de venda válido): {len(df)}")
print(f"Clientes distintos: {df['customer_id'].nunique()}")
print(f"Produtos distintos: {df['product_id'].nunique()}")

# ============================================================
# 3. MATRIZ DE INTERAÇÃO USUÁRIO x PRODUTO (binária: presença/ausência)
# ============================================================
interacoes = df[['customer_id', 'product_id']].drop_duplicates()

matriz = interacoes.pivot_table(
    index='customer_id',
    columns='product_id',
    aggfunc=lambda x: 1,
    fill_value=0
)

print(f"\nDimensão da matriz Usuário x Produto: {matriz.shape}")
matriz.to_csv('matriz_usuario_produto.csv')

# ============================================================
# 4. SIMILARIDADE DE COSSENO ENTRE PRODUTOS
#    (produto x produto, com base em quais clientes compraram cada um)
# ============================================================
# Transpor: linhas = produtos, colunas = clientes
matriz_produtos = matriz.T  # shape: (500 produtos, 2000 clientes)

sim_matrix = cosine_similarity(matriz_produtos)
sim_df = pd.DataFrame(
    sim_matrix,
    index=matriz_produtos.index,
    columns=matriz_produtos.index
)

print(f"\nMatriz de similaridade produto x produto: {sim_df.shape}")

# ============================================================
# 5. RANKING DE PRODUTOS SIMILARES AO "Motor de Popa 1949"
# ============================================================
produto_ref_id = products.loc[products['name'] == 'Motor de Popa 1949', 'id'].values[0]
print(f"\nID do produto de referência: {produto_ref_id}")

similares = sim_df[produto_ref_id].drop(index=produto_ref_id)  # remove o próprio produto
top5 = similares.sort_values(ascending=False).head(5)

# Trazer os nomes dos produtos
top5_df = top5.reset_index()
top5_df.columns = ['product_id', 'similaridade_cosseno']
top5_df = top5_df.merge(products[['id', 'name']], left_on='product_id', right_on='id')
top5_df = top5_df[['name', 'product_id', 'similaridade_cosseno']]
top5_df['similaridade_cosseno'] = top5_df['similaridade_cosseno'].round(4)

print("\n" + "="*60)
print("TOP 5 PRODUTOS MAIS SIMILARES A 'Motor de Popa 1949'")
print("="*60)
print(top5_df.to_string(index=False))

top5_df.to_csv('top5_recomendados.csv', index=False)