-- Supondo uma tabela de logs existente chamada "logs"
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    log_time TIMESTAMP NOT NULL,
    log_data TEXT
) PARTITION BY RANGE (log_time);

-- Criando tabelas de partição para cada semana
CREATE TABLE logs_20250101 PARTITION OF logs
    FOR VALUES FROM ('2025-01-01') TO ('2025-01-08');

CREATE TABLE logs_20250108 PARTITION OF logs
    FOR VALUES FROM ('2025-01-08') TO ('2025-01-15');

-- Índice na coluna de tempo dos logs
CREATE INDEX idx_logs_log_time ON logs (log_time);

-- Backup diário usando pg_dump
pg_dump -U postgres -F c -b -v -f "/path/to/backup/backup_$(date +\%Y\%m\%d).dump" mydatabase

-- Limpeza de dados antigos
DELETE FROM logs WHERE log_time < NOW() - INTERVAL '1 year';
