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

Para mais detalhes, consulte o arquivo `explicacao.md` e `workflow.yaml` no diretório `problema-3-ci-cd`.
_________

## Problema 4 - Modelagem de Dados

## Descrição
Um cliente deseja uma base de dados para gerenciar pedidos, clientes e produtos de uma loja virtual. Ele precisa saber:
- Quais são os produtos mais vendidos.
- O histórico de compras de cada cliente.
- A evolução mensal do faturamento.

## Tarefas
1. Modele o banco de dados, criando um esquema ER (Entidade-Relacionamento).
2. Escreva scripts SQL para:
   - Retornar os produtos mais vendidos.
   - Listar o histórico de compras de um cliente específico.
   - Calcular o faturamento mensal.

## Solução

###  Esquema ER
Vamos criar um diagrama ER básico que representa as entidades e seus relacionamentos.

![Diagrama ER](https://github.com/user-attachments/assets/c4254e19-d540-4058-9de0-6bd1ffcd2e14)


* Clientes (customers): Armazena informações dos clientes.
* Produtos (products): Armazena informações dos produtos.
* Pedidos (orders): Armazena informações dos pedidos realizados.
* Itens do Pedido (order_items): Armazena os produtos que compõem cada pedido.

### Scripts SQL

-- Script SQL para Retornar os Produtos Mais Vendidos
```
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
```
-- Script SQL para Listar o Histórico de Compras de um Cliente Específico
```
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
```
-- Script SQL para Calcular o Faturamento Mensal
```
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
```

Para mais detalhes, consulte o arquivo `explicacao.md` e `queries.sql` no diretório `problema-4-modelagem`.

_________

## Problema 5 - Web Scraping

Você precisa monitorar os preços de produtos em um site de e-commerce que atualiza o layout com frequência e bloqueia bots de forma ativa.

### Tarefas
1. Explique como configuraria um scraper resiliente para evitar bloqueios.
2. Escreva um código básico que:
   - Realize o scraping de uma página fictícia com Python.
   - Detecte mudanças no layout (ex.: mudanças de tags HTML).

## Solução

### Estratégia para Configurar um Scraper Resiliente:
* Evitar bloqueios: Rotação de proxies e Alteração de User-Agent.
* Atrasos randômicos
* Detectar mudanças no layout
* Usar ferramentas como BeautifulSoup ou selenium para capturar o HTML.
* Monitorar alterações nos elementos-chave (ex.: tags, IDs, classes).
* Autenticação e Captcha: Implementar automação com selenium para lidar com logins e captchas e usar APIs como 2Captcha para resolver captchas automaticamente.

### Código Básico de Scraping com Detecção de Mudanças no Layout
A seguir, um exemplo de código para realizar scraping de uma página fictícia e detectar mudanças no layout usando Python e a biblioteca BeautifulSoup:

```
import requests
from bs4 import BeautifulSoup
import time
import random
import hashlib

# Função para obter o conteúdo da página
def get_page_content(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

# Função para calcular o hash do conteúdo HTML da página
def calculate_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

# Função para detectar mudanças no layout
def detect_layout_changes(url, headers, previous_hash=None):
    content = get_page_content(url, headers)
    current_hash = calculate_hash(content)
    
    if previous_hash and current_hash != previous_hash:
        print("Mudança detectada no layout da página!")
    else:
        print("Nenhuma mudança detectada no layout da página.")
    
    return current_hash

# Cabeçalhos imitando um navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

# URL da página fictícia
url = 'https://example.com/produtos'

# Intervalo de tempo entre as requisições (2 a 5 segundos)
delay_range = (2, 5)

# Hash anterior do layout
previous_hash = None

# Realizar scraping e detecção de mudanças no layout
for _ in range(5):  # Executar 5 vezes como exemplo
    try:
        previous_hash = detect_layout_changes(url, headers, previous_hash)
    except requests.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
    
    # Atraso aleatório entre as requisições
    time.sleep(random.randint(*delay_range))

print("Scraping finalizado.")
```

### Principais Desafios Técnicos e Soluções

1. Bloqueio de IP:
* Solução: Rotação de proxies e redes VPN.
2. Alteração de layout frequente:
* Solução: Configurar alertas baseados em hashes ou IDs de elementos.
3. Desempenho:
* Solução: Armazenar resultados em banco de dados e configurar tarefas agendadas para rodar em horários fora de pico.

### Testes Unitários

Vamos usar a biblioteca unittest do Python. O teste unitário verificará se o scraper consegue acessar a página corretamente e se a função de detecção de mudanças no layout está funcionando como esperado.

Para executar os testes, você pode rodar o seguinte comando no terminal:
```
python -m unittest problema-5-web-scraping/test_scraper.py
```
Para mais detalhes, consulte o arquivo `test_scraper.py` no diretório `tests`.

_________

## Problema 6 - AWS e Infraestrutura

Sua empresa precisa processar grandes volumes de dados em tempo real e armazená-los para consultas futuras.

### Tarefas
1. Descreva uma arquitetura AWS que inclua:
   - Ingestão em tempo real (ex.: Kinesis).
   - Processamento (ex.: Lambda ou Glue).
   - Armazenamento (ex.: S3 e Redshift).
2. Explique como dimensionar essa arquitetura para lidar com picos de tráfego.

## Solução

Para processar grandes volumes de dados em tempo real e armazená-los para consultas futuras, podemos utilizar uma arquitetura AWS que envolve serviços como Kinesis, Lambda, Glue, S3 e Redshift.

## Componentes da Arquitetura:
1. Ingestão em Tempo Real (Kinesis):
* Amazon Kinesis Data Streams: Coleta e processa dados em tempo real de diversas fontes, como sensores IoT, logs de aplicativos, etc.

2. Processamento (Lambda ou Glue):
* AWS Lambda: Executa código em resposta a eventos, como novos dados chegando no Kinesis, para processamento em tempo real.
* AWS Glue: Serviço de ETL (Extract, Transform, Load) gerenciado que pode ser usado para processamento em lote e transformação de dados.

3. Armazenamento (S3 e Redshift):
* Amazon S3: Armazena dados brutos e processados de forma escalável e econômica.
* Amazon Redshift: Data warehouse para consultas analíticas rápidas e eficientes.

![Diagrama](https://github.com/user-attachments/assets/2cbbb46b-d935-4342-94cf-3be2995ff4c9)

## Dimensionamento para Lidar com Picos de Tráfego
Estratégias de Dimensionamento: 
1. Auto Scaling:
* Kinesis Data Streams: Utilize o auto-scaling para ajustar automaticamente o número de shards com base na taxa de ingestão de dados. Configure alarmes no CloudWatch para monitorar o uso dos shards e ajustar conforme necessário.
- Automatize o ajuste de shards com base em métricas como `IncomingBytes` e `IncomingRecords`.

2. Provisionamento de Capacidade:
* AWS Lambda: Garanta que as funções Lambda estejam configuradas para provisionar a capacidade adequada durante picos de tráfego. Utilize Provisioned Concurrency para manter um pool de instâncias prontas para execução.
- Configure `Provisioned Concurrency` para reduzir a latência de inicialização a frio durante picos de tráfego.

3. Armazenamento Escalável:
* Amazon S3: Escala automaticamente com base na quantidade de dados armazenados. Nenhuma ação adicional é necessária para dimensionar o armazenamento S3.
* Amazon Redshift: Utilize o Redshift Spectrum para consultar diretamente os dados no S3 sem a necessidade de carregá-los no cluster Redshift. Isso permite que você dimensione o armazenamento e o processamento de forma independente.
- Utilize `Elastic Resize` para ajustar a capacidade do cluster Redshift rapidamente em resposta a picos de carga.

4. Monitoramento e Alertas:
* Amazon CloudWatch: Configure métricas e alarmes no CloudWatch para monitorar o desempenho dos componentes da arquitetura e receber alertas em tempo real sobre possíveis gargalos ou falhas.
- Monitore métricas como `PutRecord.Success`, `GetRecords.Success`, `Lambda.Invocations`, `Lambda.Errors`, `Redshift.CPUUtilization`, e `Redshift.DiskSpaceUsage`.

## Código de Exemplo: Lambda para Processamento em Tempo Real:
```
import json
import boto3

def lambda_handler(event, context):
    # Conexão com o S3
    s3 = boto3.client('s3')
    bucket_name = 'meu-bucket'
    
    # Processa eventos recebidos do Kinesis
    for record in event['Records']:
        payload = json.loads(record['kinesis']['data'])
        # Exemplo: transformação simples
        processed_data = {"id": payload["id"], "valor": payload["valor"] * 2}
        
        # Salva dados processados no S3
        key = f"processed/{payload['id']}.json"
        s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(processed_data))
    
    return {"statusCode": 200, "body": "Dados processados e armazenados no S3"}
```
Para mais detalhes, consulte os arquivos no diretório `problema-6-aws`.

_________

## Problema 7 - Monitoramento e Alertas

Um pipeline de dados apresenta falhas esporádicas que só são descobertas dias depois.

### Tarefas
1. Proponha uma solução para implementar monitoramento e alertas em tempo real.
2. Explique quais métricas monitorar (ex.: tempo de execução, volume de dados) e como configurar alertas no CloudWatch ou uma ferramenta equivalente.

## Solução

Para resolver os problemas de falhas esporádicas em um pipeline de dados, é crucial implementar um sistema robusto de monitoramento e alertas em tempo real. Isso permitirá a detecção precoce de problemas e uma resposta rápida para minimizar o impacto.

## Estratégia de Monitoramento:
1. Monitorar métricas críticas:
* Tempo de execução: Identificar atrasos ou execução acima do esperado.
* Volume de dados: Detectar entradas ou saídas anormais.
* Taxa de falhas: Monitorar logs para erros recorrentes.

2. Configurar alertas em tempo real:
* Usar Amazon CloudWatch para coletar métricas e criar alarmes.
* Enviar notificações via SNS (e-mail, SMS ou integração com ferramentas como Slack/Teams).

## Configuração do Monitoramento no AWS CloudWatch:
1. Métricas para pipelines:
* Lambda:
   * Erros (Errors), duração (Duration), e invocações (Invocations).
* Glue ou EMR:
   * Status das execuções, volume de dados processados.
* S3:
   * Número de objetos adicionados/removidos.

2. Configuração de alarmes:
* Exemplo: Configurar um alarme para falhas de execução em um job do Glue.

```
aws cloudwatch put-metric-alarm \
    --alarm-name "GlueJobFailures" \
    --metric-name "FailedJobs" \
    --namespace "AWS/Glue" \
    --statistic "Sum" \
    --threshold 1 \
    --comparison-operator "GreaterThanOrEqualToThreshold" \
    --evaluation-periods 1 \
    --alarm-actions arn:aws:sns:us-east-1:123456789012:NotifyMe
```

## Estrutura de Alertas em Tempo Real:
1. Pipeline de Monitoramento:
* Coleta de logs em CloudWatch Logs.
* Análise em CloudWatch Metrics.
* Notificações configuradas com SNS.

2. Ferramentas Complementares:
* Amazon EventBridge: Automatizar respostas a eventos críticos (ex.: reprocessar jobs).
* Integração com sistemas de observabilidade como Datadog ou Prometheus.

## Código Python para Monitoramento e Notificações:
Exemplo de um script que verifica métricas e envia alertas:

```
import boto3

cloudwatch = boto3.client('cloudwatch')
sns = boto3.client('sns')

def check_failed_jobs():
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/Glue',
        MetricName='FailedJobs',
        Dimensions=[{'Name': 'JobName', 'Value': 'meu-job-glue'}],
        StartTime=datetime.utcnow() - timedelta(minutes=15),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=['Sum']
    )
    
    if response['Datapoints']:
        failed_jobs = response['Datapoints'][0]['Sum']
        if failed_jobs > 0:
            sns.publish(
                TopicArn='arn:aws:sns:us-east-1:123456789012:NotifyMe',
                Message=f"Falhas detectadas: {failed_jobs}",
                Subject="Alerta: Falhas no Job Glue"
            )

check_failed_jobs()
```
Para mais detalhes, consulte os arquivos no diretório `problema-7-monitoramento`.

_________

## Problema 8 - Data Governance e Segurança

Sua empresa precisa garantir que os dados sensíveis armazenados em seu ambiente AWS estejam protegidos e em conformidade com regulamentações como LGPD ou GDPR.

### Tarefas
1. Proponha uma estratégia para garantir:
   - Controle de acesso apropriado em S3 e Redshift.
   - Criptografia de dados em repouso e em trânsito.
   - Logs detalhados de acesso e auditoria.
2. Explique como você verificaria se a empresa está em conformidade com regulamentações de proteção de dados.
