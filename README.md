# Avaliação Técnica - Engenheiro de Dados

Este repositório contém as respostas para a avaliação técnica de Engenheiro de Dados. Cada problema foi resolvido com foco em boas práticas, escalabilidade e clareza.

[Avaliação Técnica - Engenheiro de Dados.pdf](https://github.com/user-attachments/files/18404134/Avaliacao.Tecnica.-.Engenheiro.de.Dados.corrigida.pdf)


## Estrutura do Repositório
- `problema-1-dba`: Soluções para otimização de banco de dados.
- `problema-2-pipeline`: Implementação de um pipeline de dados.
- `problema-3-ci-cd`: Configuração de um pipeline CI/CD.
- `problema-4-modelagem`: Modelagem de banco de dados e scripts SQL.
- `problema-5-web-scraping`: Implementação de um scraper resiliente.
- `problema-6-aws`: Arquitetura para processamento em tempo real.
- `problema-7-monitoramento`: Monitoramento e alertas para pipelines.
- `problema-8-governanca`: Estratégias de governança e segurança de dados.
- `problema-9-data-lake`: Estruturação de um Data Lake e integração com Redshift.
- `tests`: Testes unitários para validar os códigos.

## Como Executar
1. Clone o repositório:
   ```bash
   git clone https://github.com/samarcelomartins/engenheirodados-agromercantil.git
   cd avaliacao-engenheiro-dados

___________
# Problema 1 - Banco de Dados (DBA)

## Descrição
Sua empresa possui um banco de dados PostgreSQL com uma tabela de logs que cresce em 1 milhão de linhas por dia. Atualmente, as consultas realizadas nessa tabela estão extremamente lentas.

### Tarefas
1. Proponha uma solução que otimize a performance para consultas de logs recentes (últimos 7 dias) sem degradar a consulta de logs antigos.
2. Explique como você implementaria:
   - Particionamento de tabelas
   - Estratégia de indexação
   - Backup e manutenção regular da tabela.


## Solução
A solução proposta inclui particionamento de tabelas por data, criação de índices nos campos de data e nos campos mais consultados, além de uma rotina de backup diário e limpeza de dados antigos.

### Testes Unitários
Para garantir que a implementação está correta, foram criados testes unitários usando pgTAP ou Python. Os testes verificam a criação das tabelas particionadas, a criação dos índices e a execução das rotinas de backup e manutenção.

Para mais detalhes, consulte o arquivo `tests.sql` ou `test_dba.py` no diretório `tests`.

### Implementação

- **Particionamento de Tabelas**:
```sql
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
```
