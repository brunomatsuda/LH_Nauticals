


-- ============================================================
-- CAMADA 1: Dimensão de datas (calendário completo do período)
-- ============================================================
WITH calendario AS (
    SELECT generate_series(
        (SELECT MIN(placed_at::date) FROM orders WHERE channel = 'pos'),
        (SELECT MAX(placed_at::date) FROM orders WHERE channel = 'pos'),
        '1 day'::interval
    )::date AS data
),

-- ============================================================
-- CAMADA 2: Vendas diárias, apenas lojas físicas (pos)
-- ============================================================
vendas_diarias AS (
    SELECT
        placed_at::date AS data,
        SUM(total)      AS venda_dia
    FROM orders
    WHERE channel = 'pos'
    GROUP BY placed_at::date
),

-- ============================================================
-- CAMADA 3: Cruzamento calendário x vendas (dias sem venda = 0)
-- ============================================================
calendario_vendas AS (
    SELECT
        c.data,
        COALESCE(v.venda_dia, 0)::numeric AS venda_dia
    FROM calendario c
    LEFT JOIN vendas_diarias v
        ON v.data = c.data
),

-- ============================================================
-- CAMADA 4: Nome do dia da semana em português
-- ============================================================
calendario_dia_semana AS (
    SELECT
        data,
        venda_dia,
        CASE EXTRACT(DOW FROM data)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
        END AS dia_semana
    FROM calendario_vendas
)

-- ============================================================
-- RESULTADO FINAL: média de vendas por dia da semana
-- ============================================================
SELECT
    dia_semana,
    ROUND(AVG(venda_dia), 2) AS media_vendas,
    COUNT(*)                 AS qtd_dias_no_periodo
FROM calendario_dia_semana
GROUP BY dia_semana
ORDER BY media_vendas ASC;