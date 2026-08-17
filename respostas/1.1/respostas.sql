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

---Questão 4.2
order_items.product_variant_id → product_variants.id → product_variants.product_id → products.id → products.category_id. 
Com essa cadeia, cada item vendido (order_items.quantity) fica associado a uma categoria, permitindo agrupar por category_id e somar quantity.

Contei COUNT(DISTINCT products.category_id) por customer_id (via join orders → order_items → product_variants → products), gerando a CTE diversidade_cliente. Depois apliquei WHERE qtd_categorias >= 13 sobre essa contagem, antes de rankear por ticket médio — ou seja, 
o filtro de elite é aplicado como pré-requisito, não como critério de ordenação.

O ranking (ROW_NUMBER() OVER (ORDER BY ticket_medio DESC, customer_id ASC)) foi calculado sobre os clientes já filtrados pela diversidade, e restrito a posicao <= 10 na CTE top10. Na Camada 3, o SUM(quantity) por categoria só considera order_items cujo orders.customer_id está contido nesse conjunto (WHERE customer_id IN (SELECT customer_id FROM top10)), 
garantindo que nenhum item de cliente fora do Top 10 entre na soma.

---Questão 5.2
Porque agrupar direto em orders só considera dias que têm registro de venda. Dias em que a loja abriu mas vendeu zero simplesmente não existem como linha na tabela — então eles não entram no GROUP BY nem no cálculo da média. A tabela de calendário garante que todo dia do período exista como linha, com ou sem venda, 
permitindo cruzar (LEFT JOIN) e forçar os dias "vazios" a aparecerem como zero.

A média ficaria inflada artificialmente. Sem o calendário, o denominador da média (quantidade de dias) só conta os dias com venda > 0, ignorando os dias zerados — isso foi exatamente o erro do estagiário, que fez o Domingo parecer ótimo (R$5.000 de média) quando, 
na verdade, muitos Domingos venderam zero e nunca entraram na conta.

---Questão 7.2
  Vela Mestra 1913

---Questão 7.3
  Uma matriz Usuário × Produto, com customer_id nas linhas e product_id nas colunas. O valor de cada célula é binário: 1 se o cliente comprou aquele produto ao menos uma vez,
  0 caso contrário — quantidade comprada foi ignorada, só presença/ausência (por isso apliquei drop_duplicates antes de montar o pivot).

  Cada produto vira um vetor de 2000 posições (um por cliente), com 1 nas posições dos clientes que o compraram. A similaridade de cosseno mede o ângulo entre dois vetores — quanto mais próximo de 1,
  mais os dois produtos são comprados pelos mesmos clientes. Não mede se os produtos são parecidos em características (categoria, preço, função), só o padrão de co-compra.

  É muito sensível à fragmentação de catálogo. Descobrimos isso na prática: existem 42 produtos diferentes chamados "Defensa Náutica" (provavelmente deveriam ser variantes de um único produto), e isso diluiu o sinal de co-compra entre eles — nenhuma Defensa individual teve compradores suficientes em comum com o Motor de Popa para aparecer no top 5, 
  mesmo que a categoria como um todo provavelmente tivesse. O método assume que cada product_id é uma entidade coesa, e falha quando o cadastro de produtos não reflete isso.