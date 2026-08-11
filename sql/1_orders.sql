-- Questão 1.1
SELECT
  COUNT(*) AS "Total de Linhas",
  MIN(DATE(created_at)) AS "Data Mínima",
  MAX(DATE(created_at)) AS "Data Máxima",
  MIN(total) AS "Valor Mínimo",
  ROUND(MAX(total), 2) AS "Valor Máximo",
  ROUND(AVG(total), 2) AS "Valor Médio"
FROM read_csv_auto('../data/raw/orders.csv')
