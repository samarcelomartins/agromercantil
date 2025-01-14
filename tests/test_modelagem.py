def test_query_produtos_mais_vendidos(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("""
        CREATE TABLE produtos (id SERIAL, nome TEXT);
        INSERT INTO produtos (id, nome) VALUES (1, 'Produto A'), (2, 'Produto B');
    """)
    cursor.execute("""
        SELECT nome FROM produtos WHERE id = 1;
    """)
    result = cursor.fetchone()
    assert result[0] == 'Produto A'
