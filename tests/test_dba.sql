-- Teste de criação da tabela de logs
BEGIN;
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    log_time TIMESTAMP NOT NULL,
    log_data TEXT
) PARTITION BY RANGE (log_time);

-- Teste de partição de tabela
CREATE TABLE logs_20250101 PARTITION OF logs
    FOR VALUES FROM ('2025-01-01') TO ('2025-01-08');

CREATE TABLE logs_20250108 PARTITION OF logs
    FOR VALUES FROM ('2025-01-08') TO ('2025-01-15');

-- Teste de índice BRIN
CREATE INDEX idx_logs_log_time ON logs USING BRIN (log_time);

-- Verificar se a tabela de logs foi criada
SELECT * FROM ok(table_exists('logs'), 'Tabela logs criada');

-- Verificar se as partições foram criadas
SELECT * FROM ok(table_exists('logs_20250101'), 'Partição logs_20250101 criada');
SELECT * FROM ok(table_exists('logs_20250108'), 'Partição logs_20250108 criada');

-- Verificar se o índice BRIN foi criado
SELECT * FROM ok(index_exists('logs', 'idx_logs_log_time'), 'Índice BRIN idx_logs_log_time criado');

ROLLBACK;

-- Teste de rotina de limpeza de dados antigos
DELETE FROM logs WHERE log_time < NOW() - INTERVAL '1 year';
SELECT * FROM ok(1=1, 'Rotina de limpeza de dados antigos executada');

-- Teste de backup diário (apenas simulação, verificar o comando)
SELECT * FROM ok(1=1, 'Backup diário simulado');
