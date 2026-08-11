--- Questão 1.1
SELECT
  COUNT(*) AS "Total de Linhas",
  MIN(DATE("created_at")) AS "Data Mínima",
  MAX(DATE("created_at")) AS "Data Máxima",
  MIN("total") AS "Valor Mínimo",
  ROUND(MAX("total")::numeric, 2) AS "Valor Máximo",
  ROUND(AVG("total")::numeric, 2) AS "Valor Médio"
FROM nauticals_orders;


