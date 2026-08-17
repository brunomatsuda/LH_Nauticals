WITH faturamento_cliente AS (
    SELECT
        customer_id,
        SUM(total)                     AS faturamento_total,
        COUNT(id)                      AS frequencia,
        SUM(total) * 1.0 / COUNT(id)   AS ticket_medio
    FROM orders
    GROUP BY customer_id
),
diversidade_cliente AS (
    SELECT
        o.customer_id,
        COUNT(DISTINCT p.category_id) AS qtd_categorias
    FROM orders o
    JOIN order_items o_i     ON o_i.order_id = o.id
    JOIN product_variants pv ON pv.id = o_i.product_variant_id
    JOIN products p          ON p.id = pv.product_id
    GROUP BY o.customer_id
),
elite_ranking AS (
    SELECT
        f.customer_id,
        f.faturamento_total,
        f.frequencia,
        f.ticket_medio,
        d.qtd_categorias,
        ROW_NUMBER() OVER (
            ORDER BY f.ticket_medio DESC, f.customer_id ASC
        ) AS posicao
    FROM faturamento_cliente f
    JOIN diversidade_cliente d
        ON d.customer_id = f.customer_id
    WHERE d.qtd_categorias >= 13
),
top10 AS (
    SELECT *
    FROM elite_ranking
    WHERE posicao <= 10
),
categoria_top10 AS (
    SELECT
        p.category_id,
        SUM(o_i.quantity) AS total_itens
    FROM order_items o_i
    JOIN orders o             ON o.id = o_i.order_id
    JOIN product_variants pv  ON pv.id = o_i.product_variant_id
    JOIN products p           ON p.id = pv.product_id
    WHERE o.customer_id IN (SELECT customer_id FROM top10)
    GROUP BY p.category_id
)
SELECT *
FROM categoria_top10
ORDER BY total_itens DESC;