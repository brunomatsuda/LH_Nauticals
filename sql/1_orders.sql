-- Questão 1.1
SELECT
  COUNT(*) AS "Total de Linhas",
  MIN(DATE(created_at)) AS "Data Mínima",
  MAX(DATE(created_at)) AS "Data Máxima",
  MIN(total) AS "Valor Mínimo",
  ROUND(MAX(total), 2) AS "Valor Máximo",
  ROUND(AVG(total), 2) AS "Valor Médio"
FROM read_csv_auto('../data/raw/orders.csv')

/***Acredito que para uma análise preditiva seja válida,visto que os dados se extendem até o final de 2026. O Schema da tabela está bem estruturado, 
as colunas do tipo data estão em 'timestamp' e as colunas numéricas se encontram em 'double precision' .A coluna "total" possui outliers, visto queo valor médio é 28704.99 e o 
valor mínimo é 32.62.A coluna "salesperson_id", possui 24131 valores nulos e 24867 não nulos, acredito que primeiro precisariamos entender porque existem tantos valores nulos nesta coluna, 
pude averiguar e percebi que todas os vendedores com valores nulos foram feitaspor meio do e-commerce, porém existem "salesperson_id" 
com valores diferentes de null, e que também foram feitasno modelo e-commerce. Portanto antes de disponibilizar esses dados para downstream, eu verificaria esta pequena causa.***/