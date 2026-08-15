--- Questão 1.1
SELECT
  COUNT(*) AS "Total de Linhas",
  MIN(DATE("created_at")) AS "Data Mínima",
  MAX(DATE("created_at")) AS "Data Máxima",
  MIN("total") AS "Valor Mínimo",
  ROUND(MAX("total")::numeric, 2) AS "Valor Máximo",
  ROUND(AVG("total")::numeric, 2) AS "Valor Médio"
FROM nauticals_orders;

--- Questão 3.2
select 
	(select count(*) from erp.public.customers) +
	(select count(*) from erp.public.orders) +
	(select count(*) from erp.public.order_items) +
	(select count(*) from erp.public.payments) as total;
-> 251,864 linhas totais

---Questão
