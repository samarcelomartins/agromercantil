# Solução Proposta:
## Modelo ER (Entidade-Relacionamento):

1. Entidades principais:
* clientes: Informações dos clientes (id, nome, email, etc.).
* produtos: Informações sobre os produtos (id, nome e preco).
* pedidos: Representa uma compra realizada por um cliente (id, cliente_id (chave estrangeira para Clientes), data_pedidonome, preço, etc.).
* itens_pedido: Produtos comprados em um pedido específico (id, pedido_id (chave estrangeira para Pedidos), produto_id (chave estrangeira para Produtos), quantidade e preco_unitario).

2. Relacionamentos:
* Um cliente pode fazer vários pedidos (1:N).
* Um pedido pode conter vários produtos, e um produto pode estar em vários pedidos (N:N, com tabela intermediária itens_pedido).

3. Diagrama Relacional (Explicação textual):
* clientes (id, nome, email).
* produtos (id, nome, preco).
* pedidos (id, cliente_id, data).
* itens_pedido (id, pedido_id, produto_id, quantidade).

## Explicação dos Scripts SQL
Retornar os Produtos Mais Vendidos:

Usamos SUM(oi.quantidade) para somar a quantidade vendida de cada produto.
Fazemos um INNER JOIN entre order_items e products para obter o nome do produto.
Agrupamos pelo nome do produto e ordenamos pelo total vendido em ordem decrescente.
Listar o Histórico de Compras de um Cliente Específico:

Selecionamos as informações do pedido (o.id, o.data_pedido), do produto (p.nome), e dos itens do pedido (oi.quantidade, oi.preco_unitario).
Calculamos o total (oi.quantidade * oi.preco_unitario) para cada linha.
Filtramos os pedidos pelo cliente_id específico.
Ordenamos os resultados pela data do pedido em ordem decrescente.
Calcular o Faturamento Mensal:

Usamos DATE_TRUNC('month', o.data_pedido) para agrupar os pedidos por mês.
Calculamos o faturamento mensal somando (SUM) o total de cada item do pedido (oi.quantidade * oi.preco_unitario).
Agrupamos pelo mês e ordenamos em ordem decrescente.
