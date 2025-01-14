# Solução Proposta:
Modelo ER (Entidade-Relacionamento):

1. Entidades principais:
* clientes: Informações dos clientes (nome, email, etc.).
* produtos: Informações sobre os produtos (nome, preço, etc.).
* pedidos: Representa uma compra realizada por um cliente.
* itens_pedido: Produtos comprados em um pedido específico.

2. Relacionamentos:
* Um cliente pode fazer vários pedidos (1:N).
* Um pedido pode conter vários produtos, e um produto pode estar em vários pedidos (N:N, com tabela intermediária itens_pedido).

3. Diagrama Relacional (Explicação textual):
* clientes (id, nome, email).
* produtos (id, nome, preco).
* pedidos (id, cliente_id, data).
* itens_pedido (id, pedido_id, produto_id, quantidade).
