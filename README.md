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

### Testes Unitários
Para garantir que a implementação está correta, foram criados testes unitários usando pgTAP ou Python. Os testes verificam a criação das tabelas particionadas, a criação dos índices e a execução das rotinas de backup e manutenção.

Para mais detalhes, consulte o arquivo `tests.sql` ou `test_dba.py` no diretório `tests`.

_________

## Problema 2 - Pipeline de Dados

## Descrição 
Você está criando um pipeline que deve:
- Ler dados brutos de sensores IoT armazenados no S3.
- Processar os dados em lotes (batch processing).
- Carregar os resultados no Redshift para análises futuras.

### Tarefas
1. Desenhe um diagrama arquitetural que represente o pipeline.
2. Liste os principais desafios técnicos que você enfrentaria e como resolveria cada um.
3. Escreva um script em Python que implemente a etapa de leitura do S3 e aplicação de uma transformação simples (ex.: cálculo de média de um campo).

## Solução

### Diagrama

(Representação textual)
1. Sensores → S3 (raw)
2. AWS Glue/EMR → S3 (curated)
3. Dados prontos → Amazon Redshift

![Diagrama](https://github.com/user-attachments/assets/a2bde838-09a6-4bbe-8230-c602bef889f9)

### Principais Desafios Técnicos e Soluções

1. Conectividade e Autenticação com S3:
* Desafio: Garantir que o script tenha acesso seguro ao bucket S3.
* Solução: Utilizar credenciais IAM seguras e configurar políticas de acesso apropriadas.

2. Processamento em Lotes (Batch Processing):
* Desafio: Gerenciar grandes volumes de dados e garantir que o processamento seja eficiente.
* Solução: Utilizar frameworks de processamento em lote como Apache Spark ou AWS Glue para otimizar o processamento podendo configurar paralelismo no Glue e escalabilidade no EMR

3. Carregamento no Redshift:
* Desafio: Garantir que os dados sejam carregados de forma eficiente e sem erros.
* Solução: Utilizar a funcionalidade de COPY do Redshift para carregar dados em massa e configurar monitoramento para detectar e corrigir erros.

4. Confiabilidade:
* Desafio: Garantir a integridade dos dados mesmo em caso de falhas.
* Solução: Implementar reprocessamento automático e checkpoints com mecanismos de controle de versão e validação de dados para garantir que apenas dados consistentes sejam processados.

5. Formato de dados:
* Desafio: Sensores podem gerar dados em formatos variados (CSV, JSON, etc.).
* Solução: Unificar para um formato eficiente (ex.: Parquet ou ORC) no processamento.

### Script Python para Leitura do S3 e Transformação Simples
```
import boto3
import pandas as pd
import io

# Configurações do S3
s3_bucket = 'nome-do-seu-bucket'
s3_key = 'caminho/para/seu/arquivo.csv'

# Função para ler dados do S3
def read_s3_data(bucket, key):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read()
    df = pd.read_csv(io.BytesIO(data))
    return df

# Função para calcular a média de um campo
def calculate_average(df, column_name):
    return df[column_name].mean()

def main():
    # Ler os dados do S3
    df = read_s3_data(s3_bucket, s3_key)
    print("Dados lidos do S3:")
    print(df.head())

    # Calcular a média de um campo específico
    average_value = calculate_average(df, 'nome_da_coluna')
    print(f"A média do campo 'nome_da_coluna' é: {average_value}")

    # Salvar resultado no S3 (curated)
    resultado = pd.DataFrame({'sensor': ['media'], 'valor': [media]})
    resultado.to_csv('/tmp/resultado.csv', index=False)

    s3.upload_file('/tmp/resultado.csv', s3_bucket, 'curated/resultado.csv')


if __name__ == "__main__":
    main()
```
 ### Carregamento no Redshift:
Exemplo de comando SQL para carregar o arquivo processado do S3 no Redshift:
```sql
COPY minha_tabela
FROM 's3://meu-bucket/curated/resultado.csv'
IAM_ROLE 'arn:aws:iam::123456789012:role/MeuRole'
CSV
IGNOREHEADER 1
REGION 'us-west-2';
```

### Testes Unitários

Iremos utilizar a biblioteca unittest do Python. O teste verificará se o script de leitura do S3 e a aplicação da transformação simples (cálculo da média de um campo) estão funcionando corretamente.

Para executar os testes, você pode rodar o seguinte comando no terminal:
```
python -m unittest problema-2-pipeline/test_pipeline.py
```
Para mais detalhes, consulte o arquivo `tests_pipeline.py` no diretório `tests`.

_________

## Problema 3 - CI/CD e DevOps

## Descrição
Sua equipe usa o Airflow para gerenciar pipelines de dados. Você precisa configurar um pipeline CI/CD que:
- Valide mudanças no código do Airflow antes do deploy.
- Realize testes automatizados em DAGs (Directed Acyclic Graphs).
- Envie alertas para o time se algo falhar durante o deploy.

## Tarefas
1. Descrever o Fluxo do Pipeline CI/CD e Ferramentas Utilizadas
2. Criar um Arquivo YAML Básico para uma Ferramenta CI/CD
3. Explicar como Garantir que o Ambiente de Produção Esteja Protegido Contra Deploys com Falhas

## Solução
### O fluxo do pipeline CI/CD para o Airflow pode ser descrito da seguinte forma:

- Commit e Push: Desenvolvedores fazem commit e push das mudanças no repositório de código (ex.: GitHub, GitLab).
- Validação de Código: Ferramentas de linting e formatação (ex.: Flake8, Black) são executadas para garantir a qualidade do código.
- Testes Automatizados: Execução de testes unitários e de integração nos DAGs usando frameworks como pytest.
- Build e Deploy: Se os testes passarem, o código é empacotado e preparado para deploy.
- Deploy em Ambiente de Staging: O código é implantado em um ambiente de staging para testes adicionais.
- Testes em Staging: Testes adicionais são executados no ambiente de staging para garantir que tudo funcione conforme esperado.
- Deploy em Produção: Se os testes em staging passarem, o código é implantado no ambiente de produção.
- Monitoramento e Alertas: Ferramentas de monitoramento (ex.: Prometheus, Grafana) e alertas (ex.: Slack, Email) são configuradas para notificar a equipe em caso de falhas.


### Garantir que o Ambiente de Produção Esteja Protegido Contra Deploys com Falhas
Para proteger o ambiente de produção contra deploys com falhas, é crucial implementar as seguintes práticas:

1. Ambiente de Staging: Sempre realizar deploys iniciais em um ambiente de staging que replica o ambiente de produção. Assim, você pode realizar testes finais antes de promover o código para produção.
2. Testes Automatizados: Implementar testes automatizados robustos que cubram as principais funcionalidades do sistema. Esses testes devem ser executados em cada commit e durante o deploy.
3. Deploys Gradativos (Canary Deploys): Implementar uma estratégia de deploy gradativo onde as mudanças são liberadas para um pequeno subconjunto de usuários antes de serem liberadas para todos. Isso ajuda a identificar problemas rapidamente sem impactar todos os usuários.
4. Monitoramento Contínuo: Monitorar continuamente o ambiente de produção usando ferramentas como AWS CloudWatch, Grafana, ou Prometheus. Configurar alertas para detectar rapidamente qualquer problema.
5. Rollback Automático: Configurar um mecanismo de rollback automático que reverte para a versão anterior do código em caso de falhas críticas durante ou após o deploy.
