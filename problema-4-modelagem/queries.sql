-- Script SQL para Retornar os Produtos Mais Vendidos
SELECT 
    p.nome AS produto,
    SUM(oi.quantidade) AS total_vendido
FROM 
    order_items oi
INNER JOIN 
    products p ON oi.produto_id = p.id
GROUP BY 
    p.nome
ORDER BY 
    total_vendido DESC;

-- Script SQL para Listar o Histórico de Compras de um Cliente Específico
SELECT 
    o.id AS pedido_id,
    o.data_pedido,
    p.nome AS produto,
    oi.quantidade,
    oi.preco_unitario,
    (oi.quantidade * oi.preco_unitario) AS total
FROM 
    orders o
INNER JOIN 
    order_items oi ON o.id = oi.pedido_id
INNER JOIN 
    products p ON oi.produto_id = p.id
WHERE 
    o.cliente_id = ? -- Substitua pelo ID do cliente específico
ORDER BY 
    o.data_pedido DESC;

-- Script SQL para Calcular o Faturamento Mensal
SELECT 
    DATE_TRUNC('month', o.data_pedido) AS mes,
    SUM(oi.quantidade * oi.preco_unitario) AS faturamento_mensal
FROM 
    orders o
INNER JOIN 
    order_items oi ON o.id = oi.pedido_id
GROUP BY 
    mes
ORDER BY 
    mes DESC;
